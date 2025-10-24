#!/usr/bin/env python3
"""
Script de lancement quotidien pour la collecte ESPN NBA
Point d'entrée simple pour la collecte quotidienne des données
"""

import sys
import os
from datetime import datetime
import logging

# Ajouter le répertoire courant au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from espn_nba_advanced_analyzer import ESPNNBAAdvancedAnalyzer

def setup_logging():
    """Configure le logging pour le script quotidien"""
    log_filename = f"daily_collection_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def main():
    """Fonction principale pour la collecte quotidienne"""
    logger = setup_logging()
    
    print("🚀 ESPN NBA Daily Data Collection")
    print("=" * 50)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Configuration
    LEAGUE_ID = 1557635339
    SEASON = 2026
    MY_TEAM_NAME = "Neon Cobras 99"
    
    try:
        # Initialisation
        logger.info("🔧 Initialisation de l'analyseur")
        analyzer = ESPNNBAAdvancedAnalyzer(LEAGUE_ID, SEASON, MY_TEAM_NAME)
        
        # Collecte des données
        logger.info("📊 Début de la collecte des données")
        snapshot = analyzer.collect_daily_data()
        
        # Sauvegarde
        logger.info("💾 Sauvegarde des données")
        analyzer.save_daily_snapshot(snapshot)
        
        # Rapport
        logger.info("📋 Génération du rapport")
        analyzer.generate_daily_report(snapshot)
        
        # Export Google Sheets (si configuré)
        try:
            from google_sheets_integration import GoogleSheetsNBAExporter
            exporter = GoogleSheetsNBAExporter()
            export_data = analyzer.export_to_google_sheets_format(snapshot)
            exporter.export_daily_snapshot(export_data)
            logger.info("📊 Export Google Sheets réussi")
        except Exception as e:
            logger.warning(f"⚠️ Export Google Sheets échoué: {e}")
        
        # Résumé final
        print("\n" + "="*50)
        print("✅ COLLECTE QUOTIDIENNE TERMINÉE")
        print("="*50)
        print(f"📊 {len(snapshot.teams)} équipes analysées")
        print(f"👥 {sum(len(team.roster) for team in snapshot.teams)} joueurs trackés")
        print(f"🔄 {len(snapshot.transactions)} transactions récupérées")
        print(f"🏥 {len(snapshot.injuries)} blessures trackées")
        print(f"🤖 {len(snapshot.ai_recommendations)} recommandations IA")
        
        # Trouve mon équipe pour le résumé
        my_team = None
        for team in snapshot.teams:
            if team.is_my_team:
                my_team = team
                break
        
        if my_team:
            print(f"\n🏀 MON ÉQUIPE: {my_team.team_name}")
            print(f"📈 Rang: {my_team.ranking}")
            print(f"⚡ Points totaux: {my_team.total_stats.get('points', 0):.1f}")
            print(f"🪑 Points banc: {my_team.bench_stats.get('points', 0):.1f}")
            
            # Alerte si points perdus
            bench_points = my_team.bench_stats.get('points', 0)
            if bench_points > 15:
                print(f"⚠️  ALERTE: {bench_points:.1f} points perdus sur le banc!")
        
        print(f"\n📁 Fichiers générés:")
        print(f"   - espn_nba_daily_{snapshot.date}.json")
        print(f"   - daily_collection_{datetime.now().strftime('%Y%m%d')}.log")
        
        logger.info("✅ Collecte quotidienne terminée avec succès")
        
    except Exception as e:
        logger.error(f"❌ Erreur dans la collecte quotidienne: {e}")
        print(f"\n❌ ERREUR: {e}")
        print("🔍 Consultez les logs pour plus de détails")
        sys.exit(1)

if __name__ == "__main__":
    main()
