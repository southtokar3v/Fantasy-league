import pandas as pd
from datetime import datetime
import logging
from pathlib import Path

class DataProcessor:
    def __init__(self):
        self.setup_logger()
        self.raw_data_path = Path("/Users/southtokar3v/Desktop/MYEMO/data/raw")
        self.processed_data_path = Path("/Users/southtokar3v/Desktop/MYEMO/data/processed")
        
    def setup_logger(self):
        logging.basicConfig(
            filename=f'logs/data_processor_{datetime.now().strftime("%Y%m%d")}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def process_standings(self, df: pd.DataFrame) -> pd.DataFrame:
        """Traite les données de classement"""
        try:
            # Ajoute les colonnes calculées
            df['average_rank'] = df['total_points'] / df.groupby('date')['total_points'].transform('count')
            df['daily_change'] = df.groupby('team_name')['total_rank'].diff()
            return df
        except Exception as e:
            self.logger.error(f"Erreur lors du traitement des standings: {str(e)}")
            return df
    
    def process_roster_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Traite les données des rosters"""
        try:
            # Normalise les statistiques
            stats_columns = ['FG%', 'FT%', '3PM', 'REB', 'AST', 'STL', 'BLK', 'PTS']
            for col in stats_columns:
                if col in df.columns:
                    df[f'{col}_normalized'] = (df[col] - df[col].mean()) / df[col].std()
            return df
        except Exception as e:
            self.logger.error(f"Erreur lors du traitement des rosters: {str(e)}")
            return df
    
    def process_free_agents(self, df: pd.DataFrame) -> pd.DataFrame:
        """Traite les données des agents libres"""
        try:
            # Calcule les tendances
            df['trend'] = df.groupby('player_name')['stats_7d'].diff()
            # Ajoute un score d'opportunité
            stats_weights = {
                'PTS': 1.0, 'REB': 0.8, 'AST': 0.8,
                'STL': 0.6, 'BLK': 0.6, '3PM': 0.4
            }
            df['opportunity_score'] = sum(df[stat] * weight for stat, weight in stats_weights.items())
            return df
        except Exception as e:
            self.logger.error(f"Erreur lors du traitement des agents libres: {str(e)}")
            return df

    def save_processed_data(self, df: pd.DataFrame, file_name: str):
        """Sauvegarde les données traitées"""
        try:
            output_path = self.processed_data_path / f"{file_name}_{datetime.now().strftime('%Y%m%d')}.csv"
            df.to_csv(output_path, index=False)
            self.logger.info(f"Données sauvegardées dans {output_path}")
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde des données: {str(e)}")
