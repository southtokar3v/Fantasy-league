from espn_api.basketball import League
import pandas as pd
from datetime import datetime, timedelta
import os
import logging
from typing import Dict, List, Optional
from data_models import GeneralStanding, StatStanding, RosterHistory, PlayerTracking, FreeAgentMarket
from file_manager import FileManager

class DataCollector:
    STATS_CATEGORIES = ['PTS', 'REB', 'AST', 'BLK', 'STL', '3PM', 'FG%', 'FT%']
    MY_TEAM_NAME = "Neon Cobras 99"

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.league = None
        self.prev_day_data = {}
        self.today = datetime.now().strftime('%Y%m%d')
        self.base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
        self.file_manager = FileManager(self.base_path)
        self.setup_logging()
        self.connect_to_espn()
        self.load_previous_data()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def load_previous_data(self):
        """Charge les données précédentes pour calculer les différences"""
        try:
            for stat in self.STATS_CATEGORIES:
                prev_file = os.path.join(self.base_path, f'data/raw/stats/stats_{stat.lower()}_history.csv')
                if os.path.exists(prev_file):
                    df = pd.read_csv(prev_file)
                    # Obtenir les données de la dernière date pour chaque équipe
                    self.prev_day_data[stat] = df.sort_values('date').groupby('team').last().reset_index()
        except Exception as e:
            self.logger.warning(f"Impossible de charger les données précédentes : {str(e)}")
    
    def connect_to_espn(self):
        try:
            self.league = League(league_id=1557635339, year=2026)
            self.logger.info(f"✅ Connexion ESPN réussie: {self.league.settings.name}")
            self.logger.info(f"👥 {len(self.league.teams)} équipes")
        except Exception as e:
            self.logger.error(f"❌ Erreur de connexion ESPN: {str(e)}")
            raise

    def collect_general_standings(self) -> List[GeneralStanding]:
        standings_data = []
        prev_standings = self._load_previous_standings()
        
        for team in self.league.standings():
            total_points = sum(getattr(team, f'stats_{stat.lower()}', 0) for stat in self.STATS_CATEGORIES)
            avg_points = total_points / len(self.STATS_CATEGORIES)
            
            # Calcul de la différence avec la veille
            prev_points = prev_standings.get(team.team_name, {}).get('total_points', total_points)
            diff = total_points - prev_points
            
            standing = GeneralStanding(
                date=self.today,
                team=team.team_name.strip(),
                total_rank=getattr(team, 'standing', 0),
                average_rank=getattr(team, 'rank', 0),
                total_points=total_points,
                average_points=avg_points,
                prev_day_diff=diff,
                important_event=None  # À remplir manuellement ou via analyse
            )
            standings_data.append(standing)
        
        # Sauvegarde en CSV avec historique
        df = pd.DataFrame([vars(s) for s in standings_data])
        self.file_manager.append_or_create(df, 'data/raw/general/standings_history.csv')
        return standings_data

    def collect_stat_standings(self) -> Dict[str, List[StatStanding]]:
        stats_data = {}
        
        for stat in self.STATS_CATEGORIES:
            stat_standings = []
            for team in self.league.standings():
                daily_total = getattr(team, f'stats_{stat.lower()}', 0)
                daily_avg = daily_total / self.league.settings.reg_season_count
                
                # Différence avec la veille
                prev_stat = 0
                if stat in self.prev_day_data and not self.prev_day_data[stat].empty:
                    prev_team_data = self.prev_day_data[stat][
                        self.prev_day_data[stat]['team'] == team.team_name
                    ]
                    if not prev_team_data.empty:
                        prev_stat = prev_team_data.iloc[0]['daily_total']
                
                standing = StatStanding(
                    date=self.today,
                    team=team.team_name.strip(),
                    stat_name=stat,
                    daily_total=daily_total,
                    daily_average=daily_avg,
                    stat_rank=self._calculate_stat_rank(team, stat),
                    prev_day_diff=daily_total - prev_stat
                )
                stat_standings.append(standing)
            
            # Sauvegarde en CSV avec historique pour chaque stat
            df = pd.DataFrame([vars(s) for s in stat_standings])
            self.file_manager.append_or_create(df, f'data/raw/stats/stats_{stat.lower()}_history.csv')
            stats_data[stat] = stat_standings
        
        return stats_data

    def collect_roster_history(self) -> List[RosterHistory]:
        roster_data = []
        
        for team in self.league.teams:
            for player in team.roster:
                # Vérification du statut
                status = 'active'  # Par défaut, on considère le joueur comme actif
                if hasattr(player, 'injured') and player.injured:
                    status = 'IR'
                elif hasattr(player, 'slot_position') and player.slot_position == 'BE':
                    status = 'bench'
                
                # L'origine nécessiterait un suivi historique, on met 'Unknown' par défaut
                roster = RosterHistory(
                    date=self.today,
                    team=team.team_name.strip(),
                    player=player.name,
                    status=status,
                    origin='Unknown',  # À remplir via analyse historique
                    arrival_date=self.today,  # Date par défaut
                    annotation=None
                )
                roster_data.append(roster)
        
        # Sauvegarde en CSV avec historique
        df = pd.DataFrame([vars(r) for r in roster_data])
        self.file_manager.append_or_create(df, 'data/raw/rosters/roster_history.csv')
        return roster_data

    def collect_my_team_tracking(self) -> List[PlayerTracking]:
        tracking_data = []
        
        # Trouve mon équipe
        my_team = next((team for team in self.league.teams 
                       if team.team_name.strip() == self.MY_TEAM_NAME), None)
        
        if not my_team:
            self.logger.error(f"Équipe {self.MY_TEAM_NAME} non trouvée!")
            return tracking_data
        
        for player in my_team.roster:
            # Informations NBA à compléter via API NBA ou autre source
            tracking = PlayerTracking(
                date=self.today,
                player=player.name,
                fantasy_team=self.MY_TEAM_NAME,
                nba_opponent=None,  # À compléter via API NBA
                points=getattr(player, 'stats_pts', 0),
                rebounds=getattr(player, 'stats_reb', 0),
                assists=getattr(player, 'stats_ast', 0),
                blocks=getattr(player, 'stats_blk', 0),
                threes_made=getattr(player, 'stats_3pm', 0),
                status='IR' if (hasattr(player, 'injured') and player.injured) else ('bench' if hasattr(player, 'slot_position') and player.slot_position == 'BE' else 'active'),
                game_played=True,  # À vérifier via API NBA
                injury_status=player.injured if hasattr(player, 'injured') else None,
                next_game=None,  # À compléter via API NBA
                back_to_back=False  # À compléter via API NBA
            )
            tracking_data.append(tracking)
        
        # Sauvegarde en CSV avec historique
        df = pd.DataFrame([vars(t) for t in tracking_data])
        self.file_manager.append_or_create(df, 'data/raw/tracking/my_team_history.csv')
        return tracking_data

    def collect_free_agents(self) -> List[FreeAgentMarket]:
        fa_data = []
        free_agents = self.league.free_agents()
        
        for player in free_agents:
            # Calcul des statistiques sur différentes périodes
            last_week_stats = {
                'pts': getattr(player, 'stats_pts', 0),
                'reb': getattr(player, 'stats_reb', 0),
                'ast': getattr(player, 'stats_ast', 0),
                'blk': getattr(player, 'stats_blk', 0),
                '3pm': getattr(player, 'stats_3pm', 0),
            }
            
            fa = FreeAgentMarket(
                date=self.today,
                player=player.name,
                nba_team=getattr(player, 'proTeam', 'Unknown'),
                last_week_stats=last_week_stats,
                rolling_14d_stats=last_week_stats.copy(),  # À améliorer avec historique
                rolling_30d_stats=last_week_stats.copy(),  # À améliorer avec historique
                roster_percentage=getattr(player, 'percent_owned', 0),
                start_percentage=getattr(player, 'percent_started', 0),
                team_fit_score=None,  # À calculer en fonction des besoins de l'équipe
                annotation=None
            )
            fa_data.append(fa)
        
        # Sauvegarde en CSV
        df = pd.DataFrame([{
            **vars(fa),
            **{'last_week_' + k: v for k, v in fa.last_week_stats.items()},
            **{'rolling_14d_' + k: v for k, v in fa.rolling_14d_stats.items()},
            **{'rolling_30d_' + k: v for k, v in fa.rolling_30d_stats.items()}
        } for fa in fa_data])
        
        # Supprime les colonnes dictionnaire et sauvegarde avec historique
        df = df.drop(columns=['last_week_stats', 'rolling_14d_stats', 'rolling_30d_stats'])
        self.file_manager.append_or_create(df, 'data/raw/free_agents/fa_market_history.csv')
        return fa_data

    def _load_previous_standings(self) -> Dict[str, Dict]:
        prev_standings = {}
        try:
            prev_file = os.path.join(self.base_path, 'data/raw/general/standings_history.csv')
            if os.path.exists(prev_file):
                df = pd.read_csv(prev_file)
                # Obtenir les données de la dernière date pour chaque équipe
                latest_data = df.sort_values('date').groupby('team').last()
                for team_name, row in latest_data.iterrows():
                    prev_standings[team_name] = row.to_dict()
        except Exception as e:
            self.logger.warning(f"Impossible de charger les classements précédents : {str(e)}")
        return prev_standings

    def _calculate_stat_rank(self, team: object, stat: str) -> int:
        """Calcule le rang d'une équipe pour une statistique donnée"""
        all_teams = self.league.standings()
        sorted_teams = sorted(
            all_teams,
            key=lambda x: getattr(x, f'stats_{stat.lower()}', 0),
            reverse=True
        )
        return next((i + 1 for i, t in enumerate(sorted_teams) if t.team_id == team.team_id), 0)

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
        
        print("\n✨ Collecte terminée avec succès ! Les données sont dans data/raw/")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la collecte : {str(e)}")
        logging.error(f"Erreur détaillée : {str(e)}")

if __name__ == "__main__":
    main()
