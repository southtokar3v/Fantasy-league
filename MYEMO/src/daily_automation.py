#!/usr/bin/env python3
"""
Automatisation Quotidienne - Version Locale
Collecte automatique des données ESPN
"""

import schedule
import time
import os
import logging
from datetime import datetime
from collectors.collect_data import main as collect_data

def daily_collection():
    """Collecte quotidienne automatique"""
    print(f"\n🔄 Collecte automatique - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Lancement de la collecte
        collect_data()
        print("✅ Collecte automatique terminée")
        
    except Exception as e:
        print(f"❌ Erreur collecte automatique : {e}")

def setup_scheduler():
    """Configure le scheduler quotidien"""
    print("⏰ Configuration de l'automatisation quotidienne")
    
    # Collecte à 8h00
    schedule.every().day.at("08:00").do(daily_collection)
    
    # Collecte à 20h00
    schedule.every().day.at("20:00").do(daily_collection)
    
    print("✅ Scheduler configuré :")
    print("   - 8h00 : Collecte matinale")
    print("   - 20h00 : Collecte vespérale")
    print("\n🔄 Démarrage du scheduler...")
    print("Appuyez sur Ctrl+C pour arrêter")
    
    # Boucle principale
    while True:
        schedule.run_pending()
        time.sleep(60)  # Vérification toutes les minutes

def main():
    """Fonction principale"""
    print("🔄 ESPN NBA Fantasy - Automatisation Quotidienne")
    print("=" * 60)
    
    try:
        # Test initial
        print("🧪 Test initial...")
        collect_data()
        
        # Configuration du scheduler
        setup_scheduler()
        
    except KeyboardInterrupt:
        print("\n🛑 Scheduler arrêté par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    main()
