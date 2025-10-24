from espn_api.basketball import League
import pandas as pd
from datetime import datetime, timedelta
import os
import logging
from typing import Dict, List, Optional
from collectors.data_models import GeneralStanding, StatStanding, RosterHistory, PlayerTracking, FreeAgentMarket
from collectors.file_manager import FileManager

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
            level=logging.DEBUG,  # Changé en DEBUG pour voir plus de détails
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(os.path.join(self.base_path, 'logs', 'espn_collection.log'))
            ]
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
            # Calculer le total pour chaque catégorie
            category_totals = []
            for stat in self.STATS_CATEGORIES:
                stat_total = 0
                for player in team.roster:
                    if hasattr(player, 'nine_cat_averages'):
                        stat_total += float(player.nine_cat_averages.get(stat, 0))
                    elif hasattr(player, 'stats') and '2026_total' in player.stats:
                        stat_total += float(player.stats['2026_total']['avg'].get(stat, 0))
                category_totals.append(stat_total)
            
            total_points = sum(category_totals)
            avg_points = total_points / len(self.STATS_CATEGORIES) if category_totals else 0
            
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
                # Calculer le total des stats pour l'équipe
                daily_total = 0
                total_games = 0
                
                for player in team.roster:
                    if hasattr(player, 'nine_cat_averages'):
                        daily_total += float(player.nine_cat_averages.get(stat, 0))
                        total_games += 1
                    elif hasattr(player, 'stats') and '2026_total' in player.stats:
                        daily_total += float(player.stats['2026_total']['avg'].get(stat, 0))
                        total_games += 1
                
                # Calculer la moyenne (éviter division par 0)
                daily_avg = daily_total / total_games if total_games > 0 else 0
                
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
        previous_rosters = self._load_previous_rosters()
        
        for team in self.league.teams:
            for player in team.roster:
                # Vérification du statut
                status = 'active'  # Par défaut, on considère le joueur comme actif
                if hasattr(player, 'injured') and player.injured:
                    status = 'IR'
                elif hasattr(player, 'slot_position') and player.slot_position == 'BE':
                    status = 'bench'
                
                # Vérifier si le joueur était déjà dans l'équipe
                prev_record = previous_rosters.get((player.name, team.team_name.strip()))
                
                if prev_record is None:
                    # Nouveau joueur dans l'équipe
                    roster = RosterHistory(
                        date=self.today,
                        team=team.team_name.strip(),
                        player=player.name,
                        status=status,
                        origin='FA',  # Par défaut, on suppose qu'il vient des agents libres
                        arrival_date=self.today,
                        annotation=f"Ajouté à l'équipe le {self.today}"
                    )
                else:
                    # Joueur existant, mettre à jour son statut si nécessaire
                    roster = RosterHistory(
                        date=self.today,
                        team=team.team_name.strip(),
                        player=player.name,
                        status=status,
                        origin=prev_record['origin'],
                        arrival_date=prev_record['arrival_date'],
                        annotation=None if status == prev_record['status'] else f"Changement de statut: {prev_record['status']} → {status}"
                    )
                
                roster_data.append(roster)
        
        # Vérifier les joueurs qui ne sont plus dans leur équipe précédente
        current_players = {(p.name, t.team_name.strip()) for t in self.league.teams for p in t.roster}
        for (player_name, team_name), prev_record in previous_rosters.items():
            if (player_name, team_name) not in current_players:
                # Marquer le joueur comme parti
                roster = RosterHistory(
                    date=self.today,
                    team=team_name,
                    player=player_name,
                    status='departed',
                    origin=prev_record['origin'],
                    arrival_date=prev_record['arrival_date'],
                    departure_date=self.today,
                    annotation=f"Quitté l'équipe le {self.today}"
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
        previous_fa = self._load_previous_free_agents()
        current_fa_set = set()
        
        for player in free_agents:
            current_fa_set.add(player.name)
            # Statistiques du jour
            daily_stats = {
                'pts': getattr(player, 'stats_pts', 0),
                'reb': getattr(player, 'stats_reb', 0),
                'ast': getattr(player, 'stats_ast', 0),
                'blk': getattr(player, 'stats_blk', 0),
                'stl': getattr(player, 'stats_stl', 0),
                '3pm': getattr(player, 'stats_3pm', 0),
                'fg_pct': getattr(player, 'stats_fg%', 0),
                'ft_pct': getattr(player, 'stats_ft%', 0),
            }
            
            # Récupérer l'historique du joueur s'il existe
            prev_record = previous_fa.get(player.name)
            annotation = None
            
            if prev_record is None:
                # Nouveau dans les agents libres
                annotation = f"Devenu agent libre le {self.today}"
            
            fa = FreeAgentMarket(
                date=self.today,
                player=player.name,
                nba_team=getattr(player, 'proTeam', 'Unknown'),
                last_week_stats=daily_stats,  # On utilise les stats du jour
                rolling_14d_stats=daily_stats,  # À améliorer avec calcul sur historique
                rolling_30d_stats=daily_stats,  # À améliorer avec calcul sur historique
                roster_percentage=getattr(player, 'percent_owned', 0),
                start_percentage=getattr(player, 'percent_started', 0),
                team_fit_score=None,  # À calculer
                pickup_stats=daily_stats,  # Stats au moment où il devient FA
                annotation=annotation
            )
            fa_data.append(fa)
        
        # Vérifier les joueurs qui ne sont plus agents libres
        for player_name, prev_record in previous_fa.items():
            if player_name not in current_fa_set:
                # Le joueur n'est plus agent libre
                fa = FreeAgentMarket(
                    date=self.today,
                    player=player_name,
                    nba_team=prev_record['nba_team'],
                    last_week_stats=prev_record['last_week_stats'],
                    rolling_14d_stats=prev_record['rolling_14d_stats'],
                    rolling_30d_stats=prev_record['rolling_30d_stats'],
                    roster_percentage=0,
                    start_percentage=0,
                    annotation=f"N'est plus agent libre depuis le {self.today}"
                )
                fa_data.append(fa)
        
        # Sauvegarde en CSV
        df = pd.DataFrame([{
            **vars(fa),
            **{'last_week_' + k: v for k, v in fa.last_week_stats.items()},
            **{'rolling_14d_' + k: v for k, v in fa.rolling_14d_stats.items()},
            **{'rolling_30d_' + k: v for k, v in fa.rolling_30d_stats.items()},
            **({'pickup_' + k: v for k, v in fa.pickup_stats.items()} if fa.pickup_stats else {})
        } for fa in fa_data])
        
        # Supprimer les colonnes dictionnaire
        df = df.drop(columns=['last_week_stats', 'rolling_14d_stats', 'rolling_30d_stats', 'pickup_stats'])
        self.file_manager.append_or_create(df, 'data/raw/free_agents/fa_market_history.csv')
        
        return fa_data

    def collect_daily_player_stats(self) -> List[Dict]:
        """Collecte les statistiques quotidiennes de tous les joueurs de la ligue"""
        daily_stats = []
        
        for team in self.league.teams:
            processed_players = set()  # Pour suivre les joueurs déjà traités
            for player in team.roster:
                if player.name in processed_players:  # Éviter les doublons
                    continue
                    
                # Collecter les statistiques de base
                # Log les attributs du joueur et ses statistiques pour debug
                self.logger.debug(f"Attributs du joueur {player.name}: {dir(player)}")
                if hasattr(player, 'stats'):
                    self.logger.debug(f"Statistiques disponibles pour {player.name}: {player.stats}")
                if hasattr(player, 'nine_cat_averages'):
                    self.logger.debug(f"Moyennes des 9 catégories pour {player.name}: {player.nine_cat_averages}")
                
                # Récupérer les stats depuis l'objet player
                # Récupérer les statistiques des moyennes des 9 catégories
                stats = {
                    'date': self.today,
                    'player': player.name,
                    'team': team.team_name.strip(),
                    'status': 'IR' if (hasattr(player, 'injured') and player.injured) else ('bench' if hasattr(player, 'slot_position') and player.slot_position == 'BE' else 'active')
                }
                
                # Ajouter les statistiques si nine_cat_averages existe
                if hasattr(player, 'nine_cat_averages'):
                    stats.update({
                        'pts': float(player.nine_cat_averages.get('PTS', 0)),
                        'reb': float(player.nine_cat_averages.get('REB', 0)),
                        'ast': float(player.nine_cat_averages.get('AST', 0)),
                        'blk': float(player.nine_cat_averages.get('BLK', 0)),
                        'stl': float(player.nine_cat_averages.get('STL', 0)),
                        '3pm': float(player.nine_cat_averages.get('3PM', 0)),
                        'fg_pct': float(player.nine_cat_averages.get('FG%', 0)),
                        'ft_pct': float(player.nine_cat_averages.get('FT%', 0))
                    })
                # Si pas de nine_cat_averages, essayer d'obtenir depuis les stats
                elif hasattr(player, 'stats') and '2026_total' in player.stats:
                    total_stats = player.stats['2026_total']['avg']
                    stats.update({
                        'pts': float(total_stats.get('PTS', 0)),
                        'reb': float(total_stats.get('REB', 0)),
                        'ast': float(total_stats.get('AST', 0)),
                        'blk': float(total_stats.get('BLK', 0)),
                        'stl': float(total_stats.get('STL', 0)),
                        '3pm': float(total_stats.get('3PM', 0)),
                        'fg_pct': float(total_stats.get('FG%', 0)),
                        'ft_pct': float(total_stats.get('FT%', 0))
                    })
                else:
                    # Si aucune statistique n'est disponible, mettre des 0
                    stats.update({
                        'pts': 0.0, 'reb': 0.0, 'ast': 0.0,
                        'blk': 0.0, 'stl': 0.0, '3pm': 0.0,
                        'fg_pct': 0.0, 'ft_pct': 0.0
                    })
                
                # Ajouter les informations supplémentaires
                stats.update({
                    'games_played': int(getattr(player, 'games_played', 0)),
                    'injury_status': bool(getattr(player, 'injured', False)),
                    'nba_team': getattr(player, 'proTeam', 'Unknown')
                })
                
                daily_stats.append(stats)
                processed_players.add(player.name)  # Marquer le joueur comme traité
        
        # Sauvegarder dans le fichier d'historique quotidien
        df = pd.DataFrame(daily_stats)
        
        # Ne garder que les joueurs qui ont joué (avec des stats non nulles)
        df = df[(df['games_played'] > 0) | 
               (df['pts'] > 0) | (df['reb'] > 0) | (df['ast'] > 0) |
               (df['blk'] > 0) | (df['stl'] > 0) | (df['3pm'] > 0) |
               (df['fg_pct'] > 0) | (df['ft_pct'] > 0)]
        
        self.file_manager.append_or_create(df, 'data/raw/stats/daily_player_stats.csv')
        
        return daily_stats

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

    def _load_previous_rosters(self) -> Dict:
        """Charge l'historique des rosters pour détecter les changements"""
        previous_rosters = {}
        try:
            roster_file = os.path.join(self.base_path, 'data/raw/rosters/roster_history.csv')
            if os.path.exists(roster_file):
                df = pd.read_csv(roster_file)
                # Obtenir les données les plus récentes pour chaque paire joueur-équipe
                latest_data = df.sort_values('date').groupby(['player', 'team']).last()
                for (player_name, team_name), row in latest_data.iterrows():
                    previous_rosters[(player_name, team_name)] = row.to_dict()
        except Exception as e:
            self.logger.warning(f"Impossible de charger l'historique des rosters : {str(e)}")
        return previous_rosters

    def _load_previous_free_agents(self) -> Dict:
        """Charge l'historique des agents libres pour détecter les changements"""
        previous_fa = {}
        try:
            fa_file = os.path.join(self.base_path, 'data/raw/free_agents/fa_market_history.csv')
            if os.path.exists(fa_file):
                df = pd.read_csv(fa_file)
                # Obtenir les données les plus récentes pour chaque joueur
                latest_data = df.sort_values('date').groupby('player').last()
                
                for player_name, row in latest_data.iterrows():
                    # Reconstruire les dictionnaires de stats
                    last_week_stats = {}
                    rolling_14d_stats = {}
                    rolling_30d_stats = {}
                    
                    for col in df.columns:
                        if col.startswith('last_week_'):
                            last_week_stats[col.replace('last_week_', '')] = row[col]
                        elif col.startswith('rolling_14d_'):
                            rolling_14d_stats[col.replace('rolling_14d_', '')] = row[col]
                        elif col.startswith('rolling_30d_'):
                            rolling_30d_stats[col.replace('rolling_30d_', '')] = row[col]
                    
                    previous_fa[player_name] = {
                        'nba_team': row['nba_team'],
                        'last_week_stats': last_week_stats,
                        'rolling_14d_stats': rolling_14d_stats,
                        'rolling_30d_stats': rolling_30d_stats
                    }
        except Exception as e:
            self.logger.warning(f"Impossible de charger l'historique des agents libres : {str(e)}")
        return previous_fa

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
        
        # 6. Statistiques quotidiennes des joueurs
        print("\n6. Collecte des statistiques quotidiennes des joueurs...")
        daily_stats = collector.collect_daily_player_stats()
        print("✅ Statistiques quotidiennes des joueurs sauvegardées")
        
        print("\n✨ Collecte terminée avec succès ! Les données sont dans data/raw/")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la collecte : {str(e)}")
        logging.error(f"Erreur détaillée : {str(e)}")

if __name__ == "__main__":
    main()
