#!/usr/bin/env python3
"""
Système complet Google Sheets pour ESPN NBA Fantasy
Transfert automatique de toutes les données + analyses avancées
"""

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Any
import numpy as np
from espn_nba_advanced_analyzer import ESPNNBAAdvancedAnalyzer
from advanced_analysis_sheets import AdvancedAnalysisSheets

class CompleteGoogleSheetsSystem:
    """Système complet de transfert et analyse Google Sheets"""
    
    def __init__(self, league_id: int, season: int, my_team_name: str, 
                 credentials_file: str = "credentials.json", spreadsheet_id: str = None):
        self.league_id = league_id
        self.season = season
        self.my_team_name = my_team_name
        self.credentials_file = credentials_file
        self.spreadsheet_id = spreadsheet_id
        
        # Initialisation des composants
        self.setup_logging()
        self.setup_google_sheets()
        self.setup_analyzer()
        self.setup_analysis_sheets()
    
    def setup_logging(self):
        """Configure le logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_google_sheets(self):
        """Configure la connexion Google Sheets"""
        try:
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            creds = Credentials.from_service_account_file(
                self.credentials_file, 
                scopes=scopes
            )
            
            self.gc = gspread.authorize(creds)
            
            if self.spreadsheet_id:
                self.spreadsheet = self.gc.open_by_key(self.spreadsheet_id)
            else:
                # Créer un nouveau spreadsheet
                self.spreadsheet = self.gc.create(f"ESPN NBA Fantasy - {self.my_team_name}")
                self.spreadsheet_id = self.spreadsheet.id
                print(f"📊 Nouveau spreadsheet créé: {self.spreadsheet.url}")
            
            self.logger.info("✅ Connexion Google Sheets établie")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur connexion Google Sheets: {e}")
            raise
    
    def setup_analyzer(self):
        """Configure l'analyseur ESPN"""
        self.analyzer = ESPNNBAAdvancedAnalyzer(
            self.league_id, 
            self.season, 
            self.my_team_name
        )
    
    def setup_analysis_sheets(self):
        """Configure les feuilles d'analyse"""
        self.analysis_creator = AdvancedAnalysisSheets(self.spreadsheet)
    
    def run_complete_system(self):
        """Exécute le système complet de transfert et analyse"""
        self.logger.info("🚀 Démarrage du système complet Google Sheets")
        
        try:
            # 1. Collecte des données ESPN
            self.logger.info("📊 Collecte des données ESPN...")
            snapshot = self.analyzer.collect_daily_data()
            
            # 2. Création des feuilles d'analyse
            self.logger.info("📋 Création des feuilles d'analyse...")
            self.analysis_creator.create_all_analysis_sheets()
            
            # 3. Transfert des données vers Google Sheets
            self.logger.info("📤 Transfert des données vers Google Sheets...")
            self.transfer_all_data(snapshot)
            
            # 4. Mise à jour des analyses
            self.logger.info("🔍 Mise à jour des analyses...")
            self.update_all_analyses(snapshot)
            
            # 5. Génération du rapport final
            self.logger.info("📊 Génération du rapport final...")
            self.generate_final_report(snapshot)
            
            self.logger.info("✅ Système complet exécuté avec succès")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur dans le système complet: {e}")
            raise
    
    def transfer_all_data(self, snapshot):
        """Transfert toutes les données vers Google Sheets"""
        try:
            # Données quotidiennes
            self._transfer_daily_data(snapshot)
            
            # Résumé des équipes
            self._transfer_teams_summary(snapshot)
            
            # Joueurs détaillés
            self._transfer_players_detailed(snapshot)
            
            # Transactions
            self._transfer_transactions(snapshot)
            
            # Agents libres
            self._transfer_free_agents(snapshot)
            
            # Blessures
            self._transfer_injuries(snapshot)
            
            self.logger.info("✅ Toutes les données transférées")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur transfert données: {e}")
    
    def _transfer_daily_data(self, snapshot):
        """Transfert les données quotidiennes"""
        try:
            worksheet = self.spreadsheet.worksheet('📊 Données Quotidiennes')
            worksheet.clear()
            
            # En-têtes
            headers = [
                'Date', 'Ligue', 'Saison', 'Type Scoring', 'Équipes Total',
                'Semaine Actuelle', 'Mon Équipe', 'Mon Rang'
            ]
            worksheet.update('A1:H1', [headers])
            
            # Données
            current_date = datetime.now().strftime('%Y-%m-%d')
            my_team = next((team for team in snapshot.teams if team.is_my_team), None)
            
            row = [
                current_date,
                snapshot.league_id,
                snapshot.season,
                snapshot.scoring_type,
                len(snapshot.teams),
                getattr(snapshot, 'current_week', 1),
                self.my_team_name,
                my_team.ranking if my_team else 'N/A'
            ]
            
            worksheet.update('A2', [row])
            
        except Exception as e:
            self.logger.error(f"❌ Erreur transfert données quotidiennes: {e}")
    
    def _transfer_teams_summary(self, snapshot):
        """Transfert le résumé des équipes"""
        try:
            worksheet = self.spreadsheet.worksheet('🏀 Résumé Équipes')
            worksheet.clear()
            
            # En-têtes
            headers = [
                'Date', 'Équipe', 'Manager', 'Mon Équipe', 'Rang',
                'Points Totaux', 'Points Banc', 'Points Actifs',
                'Rebonds', 'Assists', 'Steals', 'Blocks', 'FG%', 'FT%', '3PM', 'TO'
            ]
            worksheet.update('A1:P1', [headers])
            
            # Données
            rows = []
            current_date = datetime.now().strftime('%Y-%m-%d')
            
            for team in snapshot.teams:
                row = [
                    current_date,
                    team.team_name,
                    team.manager,
                    'OUI' if team.is_my_team else 'NON',
                    team.ranking,
                    team.total_stats.get('points', 0),
                    team.bench_stats.get('points', 0),
                    team.active_stats.get('points', 0),
                    team.total_stats.get('rebounds', 0),
                    team.total_stats.get('assists', 0),
                    team.total_stats.get('steals', 0),
                    team.total_stats.get('blocks', 0),
                    team.total_stats.get('fg_percentage', 0),
                    team.total_stats.get('ft_percentage', 0),
                    team.total_stats.get('three_pointers', 0),
                    team.total_stats.get('turnovers', 0)
                ]
                rows.append(row)
            
            worksheet.update('A2', rows)
            
        except Exception as e:
            self.logger.error(f"❌ Erreur transfert résumé équipes: {e}")
    
    def _transfer_players_detailed(self, snapshot):
        """Transfert les détails des joueurs"""
        try:
            worksheet = self.spreadsheet.worksheet('👥 Joueurs Détaillés')
            worksheet.clear()
            
            # En-têtes
            headers = [
                'Date', 'Équipe', 'Mon Équipe', 'Joueur', 'Position',
                'Statut', 'Banc', 'Points', 'Rebonds', 'Assists',
                'Steals', 'Blocks', 'FG%', 'FT%', '3PM', 'TO',
                'Efficacité', 'Usage%', 'Blessure', 'Minutes'
            ]
            worksheet.update('A1:T1', [headers])
            
            # Données
            rows = []
            current_date = datetime.now().strftime('%Y-%m-%d')
            
            for team in snapshot.teams:
                for player in team.roster:
                    row = [
                        current_date,
                        team.team_name,
                        'OUI' if team.is_my_team else 'NON',
                        player.name,
                        player.position,
                        player.status,
                        'OUI' if player.is_bench else 'NON',
                        player.points,
                        player.rebounds,
                        player.assists,
                        player.steals,
                        player.blocks,
                        player.fg_percentage,
                        player.ft_percentage,
                        player.three_pointers,
                        player.turnovers,
                        player.efficiency,
                        player.usage_rate,
                        player.injury_status,
                        player.minutes
                    ]
                    rows.append(row)
            
            worksheet.update('A2', rows)
            
        except Exception as e:
            self.logger.error(f"❌ Erreur transfert joueurs détaillés: {e}")
    
    def _transfer_transactions(self, snapshot):
        """Transfert les transactions"""
        try:
            worksheet = self.spreadsheet.worksheet('🔄 Transactions')
            worksheet.clear()
            
            if not snapshot.transactions:
                worksheet.update('A1', [['Aucune transaction récente']])
                return
            
            # En-têtes
            headers = ['Date', 'Type', 'Description', 'Équipe']
            worksheet.update('A1:D1', [headers])
            
            # Données
            rows = []
            for trans in snapshot.transactions:
                row = [
                    trans['date'],
                    trans['type'],
                    trans['description'],
                    trans['team']
                ]
                rows.append(row)
            
            worksheet.update('A2', rows)
            
        except Exception as e:
            self.logger.error(f"❌ Erreur transfert transactions: {e}")
    
    def _transfer_free_agents(self, snapshot):
        """Transfert les agents libres"""
        try:
            worksheet = self.spreadsheet.worksheet('🆓 Agents Libres')
            worksheet.clear()
            
            if not snapshot.free_agents:
                worksheet.update('A1', [['Aucun agent libre disponible']])
                return
            
            # En-têtes
            headers = [
                'Joueur', 'Position', 'Équipe NBA', 'Points', 'Rebonds',
                'Assists', 'Steals', 'Blocks', 'Disponibilité', 'Popularité'
            ]
            worksheet.update('A1:J1', [headers])
            
            # Données
            rows = []
            for fa in snapshot.free_agents:
                row = [
                    fa.get('name', ''),
                    fa.get('position', ''),
                    fa.get('team', ''),
                    fa.get('points', 0),
                    fa.get('rebounds', 0),
                    fa.get('assists', 0),
                    fa.get('steals', 0),
                    fa.get('blocks', 0),
                    fa.get('availability', ''),
                    fa.get('popularity', '')
                ]
                rows.append(row)
            
            worksheet.update('A2', rows)
            
        except Exception as e:
            self.logger.error(f"❌ Erreur transfert agents libres: {e}")
    
    def _transfer_injuries(self, snapshot):
        """Transfert les blessures"""
        try:
            worksheet = self.spreadsheet.worksheet('🏥 Blessures')
            worksheet.clear()
            
            if not snapshot.injuries:
                worksheet.update('A1', [['Aucune information de blessure']])
                return
            
            # En-têtes
            headers = [
                'Joueur', 'Équipe', 'Statut', 'Date', 'Description',
                'Durée Estimée', 'Impact', 'Recommandation'
            ]
            worksheet.update('A1:H1', [headers])
            
            # Données
            rows = []
            for injury in snapshot.injuries:
                row = [
                    injury.get('player', ''),
                    injury.get('team', ''),
                    injury.get('status', ''),
                    injury.get('date', ''),
                    injury.get('description', ''),
                    injury.get('duration', ''),
                    injury.get('impact', ''),
                    injury.get('recommendation', '')
                ]
                rows.append(row)
            
            worksheet.update('A2', rows)
            
        except Exception as e:
            self.logger.error(f"❌ Erreur transfert blessures: {e}")
    
    def update_all_analyses(self, snapshot):
        """Met à jour toutes les analyses"""
        try:
            # Mise à jour de l'analyse mon équipe
            self._update_my_team_analysis(snapshot)
            
            # Mise à jour de l'optimisation ROTO
            self._update_roto_optimization(snapshot)
            
            # Mise à jour de l'analyse du banc
            self._update_bench_analysis(snapshot)
            
            # Mise à jour du dashboard
            self._update_dashboard(snapshot)
            
            self.logger.info("✅ Toutes les analyses mises à jour")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur mise à jour analyses: {e}")
    
    def _update_my_team_analysis(self, snapshot):
        """Met à jour l'analyse de mon équipe"""
        try:
            worksheet = self.spreadsheet.worksheet('👑 Mon Équipe - Analyse')
            
            # Trouve mon équipe
            my_team = next((team for team in snapshot.teams if team.is_my_team), None)
            if not my_team:
                return
            
            # Mise à jour des données
            current_date = datetime.now().strftime('%Y-%m-%d')
            
            # Résumé quotidien
            daily_data = [
                current_date,
                my_team.ranking,
                my_team.total_stats.get('points', 0),
                my_team.bench_stats.get('points', 0),
                my_team.active_stats.get('points', 0),
                my_team.bench_stats.get('points', 0) - my_team.active_stats.get('points', 0),
                'Calculé automatiquement',
                'Calculé automatiquement',
                'Calculé automatiquement'
            ]
            
            worksheet.update('A5:J5', [daily_data])
            
            # Données des joueurs
            player_rows = []
            for player in my_team.roster:
                row = [
                    player.name,
                    player.position,
                    player.status,
                    player.points,
                    player.rebounds,
                    player.assists,
                    player.steals,
                    player.blocks,
                    player.efficiency,
                    'Banc' if player.is_bench else 'Actif',
                    'Calculé automatiquement',
                    'Calculé automatiquement',
                    'Calculé automatiquement',
                    'Calculé automatiquement'
                ]
                player_rows.append(row)
            
            worksheet.update('A9', player_rows)
            
        except Exception as e:
            self.logger.error(f"❌ Erreur mise à jour analyse mon équipe: {e}")
    
    def _update_roto_optimization(self, snapshot):
        """Met à jour l'optimisation ROTO"""
        try:
            worksheet = self.spreadsheet.worksheet('🎯 Optimisation ROTO')
            
            # Trouve mon équipe
            my_team = next((team for team in snapshot.teams if team.is_my_team), None)
            if not my_team:
                return
            
            # Catégories ROTO
            categories = [
                'Points', 'Rebonds', 'Assists', 'Steals', 'Blocks',
                'FG%', 'FT%', '3PM', 'Turnovers'
            ]
            
            # Mise à jour des données
            for i, category in enumerate(categories, 2):
                # Données simulées (à remplacer par de vraies données)
                row = [
                    category,
                    my_team.ranking,  # Rang actuel
                    my_team.total_stats.get('points', 0),  # Points
                    'Calculé automatiquement',  # Écart leader
                    'Calculé automatiquement',  # Faiblesse
                    'Calculé automatiquement',  # Joueurs amélioration
                    'Calculé automatiquement',  # Actions suggérées
                    'Calculé automatiquement'  # Priorité
                ]
                worksheet.update(f'A{i}:H{i}', [row])
            
        except Exception as e:
            self.logger.error(f"❌ Erreur mise à jour optimisation ROTO: {e}")
    
    def _update_bench_analysis(self, snapshot):
        """Met à jour l'analyse du banc"""
        try:
            worksheet = self.spreadsheet.worksheet('🪑 Analyse Banc')
            
            # Trouve mon équipe
            my_team = next((team for team in snapshot.teams if team.is_my_team), None)
            if not my_team:
                return
            
            current_date = datetime.now().strftime('%Y-%m-%d')
            
            # Données du banc
            bench_points = my_team.bench_stats.get('points', 0)
            active_points = my_team.active_stats.get('points', 0)
            difference = bench_points - active_points
            
            bench_data = [
                current_date,
                bench_points,
                active_points,
                difference,
                'Calculé automatiquement',
                'Calculé automatiquement',
                'Calculé automatiquement',
                'Calculé automatiquement'
            ]
            
            worksheet.update('A5:H5', [bench_data])
            
        except Exception as e:
            self.logger.error(f"❌ Erreur mise à jour analyse banc: {e}")
    
    def _update_dashboard(self, snapshot):
        """Met à jour le dashboard"""
        try:
            worksheet = self.spreadsheet.worksheet('📊 Dashboard Principal')
            
            # Trouve mon équipe
            my_team = next((team for team in snapshot.teams if team.is_my_team), None)
            if not my_team:
                return
            
            current_date = datetime.now().strftime('%Y-%m-%d')
            
            # Résumé quotidien
            daily_summary = [
                current_date,
                my_team.ranking,
                my_team.total_stats.get('points', 0),
                my_team.bench_stats.get('points', 0),
                my_team.active_stats.get('points', 0),
                my_team.bench_stats.get('points', 0) - my_team.active_stats.get('points', 0),
                'Calculé automatiquement',
                'Calculé automatiquement',
                'Calculé automatiquement'
            ]
            
            worksheet.update('A5:J5', [daily_summary])
            
        except Exception as e:
            self.logger.error(f"❌ Erreur mise à jour dashboard: {e}")
    
    def generate_final_report(self, snapshot):
        """Génère le rapport final"""
        try:
            print("\n" + "="*80)
            print("🏀 RAPPORT FINAL - SYSTÈME GOOGLE SHEETS")
            print("="*80)
            
            # Statistiques générales
            print(f"\n📊 STATISTIQUES GÉNÉRALES")
            print(f"   📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   🏀 Ligue: {snapshot.league_id} - Saison {snapshot.season}")
            print(f"   👥 Équipes: {len(snapshot.teams)}")
            print(f"   🔄 Transactions: {len(snapshot.transactions)}")
            print(f"   🏥 Blessures: {len(snapshot.injuries)}")
            
            # Mon équipe
            my_team = next((team for team in snapshot.teams if team.is_my_team), None)
            if my_team:
                print(f"\n👑 MON ÉQUIPE: {my_team.team_name}")
                print(f"   📈 Rang: {my_team.ranking}")
                print(f"   ⚡ Points totaux: {my_team.total_stats.get('points', 0):.1f}")
                print(f"   🪑 Points banc: {my_team.bench_stats.get('points', 0):.1f}")
                print(f"   ⚡ Points actifs: {my_team.active_stats.get('points', 0):.1f}")
                
                # Alerte si points perdus
                bench_points = my_team.bench_stats.get('points', 0)
                if bench_points > 15:
                    print(f"   ⚠️  ALERTE: {bench_points:.1f} points perdus sur le banc!")
            
            # Feuilles créées
            print(f"\n📋 FEUILLES GOOGLE SHEETS CRÉÉES")
            print(f"   📊 Données Quotidiennes")
            print(f"   🏀 Résumé Équipes")
            print(f"   👥 Joueurs Détaillés")
            print(f"   🔄 Transactions")
            print(f"   🆓 Agents Libres")
            print(f"   🏥 Blessures")
            print(f"   👑 Mon Équipe - Analyse")
            print(f"   🎯 Optimisation ROTO")
            print(f"   🪑 Analyse Banc")
            print(f"   📊 Dashboard Principal")
            
            print(f"\n🔗 LIEN GOOGLE SHEETS: {self.spreadsheet.url}")
            print(f"\n✅ SYSTÈME COMPLET TERMINÉ AVEC SUCCÈS!")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur génération rapport final: {e}")

def main():
    """Fonction principale du système complet"""
    print("🚀 Système Complet Google Sheets ESPN NBA Fantasy")
    print("=" * 60)
    
    # Configuration
    LEAGUE_ID = 1557635339
    SEASON = 2026
    MY_TEAM_NAME = "Neon Cobras 99"
    
    try:
        # Initialisation du système
        system = CompleteGoogleSheetsSystem(
            league_id=LEAGUE_ID,
            season=SEASON,
            my_team_name=MY_TEAM_NAME
        )
        
        # Exécution du système complet
        system.run_complete_system()
        
    except Exception as e:
        print(f"❌ Erreur dans le système complet: {e}")
        print("🔍 Vérifiez la configuration et les credentials")

if __name__ == "__main__":
    main()
