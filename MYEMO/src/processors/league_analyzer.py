#!/usr/bin/env python3
"""
Script pour analyser une ligue ESPN Fantasy Football
Utilise la librairie espn-api pour récupérer:
- Les lineups des équipes
- Le classement de la ligue
- Les transactions récentes
"""

import json
from datetime import datetime
from espn_api.football import League
from espn_api.football import ESPN

def get_league_data(league_id, season=2026):
    """
    Récupère les données de la ligue ESPN
    
    Args:
        league_id (int): ID de la ligue ESPN
        season (int): Année de la saison (défaut: 2026)
    
    Returns:
        dict: Dictionnaire contenant toutes les données de la ligue
    """
    try:
        # Initialisation de la ligue
        league = League(league_id=league_id, year=season)
        
        print(f"📊 Récupération des données de la ligue {league_id} pour la saison {season}")
        print(f"🏈 Nom de la ligue: {league.settings.name}")
        print(f"👥 Nombre d'équipes: {len(league.teams)}")
        print("-" * 50)
        
        # Récupération des données
        data = {
            'league_info': {
                'name': league.settings.name,
                'season': season,
                'total_teams': len(league.teams),
                'scoring_type': league.settings.scoring_type,
                'playoff_teams': league.settings.playoff_team_count
            },
            'standings': get_standings(league),
            'lineups': get_all_lineups(league),
            'recent_transactions': get_recent_transactions(league),
            'matchups': get_current_matchups(league)
        }
        
        return data
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des données: {e}")
        return None

def get_standings(league):
    """
    Récupère le classement de la ligue
    """
    print("📈 Récupération du classement...")
    
    standings = []
    for team in league.standings:
        standings.append({
            'rank': team.standing,
            'team_name': team.team_name,
            'owner': team.owner,
            'wins': team.wins,
            'losses': team.losses,
            'ties': team.ties,
            'win_percentage': team.win_percentage,
            'points_for': team.points_for,
            'points_against': team.points_against
        })
    
    return standings

def get_all_lineups(league):
    """
    Récupère les lineups de toutes les équipes
    """
    print("👥 Récupération des lineups...")
    
    lineups = {}
    for team in league.teams:
        lineup = []
        for player in team.roster:
            lineup.append({
                'name': player.name,
                'position': player.position,
                'team': player.proTeam,
                'points': player.total_points,
                'projected_points': player.projected_total_points,
                'injury_status': player.injuryStatus,
                'lineup_slot': player.lineupSlot
            })
        
        lineups[team.team_name] = {
            'owner': team.owner,
            'roster': lineup
        }
    
    return lineups

def get_recent_transactions(league):
    """
    Récupère les transactions récentes
    """
    print("🔄 Récupération des transactions...")
    
    transactions = []
    for transaction in league.recent_activity(25):  # 25 dernières transactions
        transactions.append({
            'date': transaction.date,
            'type': transaction.type,
            'description': transaction.description,
            'team': transaction.team_name if hasattr(transaction, 'team_name') else 'N/A'
        })
    
    return transactions

def get_current_matchups(league):
    """
    Récupère les matchups actuels
    """
    print("⚔️ Récupération des matchups...")
    
    matchups = []
    current_week = league.current_week
    
    for matchup in league.scoreboard():
        matchups.append({
            'week': current_week,
            'home_team': matchup.home_team.team_name,
            'home_score': matchup.home_score,
            'away_team': matchup.away_team.team_name,
            'away_score': matchup.away_score,
            'winner': matchup.winner if hasattr(matchup, 'winner') else 'TBD'
        })
    
    return matchups

def display_standings(standings):
    """
    Affiche le classement de manière formatée
    """
    print("\n🏆 CLASSEMENT DE LA LIGUE")
    print("=" * 80)
    print(f"{'Rang':<4} {'Équipe':<25} {'Propriétaire':<20} {'W-L-T':<8} {'Pts Pour':<10} {'Pts Contre':<12}")
    print("-" * 80)
    
    for team in standings:
        record = f"{team['wins']}-{team['losses']}-{team['ties']}"
        print(f"{team['rank']:<4} {team['team_name']:<25} {team['owner']:<20} {record:<8} {team['points_for']:<10.1f} {team['points_against']:<12.1f}")

def display_lineups(lineups):
    """
    Affiche les lineups de toutes les équipes
    """
    print("\n👥 LINEUPS DES ÉQUIPES")
    print("=" * 100)
    
    for team_name, team_data in lineups.items():
        print(f"\n🏈 {team_name} (Propriétaire: {team_data['owner']})")
        print("-" * 60)
        
        # Grouper par position
        positions = {}
        for player in team_data['roster']:
            pos = player['lineup_slot']
            if pos not in positions:
                positions[pos] = []
            positions[pos].append(player)
        
        # Afficher par position
        for pos in ['QB', 'RB', 'WR', 'TE', 'FLEX', 'K', 'D/ST', 'BENCH']:
            if pos in positions:
                print(f"\n{pos}:")
                for player in positions[pos]:
                    status = f" ({player['injury_status']})" if player['injury_status'] else ""
                    print(f"  • {player['name']} ({player['team']}) - {player['points']:.1f} pts{status}")

def display_transactions(transactions):
    """
    Affiche les transactions récentes
    """
    print("\n🔄 TRANSACTIONS RÉCENTES")
    print("=" * 80)
    
    for transaction in transactions[:10]:  # Afficher les 10 dernières
        print(f"📅 {transaction['date']} - {transaction['type']}")
        print(f"   {transaction['description']}")
        print()

def save_to_json(data, filename="espn_league_data.json"):
    """
    Sauvegarde les données en JSON
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    print(f"💾 Données sauvegardées dans {filename}")

def main():
    """
    Fonction principale
    """
    # Configuration
    LEAGUE_ID = 1557635339
    SEASON = 2026
    
    print("🚀 ESPN Fantasy Football League Analyzer")
    print("=" * 50)
    
    # Récupération des données
    data = get_league_data(LEAGUE_ID, SEASON)
    
    if data:
        # Affichage des résultats
        display_standings(data['standings'])
        display_lineups(data['lineups'])
        display_transactions(data['recent_transactions'])
        
        # Sauvegarde
        save_to_json(data)
        
        print(f"\n✅ Analyse terminée avec succès!")
        print(f"📊 {data['league_info']['total_teams']} équipes analysées")
        print(f"📈 {len(data['standings'])} équipes dans le classement")
        print(f"🔄 {len(data['recent_transactions'])} transactions récupérées")
    else:
        print("❌ Échec de l'analyse de la ligue")

if __name__ == "__main__":
    main()
