import schedule
import time
from datetime import datetime, timedelta
import logging
from pathlib import Path
from src.collectors.data_collector import ESPNDataCollector
from config.settings import LEAGUE_ID, YEAR

class RealTimeCollector:
    def __init__(self):
        self.collector = ESPNDataCollector(LEAGUE_ID, YEAR)
        self.setup_logger()
        
    def setup_logger(self):
        log_dir = Path("logs/realtime")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            filename=log_dir / f"realtime_collector_{datetime.now().strftime('%Y%m%d')}.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

    def collect_all_data(self):
        """Collecte toutes les données en une fois"""
        try:
            current_time = datetime.now().strftime("%H:%M:%S")
            self.logger.info(f"Début de la collecte à {current_time}")

            # Collecte des classements
            standings_df = self.collector.collect_daily_standings()
            standings_df.to_csv(f"data/raw/standings/standings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", index=False)

            # Collecte des rosters
            rosters_df = self.collector.collect_roster_data()
            rosters_df.to_csv(f"data/raw/rosters/rosters_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", index=False)

            # Collecte des agents libres
            fa_df = self.collector.collect_free_agents()
            fa_df.to_csv(f"data/raw/free_agents/fa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", index=False)

            self.logger.info("Collecte terminée avec succès")
        except Exception as e:
            self.logger.error(f"Erreur lors de la collecte: {str(e)}")

    def start_collection(self, interval_minutes: int = 30):
        """Démarre la collecte en temps réel avec un intervalle spécifié"""
        self.logger.info(f"Démarrage de la collecte en temps réel (intervalle: {interval_minutes} minutes)")
        
        # Première collecte immédiate
        self.collect_all_data()
        
        # Planification des collectes suivantes
        schedule.every(interval_minutes).minutes.do(self.collect_all_data)
        
        # Boucle principale
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Vérifie toutes les minutes
            except KeyboardInterrupt:
                self.logger.info("Arrêt manuel de la collecte")
                break
            except Exception as e:
                self.logger.error(f"Erreur dans la boucle principale: {str(e)}")
                time.sleep(300)  # Attend 5 minutes en cas d'erreur
