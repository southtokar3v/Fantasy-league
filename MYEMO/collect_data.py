from src.collectors.collect_data import DataCollector

def main():
    # Initialiser le collecteur
    collector = DataCollector()
    
    print("🚀 Début de la collecte des données...")
    
    try:
        # 1. Classement général
        print("\n1. Collecte du classement général...")
        general_standings = collector.collect_general_standings()
        print("✅ Classement général sauvegardé")
        
        # 2. Classement par statistique
        print("\n2. Collecte des classements par statistique...")
        stats_standings = collector.collect_stat_standings()
        print("✅ Classements par statistique sauvegardés")
        
        # 3. Historique des rosters
        print("\n3. Collecte de l'historique des rosters...")
        roster_history = collector.collect_roster_history()
        print("✅ Historique des rosters sauvegardé")
        
        # 4. Suivi de mon équipe
        print("\n4. Collecte du suivi de votre équipe...")
        team_tracking = collector.collect_my_team_tracking()
        print("✅ Suivi de votre équipe sauvegardé")
        
        # 5. Marché des agents libres
        print("\n5. Collecte des agents libres...")
        free_agents = collector.collect_free_agents()
        print("✅ Données des agents libres sauvegardées")
        
        # 6. Statistiques quotidiennes des joueurs
        print("\n6. Collecte des statistiques quotidiennes des joueurs...")
        daily_stats = collector.collect_daily_player_stats()
        print("✅ Statistiques quotidiennes des joueurs sauvegardées")
        
        print("\n✨ Collecte terminée avec succès ! Les données sont dans data/raw/")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la collecte : {str(e)}")
        raise

if __name__ == "__main__":
    main()
