#!/usr/bin/env python3
"""
ESPN Fantasy NBA Advanced Data Collector
Système complet de collecte de données pour piloter une ligue Fantasy NBA au maximum
Collecte quotidienne structurée pour analyses IA et optimisations
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import time
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from espn_api.basketball import League
from espn_api.basketball import ESPN

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('espn_nba_analyzer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class PlayerStats:
    """Structure pour les stats d'un joueur"""
    player_id: str
    name: str
    position: str
    team: str
    status: str  # active/bench/injured
    injury_status: str
    points: float
    rebounds: float
    assists: float
    steals: float
    blocks: float
    fg_percentage: float
    ft_percentage: float
    three_pointers: int
    turnovers: int
    plus_minus: float
    minutes: float
    games_played: int
    date: str
    is_bench: bool
    efficiency: float
    usage_rate: float

@dataclass
class TeamData:
    """Structure pour les données d'une équipe"""
    team_id: str
    team_name: str
    manager: str
    is_my_team: bool
    roster: List[PlayerStats]
    total_stats: Dict[str, float]
    bench_stats: Dict[str, float]
    active_stats: Dict[str, float]
    ranking: int
    category_rankings: Dict[str, int]

@dataclass
class LeagueSnapshot:
    """Snapshot complet de la ligue à un moment donné"""
    date: str
    league_id: str
    season: int
    scoring_type: str
    teams: List[TeamData]
    free_agents: List[Dict]
    transactions: List[Dict]
    injuries: List[Dict]
    nba_schedule: List[Dict]
    hot_cold_analysis: Dict
    ai_recommendations: List[Dict]

