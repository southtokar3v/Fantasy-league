#!/usr/bin/env python3
"""
Extraction des Données des Joueurs ESPN
Script pour extraire les données des joueurs et statistiques
"""

import requests
import json
import pandas as pd
from datetime import datetime
import os

# Configuration
LEAGUE_ID = 1557635339
SEASON = 2026
MY_TEAM_ABBREV = "NC99"

def get_team_roster(team_id):
    """Récupère le roster d'une équipe"""
    url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/FBA/seasons/{SEASON}/segments/0/leagues/{LEAGUE_ID}/teams/{team_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Erreur pour l'équipe {team_id} : {e}")
        return None

def get_league_standings():
    """Récupère le classement de la ligue"""
    url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/FBA/seasons/{SEASON}/segments/0/leagues/{LEAGUE_ID}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Erreur classement : {e}")
        return None

def extract_player_data(roster_data):
    """Extrait les données des joueurs"""
    players = []
    
    if not roster_data or 'roster' not in roster_data:
        return players
    
    for player in roster_data['roster']:
        player_info = {
            'player_id': player.get('id'),
            'name': player.get('fullName', 'N/A'),
            'position': player.get('defaultPositionId'),
            'position_name': get_position_name(player.get('defaultPositionId')),
            'status': player.get('injuryStatus', 'ACTIVE'),
            'injured': player.get('injured', False),
            'team_id': roster_data.get('id'),
            'team_abbrev': roster_data.get('abbrev'),
            'is_my_team': roster_data.get('abbrev') == MY_TEAM_ABBREV
        }
        players.append(player_info)
    
    return players

def get_position_name(position_id):
    """Convertit l'ID de position en nom"""
    positions = {
        1: 'PG',  # Point Guard
        2: 'SG',  # Shooting Guard
        3: 'SF',  # Small Forward
        4: 'PF',  # Power Forward
        5: 'C',   # Center
        6: 'G',   # Guard
        7: 'F',   # Forward
        8: 'UTIL' # Utility
    }
    return positions.get(position_id, 'N/A')

def extract_standings_data(league_data):
    """Extrait les données de classement"""
    standings = []
    
    if not league_data or 'teams' not in league_data:
        return standings
    
    for team in league_data['teams']:
        team_info = {
            'team_id': team.get('id'),
            'abbrev': team.get('abbrev'),
            'name': team.get('name', 'N/A'),
            'is_my_team': team.get('abbrev') == MY_TEAM_ABBREV,
            'rank': team.get('rank', 'N/A'),
            'wins': team.get('wins', 0),
            'losses': team.get('losses', 0),
            'ties': team.get('ties', 0)
        }
        standings.append(team_info)
    
    return standings

def save_players_data(players, standings):
    """Sauvegarde les données des joueurs"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Sauvegarde JSON complète
    complete_data = {
        'players': players,
        'standings': standings,
        'extraction_timestamp': timestamp,
        'total_players': len(players),
        'my_team_players': len([p for p in players if p['is_my_team']])
    }
    
    json_filename = f"espn_players_data_{timestamp}.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(complete_data, f, indent=2, ensure_ascii=False)
    
    # Sauvegarde CSV des joueurs
    players_df = pd.DataFrame(players)
    players_csv = f"espn_players_{timestamp}.csv"
    players_df.to_csv(players_csv, index=False, encoding='utf-8')
    
    # Sauvegarde CSV du classement
    standings_df = pd.DataFrame(standings)
    standings_csv = f"espn_standings_{timestamp}.csv"
    standings_df.to_csv(standings_csv, index=False, encoding='utf-8')
    
    return json_filename, players_csv, standings_csv

def main():
    """Fonction principale"""
    print("🏀 EXTRACTION DES DONNÉES DES JOUEURS ESPN")
    print("=" * 60)
    
    # Récupérer les données de la ligue
    print("📡 Récupération des données de la ligue...")
    league_data = get_league_standings()
    
    if not league_data:
        print("❌ Impossible de récupérer les données de la ligue")
        return
    
    print("✅ Données de la ligue récupérées")
    
    # Extraire le classement
    standings = extract_standings_data(league_data)
    print(f"📊 Classement extrait : {len(standings)} équipes")
    
    # Récupérer les données des joueurs pour chaque équipe
    all_players = []
    
    print(f"\n🏀 Récupération des joueurs...")
    for team in league_data.get('teams', []):
        team_id = team.get('id')
        team_abbrev = team.get('abbrev')
        
        print(f"   📋 Équipe {team_abbrev} (ID: {team_id})...")
        
        roster_data = get_team_roster(team_id)
        if roster_data:
            players = extract_player_data(roster_data)
            all_players.extend(players)
            print(f"      ✅ {len(players)} joueurs trouvés")
        else:
            print(f"      ❌ Erreur pour l'équipe {team_abbrev}")
    
    # Afficher les résultats
    print(f"\n📊 RÉSULTATS :")
    print(f"   🏀 Total joueurs : {len(all_players)}")
    print(f"   👥 Équipes : {len(standings)}")
    
    my_team_players = [p for p in all_players if p['is_my_team']]
    print(f"   🎯 Vos joueurs : {len(my_team_players)}")
    
    if my_team_players:
        print(f"\n🎯 VOS JOUEURS ({MY_TEAM_ABBREV}) :")
        for player in my_team_players:
            status_icon = "🏥" if player['injured'] else "✅"
            print(f"   {status_icon} {player['name']} ({player['position_name']}) - {player['status']}")
    
    # Sauvegarder les données
    print(f"\n💾 Sauvegarde des données...")
    json_file, players_csv, standings_csv = save_players_data(all_players, standings)
    
    print(f"✅ Données sauvegardées :")
    print(f"   📄 JSON complet : {json_file}")
    print(f"   🏀 Joueurs CSV : {players_csv}")
    print(f"   📊 Classement CSV : {standings_csv}")
    
    print(f"\n🎉 EXTRACTION TERMINÉE !")
    print(f"📊 {len(all_players)} joueurs extraits")
    print(f"👥 {len(standings)} équipes analysées")
    print(f"🎯 {len(my_team_players)} joueurs dans votre équipe")

if __name__ == "__main__":
    main()
