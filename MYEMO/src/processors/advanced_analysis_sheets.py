#!/usr/bin/env python3
"""
Feuilles d'analyse avancée pour Google Sheets
Système complet d'analyse avec formules, graphiques et alertes
"""

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Any
import numpy as np

class AdvancedAnalysisSheets:
    """Créateur de feuilles d'analyse avancée pour Google Sheets"""
    
    def __init__(self, spreadsheet):
        self.spreadsheet = spreadsheet
        self.setup_logging()
    
    def setup_logging(self):
        """Configure le logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def create_my_team_analysis(self):
        """Crée la feuille d'analyse détaillée de mon équipe"""
        try:
            # Vérifie si la feuille existe
            try:
                worksheet = self.spreadsheet.worksheet('👑 Mon Équipe - Analyse')
            except:
                worksheet = self.spreadsheet.add_worksheet('👑 Mon Équipe - Analyse', rows=2000, cols=30)
            
            # Configuration de la feuille
            self._setup_my_team_headers(worksheet)
            self._setup_my_team_formulas(worksheet)
            self._setup_my_team_formatting(worksheet)
            
            self.logger.info("✅ Feuille 'Mon Équipe - Analyse' configurée")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur création analyse mon équipe: {e}")
    
    def _setup_my_team_headers(self, worksheet):
        """Configure les en-têtes de la feuille mon équipe"""
        # Titre principal
        worksheet.update('A1', [['👑 ANALYSE DÉTAILLÉE - NEON COBRAS 99']])
        
        # Section 1: Résumé quotidien
        worksheet.update('A3', [['📊 RÉSUMÉ QUOTIDIEN']])
        daily_headers = [
            'Date', 'Rang Actuel', 'Points Totaux', 'Points Banc', 'Points Actifs',
            'Différence Banc', 'Impact %', 'Statut', 'Recommandation'
        ]
        worksheet.update('A4:J4', [daily_headers])
        
        # Section 2: Analyse des joueurs
        worksheet.update('A7', [['👥 ANALYSE DES JOUEURS']])
        player_headers = [
            'Joueur', 'Position', 'Statut', 'Points', 'Rebonds', 'Assists',
            'Steals', 'Blocks', 'Efficacité', 'Banc/Actif', 'Tendance',
            'Impact', 'Recommandation', 'Priorité'
        ]
        worksheet.update('A8:N8', [player_headers])
        
        # Section 3: Analyse des catégories ROTO
        worksheet.update('A12', [['📈 ANALYSE CATÉGORIES ROTO']])
        roto_headers = [
            'Catégorie', 'Mon Rang', 'Points', 'Écart Leader', 'Faiblesse',
            'Joueurs Amélioration', 'Actions Suggérées', 'Priorité'
        ]
        worksheet.update('A13:H13', [roto_headers])
        
        # Section 4: Alertes et recommandations
        worksheet.update('A17', [['⚠️ ALERTES ET RECOMMANDATIONS']])
        alert_headers = [
            'Type', 'Priorité', 'Message', 'Action Suggérée', 'Date', 'Statut'
        ]
        worksheet.update('A18:F18', [alert_headers])
    
    def _setup_my_team_formulas(self, worksheet):
        """Configure les formules de calcul pour mon équipe"""
        # Formules pour le résumé quotidien
        formulas = [
            # Impact du banc
            ['=IF(F5>20,"🔴 URGENT","🟡 Modéré")', 'I5'],
            ['=IF(F5>20,"Changer lineup","Surveiller")', 'J5'],
            
            # Analyse des joueurs
            ['=IF(K9="Banc","⚠️ Points perdus","✅ Optimisé")', 'L9'],
            ['=IF(J9>30,"🔥 Hot","❄️ Cold")', 'M9'],
            ['=IF(L9="⚠️ Points perdus","🔴 Haute","🟢 Normale")', 'N9'],
            
            # Analyse ROTO
            ['=IF(C14>6,"🔴 Faible","🟢 Bon")', 'E14'],
            ['=IF(C14>6,"Améliorer cette catégorie","Maintenir")', 'G14'],
            ['=IF(C14>6,"Haute","Normale")', 'H14']
        ]
        
        for formula, cell in formulas:
            worksheet.update(cell, [[formula]])
    
    def _setup_my_team_formatting(self, worksheet):
        """Configure le formatage de la feuille mon équipe"""
        # Formatage des en-têtes
        header_format = {
            "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
            "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}}
        }
        
        # Applique le formatage aux en-têtes
        worksheet.format('A1:Z1', header_format)
        worksheet.format('A4:J4', header_format)
        worksheet.format('A8:N8', header_format)
        worksheet.format('A13:H13', header_format)
        worksheet.format('A18:F18', header_format)
    
    def create_roto_optimization(self):
        """Crée la feuille d'optimisation ROTO"""
        try:
            try:
                worksheet = self.spreadsheet.worksheet('🎯 Optimisation ROTO')
            except:
                worksheet = self.spreadsheet.add_worksheet('🎯 Optimisation ROTO', rows=2000, cols=30)
            
            self._setup_roto_headers(worksheet)
            self._setup_roto_formulas(worksheet)
            self._setup_roto_formatting(worksheet)
            
            self.logger.info("✅ Feuille 'Optimisation ROTO' configurée")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur création optimisation ROTO: {e}")
    
    def _setup_roto_headers(self, worksheet):
        """Configure les en-têtes de la feuille ROTO"""
        # Titre principal
        worksheet.update('A1', [['🎯 OPTIMISATION ROTO - STRATÉGIE COMPLÈTE']])
        
        # Section 1: Classement actuel
        worksheet.update('A3', [['📊 CLASSEMENT ACTUEL']])
        ranking_headers = [
            'Catégorie', 'Mon Rang', 'Points', 'Écart Leader', 'Faiblesse',
            'Joueurs Amélioration', 'Actions Suggérées', 'Priorité'
        ]
        worksheet.update('A4:H4', [ranking_headers])
        
        # Section 2: Analyse des faiblesses
        worksheet.update('A8', [['🔍 ANALYSE DES FAIBLESSES']])
        weakness_headers = [
            'Catégorie Faible', 'Rang Actuel', 'Écart à Améliorer', 'Joueurs Cibles',
            'Trades Possibles', 'Streaming Options', 'Timeline', 'Impact Estimé'
        ]
        worksheet.update('A9:H9', [weakness_headers])
        
        # Section 3: Stratégie d'amélioration
        worksheet.update('A13', [['🚀 STRATÉGIE D\'AMÉLIORATION']])
        strategy_headers = [
            'Action', 'Catégorie', 'Joueur', 'Coût', 'Bénéfice', 'Risque',
            'Timeline', 'Statut'
        ]
        worksheet.update('A14:H14', [strategy_headers])
    
    def _setup_roto_formulas(self, worksheet):
        """Configure les formules pour l'optimisation ROTO"""
        formulas = [
            # Analyse des faiblesses
            ['=IF(C5>6,"🔴 Critique","🟡 Modéré")', 'E5'],
            ['=IF(C5>6,"Améliorer urgent","Surveiller")', 'G5'],
            ['=IF(C5>6,"Haute","Normale")', 'H5'],
            
            # Stratégie d'amélioration
            ['=IF(F15>0.7,"🔥 Fort","🟡 Modéré")', 'G15'],
            ['=IF(F15>0.7,"Exécuter","Évaluer")', 'H15']
        ]
        
        for formula, cell in formulas:
            worksheet.update(cell, [[formula]])
    
    def _setup_roto_formatting(self, worksheet):
        """Configure le formatage de la feuille ROTO"""
        header_format = {
            "backgroundColor": {"red": 0.8, "green": 0.2, "blue": 0.2},
            "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}}
        }
        
        worksheet.format('A1:Z1', header_format)
        worksheet.format('A4:H4', header_format)
        worksheet.format('A9:H9', header_format)
        worksheet.format('A14:H14', header_format)
    
    def create_bench_analysis(self):
        """Crée la feuille d'analyse du banc"""
        try:
            try:
                worksheet = self.spreadsheet.worksheet('🪑 Analyse Banc')
            except:
                worksheet = self.spreadsheet.add_worksheet('🪑 Analyse Banc', rows=2000, cols=30)
            
            self._setup_bench_headers(worksheet)
            self._setup_bench_formulas(worksheet)
            self._setup_bench_formatting(worksheet)
            
            self.logger.info("✅ Feuille 'Analyse Banc' configurée")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur création analyse banc: {e}")
    
    def _setup_bench_headers(self, worksheet):
        """Configure les en-têtes de la feuille banc"""
        # Titre principal
        worksheet.update('A1', [['🪑 ANALYSE DÉTAILLÉE DU BANC - POINTS PERDUS']])
        
        # Section 1: Résumé du banc
        worksheet.update('A3', [['📊 RÉSUMÉ DU BANC']])
        bench_headers = [
            'Date', 'Points Banc', 'Points Actifs', 'Différence', 'Impact %',
            'Recommandation', 'Action Requise', 'Priorité'
        ]
        worksheet.update('A4:H4', [bench_headers])
        
        # Section 2: Joueurs sur le banc
        worksheet.update('A8', [['👥 JOUEURS SUR LE BANC']])
        player_headers = [
            'Joueur', 'Position', 'Points Banc', 'Points Actifs', 'Différence',
            'Impact', 'Recommandation', 'Action'
        ]
        worksheet.update('A9:H9', [player_headers])
        
        # Section 3: Optimisation
        worksheet.update('A13', [['🎯 OPTIMISATION DU LINEUP']])
        optimization_headers = [
            'Joueur à Sortir', 'Joueur à Mettre', 'Gain Estimé', 'Risque',
            'Impact Classement', 'Recommandation', 'Priorité', 'Statut'
        ]
        worksheet.update('A14:H14', [optimization_headers])
    
    def _setup_bench_formulas(self, worksheet):
        """Configure les formules pour l'analyse du banc"""
        formulas = [
            # Impact du banc
            ['=E5/D5*100', 'F5'],
            ['=IF(E5>20,"🔴 URGENT","🟡 Modéré")', 'G5'],
            ['=IF(E5>20,"Changer lineup","Surveiller")', 'H5'],
            
            # Analyse des joueurs
            ['=IF(E10>15,"🔴 Critique","🟡 Modéré")', 'F10'],
            ['=IF(E10>15,"Sortir du banc","Surveiller")', 'G10'],
            
            # Optimisation
            ['=IF(C15>20,"🔥 Fort","🟡 Modéré")', 'F15'],
            ['=IF(C15>20,"Exécuter","Évaluer")', 'G15']
        ]
        
        for formula, cell in formulas:
            worksheet.update(cell, [[formula]])
    
    def _setup_bench_formatting(self, worksheet):
        """Configure le formatage de la feuille banc"""
        header_format = {
            "backgroundColor": {"red": 0.2, "green": 0.6, "blue": 0.2},
            "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}}
        }
        
        worksheet.format('A1:Z1', header_format)
        worksheet.format('A4:H4', header_format)
        worksheet.format('A9:H9', header_format)
        worksheet.format('A14:H14', header_format)
    
    def create_dashboard(self):
        """Crée le dashboard principal"""
        try:
            try:
                worksheet = self.spreadsheet.worksheet('📊 Dashboard Principal')
            except:
                worksheet = self.spreadsheet.add_worksheet('📊 Dashboard Principal', rows=2000, cols=30)
            
            self._setup_dashboard_headers(worksheet)
            self._setup_dashboard_formulas(worksheet)
            self._setup_dashboard_formatting(worksheet)
            
            self.logger.info("✅ Dashboard principal configuré")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur création dashboard: {e}")
    
    def _setup_dashboard_headers(self, worksheet):
        """Configure les en-têtes du dashboard"""
        # Titre principal
        worksheet.update('A1', [['🏀 ESPN NBA FANTASY DASHBOARD - NEON COBRAS 99']])
        
        # Section 1: Résumé quotidien
        worksheet.update('A3', [['📊 RÉSUMÉ QUOTIDIEN']])
        daily_summary = [
            'Date', 'Rang Actuel', 'Points Totaux', 'Points Banc', 'Points Actifs',
            'Différence Banc', 'Impact %', 'Statut', 'Recommandation'
        ]
        worksheet.update('A4:J4', [daily_summary])
        
        # Section 2: Classement actuel
        worksheet.update('A7', [['🏆 CLASSEMENT ACTUEL']])
        ranking_summary = [
            'Rang', 'Équipe', 'Points', 'Rebonds', 'Assists', 'Steals', 'Blocks',
            'FG%', 'FT%', '3PM', 'TO', 'Total'
        ]
        worksheet.update('A8:L8', [ranking_summary])
        
        # Section 3: Alertes importantes
        worksheet.update('A11', [['⚠️ ALERTES IMPORTANTES']])
        alert_headers = [
            'Type', 'Priorité', 'Message', 'Action Suggérée', 'Date', 'Statut'
        ]
        worksheet.update('A12:F12', [alert_headers])
        
        # Section 4: Recommandations IA
        worksheet.update('A16', [['🤖 RECOMMANDATIONS IA']])
        ai_headers = [
            'Recommandation', 'Priorité', 'Impact', 'Action', 'Timeline', 'Statut'
        ]
        worksheet.update('A17:F17', [ai_headers])
        
        # Section 5: Tendances
        worksheet.update('A21', [['📈 TENDANCES']])
        trend_headers = [
            'Joueur', 'Tendance', 'Période', 'Impact', 'Recommandation', 'Priorité'
        ]
        worksheet.update('A22:F22', [trend_headers])
    
    def _setup_dashboard_formulas(self, worksheet):
        """Configure les formules du dashboard"""
        formulas = [
            # Résumé quotidien
            ['=IF(F5>20,"🔴 URGENT","🟡 Modéré")', 'I5'],
            ['=IF(F5>20,"Optimiser lineup","Surveiller")', 'J5'],
            
            # Alertes
            ['=IF(B13="Haute","🔴 Critique","🟡 Modéré")', 'F13'],
            ['=IF(B13="Haute","Action immédiate","Surveiller")', 'G13'],
            
            # Recommandations IA
            ['=IF(B18="Haute","🔥 Fort","🟡 Modéré")', 'C18'],
            ['=IF(B18="Haute","Exécuter","Évaluer")', 'D18']
        ]
        
        for formula, cell in formulas:
            worksheet.update(cell, [[formula]])
    
    def _setup_dashboard_formatting(self, worksheet):
        """Configure le formatage du dashboard"""
        # Titre principal
        title_format = {
            "backgroundColor": {"red": 0.1, "green": 0.3, "blue": 0.7},
            "textFormat": {"bold": True, "fontSize": 16, "foregroundColor": {"red": 1, "green": 1, "blue": 1}}
        }
        
        # En-têtes de sections
        section_format = {
            "backgroundColor": {"red": 0.8, "green": 0.8, "blue": 0.8},
            "textFormat": {"bold": True, "foregroundColor": {"red": 0, "green": 0, "blue": 0}}
        }
        
        worksheet.format('A1:Z1', title_format)
        worksheet.format('A4:J4', section_format)
        worksheet.format('A8:L8', section_format)
        worksheet.format('A12:F12', section_format)
        worksheet.format('A17:F17', section_format)
        worksheet.format('A22:F22', section_format)
    
    def create_all_analysis_sheets(self):
        """Crée toutes les feuilles d'analyse"""
        self.logger.info("🚀 Création de toutes les feuilles d'analyse...")
        
        try:
            self.create_my_team_analysis()
            self.create_roto_optimization()
            self.create_bench_analysis()
            self.create_dashboard()
            
            self.logger.info("✅ Toutes les feuilles d'analyse créées avec succès")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur création feuilles d'analyse: {e}")

def main():
    """Fonction principale pour créer les feuilles d'analyse"""
    print("🚀 Création des feuilles d'analyse avancée")
    print("=" * 50)
    
    try:
        # Configuration Google Sheets
        from google_sheets_integration import GoogleSheetsNBAExporter
        
        exporter = GoogleSheetsNBAExporter()
        spreadsheet = exporter.spreadsheet
        
        # Création des feuilles d'analyse
        analysis_creator = AdvancedAnalysisSheets(spreadsheet)
        analysis_creator.create_all_analysis_sheets()
        
        print("✅ Feuilles d'analyse créées avec succès!")
        print("📊 Feuilles disponibles:")
        print("   - 👑 Mon Équipe - Analyse")
        print("   - 🎯 Optimisation ROTO")
        print("   - 🪑 Analyse Banc")
        print("   - 📊 Dashboard Principal")
        
    except Exception as e:
        print(f"❌ Erreur création feuilles d'analyse: {e}")

if __name__ == "__main__":
    main()
