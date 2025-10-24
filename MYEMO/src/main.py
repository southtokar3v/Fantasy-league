from datetime import datetime
import logging
from pathlib import Path
from scripts.collectors.data_collector import ESPNDataCollector
from scripts.processors.data_processor import DataProcessor

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
        # Initialisation des collecteurs et processeurs
        collector = ESPNDataCollector(LEAGUE_ID, YEAR)
        processor = DataProcessor()
        
        # Collecte des données
        logger.info("Début de la collecte des données...")
        
        # Standings
        standings_df = collector.collect_daily_standings()
        processed_standings = processor.process_standings(standings_df)
        processor.save_processed_data(processed_standings, "standings")
        
        # Rosters
        roster_df = collector.collect_roster_data()
        processed_rosters = processor.process_roster_data(roster_df)
        processor.save_processed_data(processed_rosters, "rosters")
        
        # Free Agents
        fa_df = collector.collect_free_agents()
        processed_fa = processor.process_free_agents(fa_df)
        processor.save_processed_data(processed_fa, "free_agents")
        
        logger.info("Collecte et traitement des données terminés avec succès")
        
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution: {str(e)}")

if __name__ == "__main__":
    main()