class ESPNNBAAdvancedAnalyzer:
    """Analyseur avancé pour ESPN Fantasy NBA"""
    
    def __init__(self, league_id: int, season: int, my_team_name: str = "Neon Cobras 99"):
        self.league_id = league_id
        self.season = season
        self.my_team_name = my_team_name
        self.league = None
        self.data_history = []
        self.setup_league()
    
    def setup_league(self):
        """Initialise la connexion à la ligue ESPN"""
        try:
            self.league = League(league_id=self.league_id, year=self.season)
            logger.info(f"✅ Connexion établie à la ligue {self.league_id} - {self.season}")
            logger.info(f"🏀 Ligue: {self.league.settings.name}")
            logger.info(f"👥 {len(self.league.teams)} équipes")
        except Exception as e:
            logger.error(f"❌ Erreur connexion ligue: {e}")
            raise
    
    def collect_daily_data(self) -> LeagueSnapshot:
        """Collecte complète des données quotidiennes"""
        logger.info("🚀 Début de la collecte quotidienne des données")
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # 1. Infos générales ligue
        league_info = self._get_league_info()
        
        # 2. Données des équipes
        teams_data = self._get_teams_data()
        
        # 3. Free agents
        free_agents = self._get_free_agents()
        
        # 4. Transactions
        transactions = self._get_transactions()
        
        # 5. Blessures
        injuries = self._get_injuries()
        
        # 6. Planning NBA
        nba_schedule = self._get_nba_schedule()
        
        # 7. Analyses hot/cold
        hot_cold = self._analyze_hot_cold_streaks()
        
        # 8. Recommandations IA
        ai_recs = self._generate_ai_recommendations()
        
        snapshot = LeagueSnapshot(
            date=current_date,
            league_id=str(self.league_id),
            season=self.season,
            scoring_type=league_info['scoring_type'],
            teams=teams_data,
            free_agents=free_agents,
            transactions=transactions,
            injuries=injuries,
            nba_schedule=nba_schedule,
            hot_cold_analysis=hot_cold,
            ai_recommendations=ai_recs
        )
        
        self.data_history.append(snapshot)
        logger.info("✅ Collecte quotidienne terminée")
        
        return snapshot
    
    def _get_league_info(self) -> Dict:
        """Récupère les informations générales de la ligue"""
        return {
            'league_id': self.league_id,
            'season': self.season,
            'name': self.league.settings.name,
            'scoring_type': self.league.settings.scoring_type,
            'total_teams': len(self.league.teams),
            'playoff_teams': self.league.settings.playoff_team_count,
            'current_week': self.league.current_week
        }
    
    def _get_teams_data(self) -> List[TeamData]:
        """Récupère les données complètes de toutes les équipes"""
        teams_data = []
        
        for team in self.league.teams:
            is_my_team = team.team_name == self.my_team_name
            
            # Roster complet avec statuts
            roster = self._get_team_roster(team)
            
            # Stats totales
            total_stats = self._calculate_team_stats(roster, bench_only=False)
            bench_stats = self._calculate_team_stats(roster, bench_only=True)
            active_stats = self._calculate_team_stats(roster, active_only=True)
            
            # Classements
            ranking = team.standing
            category_rankings = self._get_category_rankings(team)
            
            team_data = TeamData(
                team_id=str(team.team_id),
                team_name=team.team_name,
                manager=team.owner,
                is_my_team=is_my_team,
                roster=roster,
                total_stats=total_stats,
                bench_stats=bench_stats,
                active_stats=active_stats,
                ranking=ranking,
                category_rankings=category_rankings
            )
            
            teams_data.append(team_data)
        
        return teams_data
    
    def _get_team_roster(self, team) -> List[PlayerStats]:
        """Récupère le roster d'une équipe avec statuts détaillés"""
        roster = []
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        for player in team.roster:
            # Détermine si le joueur est sur le banc
            is_bench = player.lineupSlot in ['BE', 'IR']
            
            # Stats du joueur
            stats = {
                'points': player.total_points,
                'rebounds': player.rebounds,
                'assists': player.assists,
                'steals': player.steals,
                'blocks': player.blocks,
                'fg_percentage': player.field_goal_percentage,
                'ft_percentage': player.free_throw_percentage,
                'three_pointers': player.three_pointers_made,
                'turnovers': player.turnovers,
                'plus_minus': getattr(player, 'plus_minus', 0),
                'minutes': getattr(player, 'minutes', 0),
                'games_played': getattr(player, 'games_played', 0)
            }
            
            # Calculs avancés
            efficiency = self._calculate_efficiency(stats)
            usage_rate = getattr(player, 'usage_rate', 0)
            
            player_stats = PlayerStats(
                player_id=str(player.playerId),
                name=player.name,
                position=player.position,
                team=player.proTeam,
                status='active' if not is_bench else 'bench',
                injury_status=getattr(player, 'injuryStatus', ''),
                points=stats['points'],
                rebounds=stats['rebounds'],
                assists=stats['assists'],
                steals=stats['steals'],
                blocks=stats['blocks'],
                fg_percentage=stats['fg_percentage'],
                ft_percentage=stats['ft_percentage'],
                three_pointers=stats['three_pointers'],
                turnovers=stats['turnovers'],
                plus_minus=stats['plus_minus'],
                minutes=stats['minutes'],
                games_played=stats['games_played'],
                date=current_date,
                is_bench=is_bench,
                efficiency=efficiency,
                usage_rate=usage_rate
            )
            
            roster.append(player_stats)
        
        return roster
    
    def _calculate_team_stats(self, roster: List[PlayerStats], bench_only: bool = False, active_only: bool = False) -> Dict[str, float]:
        """Calcule les stats d'une équipe (totales, bench, ou actives)"""
        filtered_roster = roster
        
        if bench_only:
            filtered_roster = [p for p in roster if p.is_bench]
        elif active_only:
            filtered_roster = [p for p in roster if not p.is_bench]
        
        if not filtered_roster:
            return {key: 0.0 for key in ['points', 'rebounds', 'assists', 'steals', 'blocks', 'fg_percentage', 'ft_percentage', 'three_pointers', 'turnovers']}
        
        stats = {
            'points': sum(p.points for p in filtered_roster),
            'rebounds': sum(p.rebounds for p in filtered_roster),
            'assists': sum(p.assists for p in filtered_roster),
            'steals': sum(p.steals for p in filtered_roster),
            'blocks': sum(p.blocks for p in filtered_roster),
            'fg_percentage': np.mean([p.fg_percentage for p in filtered_roster if p.fg_percentage > 0]),
            'ft_percentage': np.mean([p.ft_percentage for p in filtered_roster if p.ft_percentage > 0]),
            'three_pointers': sum(p.three_pointers for p in filtered_roster),
            'turnovers': sum(p.turnovers for p in filtered_roster)
        }
        
        return stats
    
    def _get_category_rankings(self, team) -> Dict[str, int]:
        """Récupère les classements par catégorie pour une équipe"""
        # Cette fonction nécessiterait l'accès aux classements détaillés
        # Pour l'instant, on retourne des valeurs par défaut
        return {
            'points': 1,
            'rebounds': 1,
            'assists': 1,
            'steals': 1,
            'blocks': 1,
            'fg_percentage': 1,
            'ft_percentage': 1,
            'three_pointers': 1,
            'turnovers': 1
        }
    
    def _calculate_efficiency(self, stats: Dict) -> float:
        """Calcule l'efficacité d'un joueur"""
        try:
            eff = (stats['points'] + stats['rebounds'] + stats['assists'] + 
                   stats['steals'] + stats['blocks'] - stats['turnovers'])
            return eff
        except:
            return 0.0
    
    def _get_free_agents(self) -> List[Dict]:
        """Récupère la liste des free agents avec leurs stats"""
        try:
            # Récupère les free agents disponibles
            free_agents = []
            # Cette partie nécessiterait une implémentation spécifique selon l'API
            return free_agents
        except Exception as e:
            logger.error(f"Erreur récupération FA: {e}")
            return []
    
    def _get_transactions(self) -> List[Dict]:
        """Récupère les transactions récentes"""
        try:
            transactions = []
            for activity in self.league.recent_activity(50):
                transactions.append({
                    'date': activity.date,
                    'type': activity.type,
                    'description': activity.description,
                    'team': getattr(activity, 'team_name', 'N/A')
                })
            return transactions
        except Exception as e:
            logger.error(f"Erreur récupération transactions: {e}")
            return []
    
    def _get_injuries(self) -> List[Dict]:
        """Récupère les informations sur les blessures"""
        injuries = []
        # Cette fonction nécessiterait l'intégration avec une API de blessures NBA
        return injuries
    
    def _get_nba_schedule(self) -> List[Dict]:
        """Récupère le planning NBA"""
        schedule = []
        # Cette fonction nécessiterait l'intégration avec l'API NBA
        return schedule
    
    def _analyze_hot_cold_streaks(self) -> Dict:
        """Analyse les tendances hot/cold des joueurs"""
        if len(self.data_history) < 2:
            return {}
        
        # Compare les performances récentes
        current_snapshot = self.data_history[-1]
        previous_snapshot = self.data_history[-2]
        
        hot_cold_analysis = {
            'hot_players': [],
            'cold_players': [],
            'trending_up': [],
            'trending_down': []
        }
        
        # Analyse des tendances (simplifiée)
        for team in current_snapshot.teams:
            for player in team.roster:
                # Logique d'analyse des tendances
                pass
        
        return hot_cold_analysis
    
    def _generate_ai_recommendations(self) -> List[Dict]:
        """Génère des recommandations IA basées sur les données"""
        recommendations = []
        
        # Analyse des points perdus sur le banc
        my_team = None
        for team in self.data_history[-1].teams if self.data_history else []:
            if team.is_my_team:
                my_team = team
                break
        
        if my_team:
            # Recommandations basées sur les stats du banc
            bench_points = my_team.bench_stats.get('points', 0)
            if bench_points > 20:  # Seuil arbitraire
                recommendations.append({
                    'type': 'bench_optimization',
                    'message': f"Points perdus sur le banc: {bench_points:.1f}",
                    'priority': 'high'
                })
        
        return recommendations
    
    def export_to_google_sheets_format(self, snapshot: LeagueSnapshot) -> Dict:
        """Exporte les données au format Google Sheets"""
        export_data = {
            'league_info': asdict(snapshot),
            'teams_summary': [],
            'players_detailed': [],
            'transactions': snapshot.transactions,
            'free_agents': snapshot.free_agents,
            'injuries': snapshot.injuries,
            'ai_insights': snapshot.ai_recommendations
        }
        
        # Résumé des équipes
        for team in snapshot.teams:
            export_data['teams_summary'].append({
                'team_name': team.team_name,
                'manager': team.manager,
                'is_my_team': team.is_my_team,
                'ranking': team.ranking,
                'total_points': team.total_stats.get('points', 0),
                'bench_points': team.bench_stats.get('points', 0),
                'active_points': team.active_stats.get('points', 0)
            })
        
        # Détails des joueurs
        for team in snapshot.teams:
            for player in team.roster:
                export_data['players_detailed'].append({
                    'date': player.date,
                    'team': team.team_name,
                    'is_my_team': team.is_my_team,
                    'player_name': player.name,
                    'position': player.position,
                    'status': player.status,
                    'is_bench': player.is_bench,
                    'points': player.points,
                    'rebounds': player.rebounds,
                    'assists': player.assists,
                    'steals': player.steals,
                    'blocks': player.blocks,
                    'efficiency': player.efficiency,
                    'injury_status': player.injury_status
                })
        
        return export_data
    
    def save_daily_snapshot(self, snapshot: LeagueSnapshot):
        """Sauvegarde le snapshot quotidien"""
        filename = f"espn_nba_daily_{snapshot.date}.json"
        
        export_data = self.export_to_google_sheets_format(snapshot)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"💾 Snapshot sauvegardé: {filename}")
    
    def generate_daily_report(self, snapshot: LeagueSnapshot):
        """Génère un rapport quotidien"""
        print("\n" + "="*80)
        print(f"📊 RAPPORT QUOTIDIEN - {snapshot.date}")
        print("="*80)
        
        # Trouve mon équipe
        my_team = None
        for team in snapshot.teams:
            if team.is_my_team:
                my_team = team
                break
        
        if my_team:
            print(f"\n🏀 MON ÉQUIPE: {my_team.team_name} (Rang: {my_team.ranking})")
            print(f"📈 Points totaux: {my_team.total_stats.get('points', 0):.1f}")
            print(f"🪑 Points sur le banc: {my_team.bench_stats.get('points', 0):.1f}")
            print(f"⚡ Points actifs: {my_team.active_stats.get('points', 0):.1f}")
            
            # Analyse des points perdus
            bench_points = my_team.bench_stats.get('points', 0)
            if bench_points > 15:
                print(f"⚠️  ATTENTION: {bench_points:.1f} points perdus sur le banc!")
        
        # Classement général
        print(f"\n🏆 CLASSEMENT GÉNÉRAL")
        print("-" * 50)
        for i, team in enumerate(sorted(snapshot.teams, key=lambda x: x.ranking)[:5]):
            marker = "👑" if team.is_my_team else "  "
            print(f"{marker} {team.ranking}. {team.team_name} - {team.total_stats.get('points', 0):.1f} pts")
        
        # Transactions récentes
        if snapshot.transactions:
            print(f"\n🔄 TRANSACTIONS RÉCENTES")
            print("-" * 50)
            for trans in snapshot.transactions[:5]:
                print(f"📅 {trans['date']} - {trans['type']}: {trans['description']}")
        
        # Recommandations IA
        if snapshot.ai_recommendations:
            print(f"\n🤖 RECOMMANDATIONS IA")
            print("-" * 50)
            for rec in snapshot.ai_recommendations:
                print(f"💡 {rec['message']}")

def main():
    """Fonction principale"""
    # Configuration
    LEAGUE_ID = 1557635339
    SEASON = 2026
    MY_TEAM_NAME = "Neon Cobras 99"
    
    print("🚀 ESPN Fantasy NBA Advanced Analyzer")
    print("="*60)
    
    try:
        # Initialisation
        analyzer = ESPNNBAAdvancedAnalyzer(LEAGUE_ID, SEASON, MY_TEAM_NAME)
        
        # Collecte quotidienne
        snapshot = analyzer.collect_daily_data()
        
        # Sauvegarde
        analyzer.save_daily_snapshot(snapshot)
        
        # Rapport
        analyzer.generate_daily_report(snapshot)
        
        print(f"\n✅ Analyse terminée avec succès!")
        print(f"📊 {len(snapshot.teams)} équipes analysées")
        print(f"👥 {sum(len(team.roster) for team in snapshot.teams)} joueurs trackés")
        print(f"🔄 {len(snapshot.transactions)} transactions récupérées")
        
    except Exception as e:
        logger.error(f"❌ Erreur dans l'analyse: {e}")
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()
