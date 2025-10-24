from datetime import datetime
import logging
from pathlib import Path
from src.collectors.collect_data import DataCollector
from src.processors.data_processor import DataProcessor

def main():
    # Configuration
    LEAGUE_ID = "1557635339"
    YEAR = 2026
    
    # Setup logging
    logging.basicConfig(
        filename=f'logs/main_{datetime.now().strftime("%Y%m%d")}.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    try:
        # Initialisation du collecteur
        collector = DataCollector()
        processor = DataProcessor()
        
        # Collecte des données
        logger.info("Début de la collecte des données...")
        
        # 1. Classement général
        general_standings = collector.collect_general_standings()
        processor.process_general_standings(general_standings)
        
        # 2. Classements par statistique
        stats_standings = collector.collect_stat_standings()
        processor.process_stat_standings(stats_standings)
        
        # 3. Historique des rosters
        roster_history = collector.collect_roster_history()
        processor.process_roster_history(roster_history)
        
        # 4. Suivi de l'équipe
        team_tracking = collector.collect_my_team_tracking()
        processor.process_team_tracking(team_tracking)
        
        # 5. Agents libres
        free_agents = collector.collect_free_agents()
        processor.process_free_agents(free_agents)
        
        logger.info("Collecte et traitement des données terminés avec succès")
        
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution: {str(e)}")

if __name__ == "__main__":
    main()
