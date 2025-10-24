"""
Script principal pour la collecte des données
"""
from src.collectors.data_collector import ESPNDataCollector
from config.settings import LEAGUE_ID, YEAR, DATA_PATHS
import logging
import os

def setup_logging():
    """Configure le logging"""
    if not os.path.exists(DATA_PATHS["LOGS"]):
        os.makedirs(DATA_PATHS["LOGS"])
    
    logging.basicConfig(
        filename=os.path.join(DATA_PATHS["LOGS"], "collection.log"),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def main():
    # Configuration du logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Création des dossiers nécessaires
        for path in DATA_PATHS.values():
            os.makedirs(path, exist_ok=True)
        
        # Initialisation du collecteur
        collector = ESPNDataCollector(LEAGUE_ID, YEAR)
        
        # Collecte des données
        logger.info("Début de la collecte des données")
        
        standings_df = collector.collect_daily_standings()
        logger.info("Classements collectés")
        
        rosters_df = collector.collect_roster_data()
        logger.info("Rosters collectés")
        
        fa_df = collector.collect_free_agents()
        logger.info("Agents libres collectés")
        
        logger.info("Collecte terminée avec succès")
        
    except Exception as e:
        logger.error(f"Erreur lors de la collecte : {str(e)}")
        raise

if __name__ == "__main__":
    main()
