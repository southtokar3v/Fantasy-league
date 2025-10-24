import os
import pandas as pd
from datetime import datetime

class FileManager:
    def __init__(self, base_path: str):
        self.base_path = base_path

    def append_or_create(self, df: pd.DataFrame, file_path: str) -> None:
        """Ajoute les données au fichier existant ou crée un nouveau fichier si nécessaire."""
        full_path = os.path.join(self.base_path, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        if os.path.exists(full_path):
            # Charger les données existantes
            existing_df = pd.read_csv(full_path)
            
            # Combiner avec les nouvelles données
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            
            # Supprimer les doublons potentiels basés sur la date et l'identifiant unique
            if 'date' in combined_df.columns:
                # Pour les classements d'équipe
                if 'team' in combined_df.columns:
                    combined_df = combined_df.drop_duplicates(subset=['date', 'team'], keep='last')
                # Pour les données de joueurs
                elif 'player' in combined_df.columns:
                    combined_df = combined_df.drop_duplicates(subset=['date', 'player'], keep='last')
            
            # Sauvegarder le fichier mis à jour
            combined_df.to_csv(full_path, index=False)
        else:
            # Créer un nouveau fichier
            df.to_csv(full_path, index=False)
