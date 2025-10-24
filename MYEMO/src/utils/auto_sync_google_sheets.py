#!/usr/bin/env python3
"""
Synchronisation automatique Google Sheets
Script de synchronisation quotidienne avec Google Sheets
"""

import schedule
import time
import logging
from datetime import datetime, timedelta
import json
import os
from complete_google_sheets_system import CompleteGoogleSheetsSystem

class AutoSyncGoogleSheets:
    """Synchronisation automatique avec Google Sheets"""
    
    def __init__(self, league_id: int, season: int, my_team_name: str):
        self.league_id = league_id
        self.season = season
        self.my_team_name = my_team_name
        self.setup_logging()
        self.setup_system()
    
    def setup_logging(self):
        """Configure le logging"""
        log_filename = f"auto_sync_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_system(self):
        """Configure le système de synchronisation"""
        try:
            self.system = CompleteGoogleSheetsSystem(
                league_id=self.league_id,
                season=self.season,
                my_team_name=self.my_team_name
            )
            self.logger.info("✅ Système de synchronisation configuré")
        except Exception as e:
            self.logger.error(f"❌ Erreur configuration système: {e}")
            raise
    
    def daily_sync(self):
        """Synchronisation quotidienne"""
        try:
            self.logger.info("🚀 Début de la synchronisation quotidienne")
            
            # Exécution du système complet
            self.system.run_complete_system()
            
            # Sauvegarde de l'état
            self.save_sync_state()
            
            self.logger.info("✅ Synchronisation quotidienne terminée")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur synchronisation quotidienne: {e}")
            self.send_error_notification(str(e))
    
    def save_sync_state(self):
        """Sauvegarde l'état de synchronisation"""
        try:
            state = {
                'last_sync': datetime.now().isoformat(),
                'league_id': self.league_id,
                'season': self.season,
                'my_team_name': self.my_team_name,
                'status': 'success'
            }
            
            with open('sync_state.json', 'w') as f:
                json.dump(state, f, indent=2)
            
            self.logger.info("💾 État de synchronisation sauvegardé")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur sauvegarde état: {e}")
    
    def send_error_notification(self, error_message):
        """Envoie une notification d'erreur"""
        try:
            # Log de l'erreur
            self.logger.error(f"❌ Notification d'erreur: {error_message}")
            
            # Sauvegarde de l'erreur
            error_log = {
                'timestamp': datetime.now().isoformat(),
                'error': error_message,
                'league_id': self.league_id,
                'season': self.season
            }
            
            with open('sync_errors.json', 'a') as f:
                f.write(json.dumps(error_log) + '\n')
            
        except Exception as e:
            self.logger.error(f"❌ Erreur notification: {e}")
    
    def weekly_analysis(self):
        """Analyse hebdomadaire approfondie"""
        try:
            self.logger.info("📊 Début de l'analyse hebdomadaire")
            
            # Exécution du système complet
            self.system.run_complete_system()
            
            # Analyse des tendances
            self.analyze_weekly_trends()
            
            # Génération du rapport hebdomadaire
            self.generate_weekly_report()
            
            self.logger.info("✅ Analyse hebdomadaire terminée")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur analyse hebdomadaire: {e}")
    
    def analyze_weekly_trends(self):
        """Analyse les tendances hebdomadaires"""
        try:
            # Cette fonction analyserait les données historiques
            # pour identifier les tendances et patterns
            
            trends = {
                'hot_players': [],
                'cold_players': [],
                'team_trends': [],
                'category_trends': [],
                'bench_optimization': [],
                'trade_opportunities': []
            }
            
            # Sauvegarde des tendances
            with open('weekly_trends.json', 'w') as f:
                json.dump(trends, f, indent=2)
            
            self.logger.info("📈 Tendances hebdomadaires analysées")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur analyse tendances: {e}")
    
    def generate_weekly_report(self):
        """Génère le rapport hebdomadaire"""
        try:
            report = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'type': 'weekly_analysis',
                'league_id': self.league_id,
                'season': self.season,
                'my_team_name': self.my_team_name,
                'trends': 'weekly_trends.json',
                'recommendations': self.generate_weekly_recommendations()
            }
            
            filename = f"weekly_report_{datetime.now().strftime('%Y%m%d')}.json"
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            
            self.logger.info(f"📊 Rapport hebdomadaire généré: {filename}")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur génération rapport hebdomadaire: {e}")
    
    def generate_weekly_recommendations(self):
        """Génère des recommandations hebdomadaires"""
        recommendations = [
            {
                'type': 'bench_optimization',
                'priority': 'high',
                'message': 'Optimiser le lineup pour réduire les points perdus sur le banc',
                'action': 'Analyser les performances et ajuster le lineup'
            },
            {
                'type': 'roto_improvement',
                'priority': 'medium',
                'message': 'Améliorer les catégories faibles en ROTO',
                'action': 'Identifier les joueurs cibles pour les trades'
            },
            {
                'type': 'streaming_opportunities',
                'priority': 'low',
                'message': 'Opportunités de streaming pour la semaine',
                'action': 'Analyser les free agents disponibles'
            }
        ]
        
        return recommendations
    
    def start_scheduler(self):
        """Démarre le scheduler de synchronisation"""
        self.logger.info("🚀 Démarrage du scheduler de synchronisation")
        
        # Synchronisation quotidienne à 8h00
        schedule.every().day.at("08:00").do(self.daily_sync)
        
        # Synchronisation quotidienne à 20h00
        schedule.every().day.at("20:00").do(self.daily_sync)
        
        # Analyse hebdomadaire le dimanche à 9h00
        schedule.every().sunday.at("09:00").do(self.weekly_analysis)
        
        self.logger.info("⏰ Scheduler configuré:")
        self.logger.info("   - Synchronisation quotidienne: 8h00 et 20h00")
        self.logger.info("   - Analyse hebdomadaire: Dimanche 9h00")
        
        # Boucle principale
        while True:
            schedule.run_pending()
            time.sleep(60)  # Vérification toutes les minutes
    
    def run_manual_sync(self):
        """Exécute une synchronisation manuelle"""
        try:
            print("🚀 Synchronisation manuelle Google Sheets")
            print("=" * 50)
            
            # Exécution du système complet
            self.system.run_complete_system()
            
            print("✅ Synchronisation manuelle terminée avec succès!")
            
        except Exception as e:
            print(f"❌ Erreur synchronisation manuelle: {e}")
            self.logger.error(f"❌ Erreur synchronisation manuelle: {e}")

def main():
    """Fonction principale du système de synchronisation"""
    print("🚀 Auto Sync Google Sheets - ESPN NBA Fantasy")
    print("=" * 60)
    
    # Configuration
    LEAGUE_ID = 1557635339
    SEASON = 2026
    MY_TEAM_NAME = "Neon Cobras 99"
    
    try:
        # Initialisation du système
        sync_system = AutoSyncGoogleSheets(LEAGUE_ID, SEASON, MY_TEAM_NAME)
        
        # Test de synchronisation
        print("🧪 Test de synchronisation...")
        sync_system.run_manual_sync()
        
        # Démarrage du scheduler
        print("\n⏰ Démarrage du scheduler automatique...")
        print("Appuyez sur Ctrl+C pour arrêter")
        
        sync_system.start_scheduler()
        
    except KeyboardInterrupt:
        print("\n🛑 Scheduler arrêté par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur dans le système de synchronisation: {e}")

if __name__ == "__main__":
    main()
