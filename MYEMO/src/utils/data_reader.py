import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

class DataReader:
    def __init__(self, base_path: str = "data"):
        self.base_path = Path(base_path)
        
    def read_latest_standings(self) -> pd.DataFrame:
        """Lit le dernier fichier de standings disponible"""
        standings_dir = self.base_path / "raw" / "standings"
        latest_file = max(standings_dir.glob("standings_*.csv"))
        return pd.read_csv(latest_file)
    
    def read_latest_rosters(self) -> pd.DataFrame:
        """Lit le dernier fichier de rosters disponible"""
        rosters_dir = self.base_path / "raw" / "rosters"
        latest_file = max(rosters_dir.glob("rosters_*.csv"))
        return pd.read_csv(latest_file)
    
    def read_latest_free_agents(self) -> pd.DataFrame:
        """Lit le dernier fichier d'agents libres disponible"""
        fa_dir = self.base_path / "raw" / "free_agents"
        latest_file = max(fa_dir.glob("fa_*.csv"))
        return pd.read_csv(latest_file)
    
    def read_date_range(self, start_date: str, end_date: str, data_type: str) -> pd.DataFrame:
        """Lit les données pour une période spécifique"""
        data_dir = self.base_path / "raw" / data_type
        
        # Conversion des dates
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        # Récupération et concaténation des fichiers
        all_data = []
        for file in data_dir.glob(f"{data_type}_*.csv"):
            file_date = datetime.strptime(file.stem.split("_")[1], "%Y%m%d")
            if start <= file_date <= end:
                df = pd.read_csv(file)
                all_data.append(df)
        
        return pd.concat(all_data) if all_data else pd.DataFrame()

    def get_team_history(self, team_name: str) -> dict:
        """Récupère l'historique complet d'une équipe"""
        standings = self.read_date_range(
            "2025-10-01",  # Début de saison
            datetime.now().strftime("%Y-%m-%d"),
            "standings"
        )
        
        rosters = self.read_date_range(
            "2025-10-01",
            datetime.now().strftime("%Y-%m-%d"),
            "rosters"
        )
        
        team_standings = standings[standings["team_name"] == team_name]
        team_rosters = rosters[rosters["team_name"] == team_name]
        
        return {
            "standings": team_standings,
            "rosters": team_rosters
        }
