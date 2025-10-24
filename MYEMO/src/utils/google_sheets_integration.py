#!/usr/bin/env python3
"""
Intégration Google Sheets pour ESPN NBA Fantasy Data
Export automatique des données vers Google Sheets pour analyses avancées
Système complet avec feuilles d'analyse et visualisations
"""

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Any
import numpy as np

class GoogleSheetsNBAExporter:
    """Exportateur vers Google Sheets pour les données NBA Fantasy avec analyses avancées"""
    
    def __init__(self, credentials_file: str = "credentials.json", spreadsheet_id: str = None):
        self.credentials_file = credentials_file
        self.spreadsheet_id = spreadsheet_id
        self.setup_google_sheets()
        self.setup_logging()
    
    def setup_google_sheets(self):
        """Configure la connexion à Google Sheets"""
        try:
            # Définition des scopes
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Chargement des credentials
            creds = Credentials.from_service_account_file(
                self.credentials_file, 
                scopes=scopes
            )
            
            # Initialisation de gspread
            self.gc = gspread.authorize(creds)
            
            # Création ou ouverture du spreadsheet
            if self.spreadsheet_id:
                self.spreadsheet = self.gc.open_by_key(self.spreadsheet_id)
            else:
                # Créer un nouveau spreadsheet
                self.spreadsheet = self.gc.create("ESPN NBA Fantasy Data - Neon Cobras 99")
                self.spreadsheet_id = self.spreadsheet.id
                print(f"📊 Nouveau spreadsheet créé: {self.spreadsheet.url}")
            
            logging.info("✅ Connexion Google Sheets établie")
            
        except Exception as e:
            logging.error(f"❌ Erreur connexion Google Sheets: {e}")
            raise
    
    def setup_logging(self):
        """Configure le logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def create_worksheets(self):
        """Crée les feuilles de calcul nécessaires avec structure d'analyse"""
        worksheets = {
            # Feuilles de données
            'daily_snapshot': '📊 Données Quotidiennes',
            'teams_summary': '🏀 Résumé Équipes',
            'players_detailed': '👥 Joueurs Détaillés',
            'transactions': '🔄 Transactions',
            'free_agents': '🆓 Agents Libres',
            'injuries': '🏥 Blessures',
            
            # Feuilles d'analyse
            'rankings': '📈 Classements ROTO',
            'bench_analysis': '🪑 Analyse Banc',
            'ai_insights': '🤖 Insights IA',
            'trends': '📊 Tendances',
            'my_team_analysis': '👑 Mon Équipe - Analyse',
            'roto_optimization': '🎯 Optimisation ROTO',
            'trade_analysis': '💼 Analyse Trades',
            'streaming_targets': '🎯 Cibles Streaming',
            'injury_management': '🏥 Gestion Blessures',
            'weekly_report': '📅 Rapport Hebdomadaire',
            'dashboard': '📊 Dashboard Principal'
        }
        
        for sheet_name, title in worksheets.items():
            try:
                # Vérifie si la feuille existe
                try:
                    self.spreadsheet.worksheet(title)
                    self.logger.info(f"📊 Feuille '{title}' existe déjà")
                except:
                    # Crée la feuille si elle n'existe pas
                    worksheet = self.spreadsheet.add_worksheet(title=title, rows=2000, cols=30)
                    
                    # Configuration spéciale selon le type de feuille
                    if 'analysis' in sheet_name or 'dashboard' in sheet_name:
                        self._setup_analysis_worksheet(worksheet, sheet_name)
                    
                    self.logger.info(f"✅ Feuille '{title}' créée")
                    
            except Exception as e:
                self.logger.error(f"❌ Erreur création feuille '{title}': {e}")
    
    def _setup_analysis_worksheet(self, worksheet, sheet_name):
        """Configure une feuille d'analyse avec formules et formatage"""
        try:
            if sheet_name == 'my_team_analysis':
                self._setup_my_team_analysis(worksheet)
            elif sheet_name == 'roto_optimization':
                self._setup_roto_optimization(worksheet)
            elif sheet_name == 'dashboard':
                self._setup_dashboard(worksheet)
            elif sheet_name == 'bench_analysis':
                self._setup_bench_analysis(worksheet)
                
        except Exception as e:
            self.logger.error(f"❌ Erreur configuration feuille {sheet_name}: {e}")
    
    def _setup_my_team_analysis(self, worksheet):
        """Configure la feuille d'analyse de mon équipe"""
        headers = [
            'Date', 'Statut', 'Joueur', 'Position', 'Points', 'Rebonds', 'Assists',
            'Steals', 'Blocks', 'Efficacité', 'Banc/Actif', 'Impact Classement',
            'Recommandation', 'Priorité'
        ]
        worksheet.update('A1:N1', [headers])
        
        # Formules d'analyse
        formulas = [
            ['=IF(K2="Banc","⚠️ Points perdus","✅ Optimisé")', 'L2'],
            ['=IF(J2>30,"🔥 Hot","❄️ Cold")', 'M2'],
            ['=IF(L2="⚠️ Points perdus","🔴 Haute","🟢 Normale")', 'N2']
        ]
        
        for formula, cell in formulas:
            worksheet.update(cell, [[formula]])
    
    def _setup_roto_optimization(self, worksheet):
        """Configure la feuille d'optimisation ROTO"""
        headers = [
            'Catégorie', 'Mon Rang', 'Points', 'Écart Leader', 'Faiblesse',
            'Joueurs Amélioration', 'Actions Suggérées', 'Priorité'
        ]
        worksheet.update('A1:H1', [headers])
        
        # Catégories ROTO
        roto_categories = [
            'Points', 'Rebonds', 'Assists', 'Steals', 'Blocks',
            'FG%', 'FT%', '3PM', 'Turnovers'
        ]
        
        for i, category in enumerate(roto_categories, 2):
            worksheet.update(f'A{i}', [[category]])
    
    def _setup_dashboard(self, worksheet):
        """Configure le dashboard principal"""
        # Titre principal
        worksheet.update('A1', [['🏀 ESPN NBA FANTASY DASHBOARD - NEON COBRAS 99']])
        worksheet.update('A1:Z1', [['🏀 ESPN NBA FANTASY DASHBOARD - NEON COBRAS 99']])
        
        # Sections du dashboard
        sections = [
            ['📊 RÉSUMÉ QUOTIDIEN', 'A3'],
            ['🏆 CLASSEMENT ACTUEL', 'A6'],
            ['⚠️ ALERTES IMPORTANTES', 'A9'],
            ['🎯 RECOMMANDATIONS IA', 'A12'],
            ['📈 TENDANCES', 'A15'],
            ['🔄 ACTIVITÉ RÉCENTE', 'A18']
        ]
        
        for section, cell in sections:
            worksheet.update(cell, [[section]])
    
    def _setup_bench_analysis(self, worksheet):
        """Configure la feuille d'analyse du banc"""
        headers = [
            'Date', 'Équipe', 'Points Banc', 'Points Actifs', 'Différence',
            'Impact %', 'Recommandation', 'Action Requise', 'Priorité'
        ]
        worksheet.update('A1:I1', [headers])
        
        # Formules de calcul
        formulas = [
            ['=E2/C2*100', 'F2'],  # Impact %
            ['=IF(E2>20,"🔴 URGENT","🟡 Modéré")', 'G2'],  # Recommandation
            ['=IF(E2>20,"Changer lineup","Surveiller")', 'H2'],  # Action
            ['=IF(E2>20,"Haute","Normale")', 'I2']  # Priorité
        ]
        
        for formula, cell in formulas:
            worksheet.update(cell, [[formula]])
    
    def export_daily_snapshot(self, snapshot_data: Dict):
        """Exporte les données quotidiennes vers Google Sheets"""
        try:
            # Feuille: Données Quotidiennes
            self._export_to_sheet('Données Quotidiennes', snapshot_data['league_info'])
            
            # Feuille: Résumé Équipes
            self._export_teams_summary(snapshot_data['teams_summary'])
            
            # Feuille: Joueurs Détaillés
            self._export_players_detailed(snapshot_data['players_detailed'])
            
            # Feuille: Transactions
            self._export_transactions(snapshot_data['transactions'])
            
            # Feuille: Agents Libres
            self._export_free_agents(snapshot_data['free_agents'])
            
            # Feuille: Blessures
            self._export_injuries(snapshot_data['injuries'])
            
            # Feuille: Insights IA
            self._export_ai_insights(snapshot_data['ai_insights'])
            
            self.logger.info("✅ Export quotidien vers Google Sheets terminé")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur export quotidien: {e}")
    
    def _export_to_sheet(self, sheet_name: str, data: Dict):
        """Exporte des données vers une feuille spécifique"""
        try:
            worksheet = self.spreadsheet.worksheet(sheet_name)
            
            # Efface le contenu existant
            worksheet.clear()
            
            # Prépare les données
            if isinstance(data, dict):
                # Convertit le dict en liste de listes
                rows = []
                for key, value in data.items():
                    rows.append([key, str(value)])
                
                # Ajoute les en-têtes
                worksheet.update('A1:B1', [['Clé', 'Valeur']])
                worksheet.update('A2', rows)
            else:
                worksheet.update('A1', [[str(data)]])
                
        except Exception as e:
            self.logger.error(f"❌ Erreur export vers '{sheet_name}': {e}")
    
    def _export_teams_summary(self, teams_data: List[Dict]):
        """Exporte le résumé des équipes"""
        try:
            worksheet = self.spreadsheet.worksheet('Résumé Équipes')
            worksheet.clear()
            
            # En-têtes
            headers = [
                'Date', 'Équipe', 'Manager', 'Mon Équipe', 'Rang', 
                'Points Totaux', 'Points Banc', 'Points Actifs',
                'Rebonds', 'Assists', 'Steals', 'Blocks'
            ]
            
            worksheet.update('A1', [headers])
            
            # Données
            rows = []
            current_date = datetime.now().strftime('%Y-%m-%d')
            
            for team in teams_data:
                row = [
                    current_date,
                    team['team_name'],
                    team['manager'],
                    'OUI' if team['is_my_team'] else 'NON',
                    team['ranking'],
                    team['total_points'],
                    team['bench_points'],
                    team['active_points'],
                    # Ajouter d'autres stats selon les données disponibles
                    0, 0, 0, 0  # Placeholders pour les autres stats
                ]
                rows.append(row)
            
            worksheet.update('A2', rows)
            
        except Exception as e:
            self.logger.error(f"❌ Erreur export résumé équipes: {e}")
    
    def _export_players_detailed(self, players_data: List[Dict]):
        """Exporte les détails des joueurs"""
        try:
            worksheet = self.spreadsheet.worksheet('Joueurs Détaillés')
            worksheet.clear()
            
            # En-têtes
            headers = [
                'Date', 'Équipe', 'Mon Équipe', 'Joueur', 'Position',
                'Statut', 'Banc', 'Points', 'Rebonds', 'Assists',
                'Steals', 'Blocks', 'Efficacité', 'Blessure'
            ]
            
            worksheet.update('A1', [headers])
            
            # Données
            rows = []
            for player in players_data:
                row = [
                    player['date'],
                    player['team'],
                    'OUI' if player['is_my_team'] else 'NON',
                    player['player_name'],
                    player['position'],
                    player['status'],
                    'OUI' if player['is_bench'] else 'NON',
                    player['points'],
                    player['rebounds'],
                    player['assists'],
                    player['steals'],
                    player['blocks'],
                    player['efficiency'],
                    player['injury_status']
                ]
                rows.append(row)
            
            worksheet.update('A2', rows)
            
        except Exception as e:
            self.logger.error(f"❌ Erreur export joueurs détaillés: {e}")
    
    def _export_transactions(self, transactions_data: List[Dict]):
        """Exporte les transactions"""
        try:
            worksheet = self.spreadsheet.worksheet('Transactions')
            worksheet.clear()
            
            if not transactions_data:
                worksheet.update('A1', [['Aucune transaction récente']])
                return
            
            # En-têtes
            headers = ['Date', 'Type', 'Description', 'Équipe']
            worksheet.update('A1', [headers])
            
            # Données
            rows = []
            for trans in transactions_data:
                row = [
                    trans['date'],
                    trans['type'],
                    trans['description'],
                    trans['team']
                ]
                rows.append(row)
            
            worksheet.update('A2', rows)
            
        except Exception as e:
            self.logger.error(f"❌ Erreur export transactions: {e}")
    
    def _export_free_agents(self, free_agents_data: List[Dict]):
        """Exporte les agents libres"""
        try:
            worksheet = self.spreadsheet.worksheet('Agents Libres')
            worksheet.clear()
            
            if not free_agents_data:
                worksheet.update('A1', [['Aucun agent libre disponible']])
                return
            
            # En-têtes
            headers = ['Joueur', 'Position', 'Équipe NBA', 'Points', 'Rebonds', 'Assists', 'Disponibilité']
            worksheet.update('A1', [headers])
            
            # Données
            rows = []
            for fa in free_agents_data:
                row = [
                    fa.get('name', ''),
                    fa.get('position', ''),
                    fa.get('team', ''),
                    fa.get('points', 0),
                    fa.get('rebounds', 0),
                    fa.get('assists', 0),
                    fa.get('availability', '')
                ]
                rows.append(row)
            
            worksheet.update('A2', rows)
            
        except Exception as e:
            self.logger.error(f"❌ Erreur export agents libres: {e}")
    
    def _export_injuries(self, injuries_data: List[Dict]):
        """Exporte les informations sur les blessures"""
        try:
            worksheet = self.spreadsheet.worksheet('Blessures')
            worksheet.clear()
            
            if not injuries_data:
                worksheet.update('A1', [['Aucune information de blessure']])
                return
            
            # En-têtes
            headers = ['Joueur', 'Équipe', 'Statut', 'Date', 'Description']
            worksheet.update('A1', [headers])
            
            # Données
            rows = []
            for injury in injuries_data:
                row = [
                    injury.get('player', ''),
                    injury.get('team', ''),
                    injury.get('status', ''),
                    injury.get('date', ''),
                    injury.get('description', '')
                ]
                rows.append(row)
            
            worksheet.update('A2', rows)
            
        except Exception as e:
            self.logger.error(f"❌ Erreur export blessures: {e}")
    
    def _export_ai_insights(self, ai_insights: List[Dict]):
        """Exporte les insights IA"""
        try:
            worksheet = self.spreadsheet.worksheet('Insights IA')
            worksheet.clear()
            
            if not ai_insights:
                worksheet.update('A1', [['Aucun insight IA disponible']])
                return
            
            # En-têtes
            headers = ['Date', 'Type', 'Priorité', 'Message', 'Action Suggérée']
            worksheet.update('A1', [headers])
            
            # Données
            rows = []
            current_date = datetime.now().strftime('%Y-%m-%d')
            
            for insight in ai_insights:
                row = [
                    current_date,
                    insight.get('type', ''),
                    insight.get('priority', ''),
                    insight.get('message', ''),
                    insight.get('action', '')
                ]
                rows.append(row)
            
            worksheet.update('A2', rows)
            
        except Exception as e:
            self.logger.error(f"❌ Erreur export insights IA: {e}")
    
    def create_bench_analysis_sheet(self, snapshot_data: Dict):
        """Crée une feuille d'analyse spécifique pour les points perdus sur le banc"""
        try:
            worksheet = self.spreadsheet.worksheet('Analyse Banc')
            worksheet.clear()
            
            # En-têtes
            headers = [
                'Date', 'Équipe', 'Points Banc', 'Points Actifs', 
                'Différence', 'Impact Classement', 'Recommandation'
            ]
            
            worksheet.update('A1', [headers])
            
            # Analyse pour chaque équipe
            rows = []
            current_date = datetime.now().strftime('%Y-%m-%d')
            
            for team in snapshot_data['teams_summary']:
                bench_points = team.get('bench_points', 0)
                active_points = team.get('active_points', 0)
                difference = bench_points - active_points
                
                # Recommandation basée sur la différence
                if difference > 20:
                    recommendation = "URGENT: Optimiser le lineup"
                elif difference > 10:
                    recommendation = "Considérer des changements"
                else:
                    recommendation = "Lineup optimal"
                
                row = [
                    current_date,
                    team['team_name'],
                    bench_points,
                    active_points,
                    difference,
                    "Impact élevé" if difference > 15 else "Impact modéré",
                    recommendation
                ]
                rows.append(row)
            
            worksheet.update('A2', rows)
            
        except Exception as e:
            self.logger.error(f"❌ Erreur création analyse banc: {e}")
    
    def setup_automated_export(self):
        """Configure l'export automatique"""
        self.logger.info("🔄 Configuration de l'export automatique vers Google Sheets")
        
        # Crée les feuilles nécessaires
        self.create_worksheets()
        
        self.logger.info("✅ Export automatique configuré")

def main():
    """Fonction principale pour tester l'intégration Google Sheets"""
    print("🚀 ESPN NBA Google Sheets Integration")
    print("=" * 50)
    
    try:
        # Initialisation
        exporter = GoogleSheetsNBAExporter()
        
        # Configuration
        exporter.setup_automated_export()
        
        print("✅ Intégration Google Sheets configurée avec succès!")
        print("📊 Feuilles de calcul créées:")
        print("   - Données Quotidiennes")
        print("   - Résumé Équipes")
        print("   - Joueurs Détaillés")
        print("   - Transactions")
        print("   - Agents Libres")
        print("   - Blessures")
        print("   - Analyse Banc")
        print("   - Insights IA")
        
    except Exception as e:
        print(f"❌ Erreur configuration Google Sheets: {e}")
        print("💡 Assurez-vous d'avoir configuré le fichier credentials.json")

if __name__ == "__main__":
    main()
