from typing import Dict, List
import pandas as pd
from datetime import datetime
import logging
import os
from espn_api.basketball import League

class ESPNDataCollectorError(Exception):
    """Classe personnalisée pour les erreurs de collecte"""
    def __init__(self, message: str, error_code: str, source: str):
        self.error_code = error_code
        self.source = source
        super().__init__(f"[{error_code}] {source}: {message}")

class ESPNDataCollector:
    ERROR_CODES = {
        "CONN": "Erreur de connexion ESPN",
        "DATA": "Erreur de données",
        "AUTH": "Erreur d'authentification",
        "PARSE": "Erreur de parsing",
        "API": "Erreur API ESPN"
    }

    def __init__(self, league_id: str, year: int):
        self.league_id = league_id
        self.year = year
        try:
            self.league = League(league_id=league_id, year=year)
        except Exception as e:
            raise ESPNDataCollectorError(str(e), "CONN", "League Initialization")
        self.setup_logger()
        
    def setup_logger(self):
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        logging.basicConfig(
            filename=os.path.join(log_dir, f"espn_collector_{datetime.now().strftime('%Y%m%d')}.log"),
            level=logging.INFO,
            format="%(asctime)s - [%(error_code)s] - %(levelname)s - %(source)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)
        
    def log_error(self, error: Exception, error_code: str, source: str):
        """Log une erreur avec son code et sa source"""
        extra = {
            "error_code": error_code,
            "source": source
        }
        self.logger.error(str(error), extra=extra)

    def _get_current_date(self) -> str:
        """Retourne la date courante au format YYYY-MM-DD"""
        return datetime.now().strftime("%Y-%m-%d")

    def _extract_stats(self, stats: Dict, stats_list: List[str]) -> Dict:
        """Extrait les statistiques spécifiées"""
        return {stat: stats.get(stat, 0) for stat in stats_list}

    def _ensure_data_dirs(self):
        """Crée les répertoires de données s'ils n'existent pas"""
        base_path = "data/raw"
        dirs = ["standings", "rosters", "free_agents"]
        for dir_name in dirs:
            os.makedirs(f"{base_path}/{dir_name}", exist_ok=True)

    def _save_data(self, df: pd.DataFrame, data_type: str):
        """Sauvegarde les données dans un fichier CSV"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/raw/{data_type}/{data_type}_{timestamp}.csv"
        df.to_csv(filename, index=False)
        self.logger.info(f"Données sauvegardées dans {filename}")

    def collect_daily_standings(self) -> pd.DataFrame:
        """Collecte le classement quotidien et les statistiques"""
        try:
            self._ensure_data_dirs()
            STATS_CATEGORIES = ["FG%", "FT%", "3PM", "REB", "AST", "STL", "BLK", "PTS"]
            current_date = self._get_current_date()
            
            data = [{
                "date": current_date,
                "team_name": team.team_name,
                "total_rank": team.standing,
                "total_points": team.points_for,
                **self._extract_stats(team.stats, STATS_CATEGORIES)
            } for team in self.league.teams]
            
            df = pd.DataFrame(data)
            self._save_data(df, "standings")
            self.logger.info(f"Collecte réussie: {len(data)} équipes traitées")
            return df
        except Exception as e:
            self.log_error(e, "DATA", "Standings Collection")
            raise ESPNDataCollectorError(str(e), "DATA", "Standings Collection")
    
    def _process_player_data(self, player, team_name: str = None) -> Dict:
        """Traite les données d'un joueur"""
        # Extraction des statistiques de base pour chaque période
        periods = ["2026_total", "2026_last_30", "2026_last_15", "2026_last_7"]
        
        stats_data = {}
        for period in periods:
            if hasattr(player, "stats") and period in player.stats:
                period_stats = player.stats[period]["avg"]
                stats_data[period] = {
                    "PTS": period_stats.get("PTS", 0),
                    "BLK": period_stats.get("BLK", 0),
                    "STL": period_stats.get("STL", 0),
                    "AST": period_stats.get("AST", 0),
                    "REB": period_stats.get("REB", 0),
                    "TO": period_stats.get("TO", 0),
                    "3PM": period_stats.get("3PM", 0),
                    "FG%": period_stats.get("FG%", 0),
                    "FT%": period_stats.get("FT%", 0)
                }
            else:
                stats_data[period] = {}

        # Extraction des moyennes sur 9 catégories
        nine_cat_stats = player.nine_cat_averages if hasattr(player, "nine_cat_averages") else {}
        
        return {
            "date": self._get_current_date(),
            "player_name": player.name,
            "team_name": team_name,
            "position": player.position,
            "proTeam": player.proTeam,
            "injured": player.injured,
            "injury_status": player.injuryStatus,
            "total_stats": stats_data["2026_total"],
            "last_30_stats": stats_data["2026_last_30"],
            "last_15_stats": stats_data["2026_last_15"],
            "last_7_stats": stats_data["2026_last_7"],
            "nine_cat_averages": nine_cat_stats
        }

    def collect_roster_data(self) -> pd.DataFrame:
        """Collecte les données des rosters"""
        try:
            self._ensure_data_dirs()
            data = []
            for team in self.league.teams:
                roster_data = [self._process_player_data(player, team.team_name) 
                             for player in team.roster]
                data.extend(roster_data)
                
            df = pd.DataFrame(data)
            self._save_data(df, "rosters")
            self.logger.info(f"Collecte roster réussie: {len(data)} joueurs traités")
            return df
        except Exception as e:
            self.log_error(e, "DATA", "Roster Collection")
            raise ESPNDataCollectorError(str(e), "DATA", "Roster Collection")

    def collect_free_agents(self) -> pd.DataFrame:
        """Collecte les données des agents libres"""
        try:
            self._ensure_data_dirs()
            free_agents = self.league.free_agents()
            data = [self._process_player_data(player) for player in free_agents]
            
            df = pd.DataFrame(data)
            self._save_data(df, "free_agents")
            self.logger.info(f"Collecte FA réussie: {len(data)} agents libres traités")
            return df
        except Exception as e:
            self.log_error(e, "DATA", "Free Agents Collection")
            raise ESPNDataCollectorError(str(e), "DATA", "Free Agents Collection")
