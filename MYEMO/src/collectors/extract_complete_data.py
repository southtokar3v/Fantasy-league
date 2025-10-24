#!/usr/bin/env python3
"""
Extraction Complète des Données ESPN
Script pour extraire toutes les données de votre ligue Fantasy NBA
"""

import requests
import json
import pandas as pd
from datetime import datetime
import os

# Configuration
LEAGUE_ID = 1557635339
SEASON = 2026
MY_TEAM_ABBREV = "NC99"  # Votre équipe "Neon Cobras 99"
MY_TEAM_ID = 10  # ID de votre équipe

def get_espn_data():
    """Récupère les données de la ligue ESPN"""
    url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/FBA/seasons/{SEASON}/segments/0/leagues/{LEAGUE_ID}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Erreur API : {e}")
        return None

def extract_league_info(data):
    """Extrait les informations générales de la ligue"""
    info = {
        'league_id': LEAGUE_ID,
        'season': SEASON,
        'league_name': data.get('settings', {}).get('name', 'N/A'),
        'total_teams': len(data.get('teams', [])),
        'scoring_type': 'Rotisserie',  # Votre ligue est en ROTO
        'extraction_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return info

def extract_teams_info(data):
    """Extrait les informations des équipes"""
    teams = []
    
    for team in data.get('teams', []):
        team_info = {
            'team_id': team.get('id'),
            'abbrev': team.get('abbrev'),
            'name': team.get('name', 'N/A'),
            'owners': team.get('owners', []),
            'is_my_team': team.get('abbrev') == MY_TEAM_ABBREV
        }
        teams.append(team_info)
    
    return teams

def extract_members_info(data):
    """Extrait les informations des membres"""
    members = []
    
    for member in data.get('members', []):
        member_info = {
            'member_id': member.get('id'),
            'display_name': member.get('displayName'),
            'is_league_manager': member.get('isLeagueManager', False)
        }
        members.append(member_info)
    
    return members

def find_my_team_owner(teams, members):
    """Trouve le propriétaire de votre équipe"""
    my_team = next((t for t in teams if t['abbrev'] == MY_TEAM_ABBREV), None)
    
    if my_team and my_team['owners']:
        owner_id = my_team['owners'][0]
        owner = next((m for m in members if m['member_id'] == owner_id), None)
        return owner
    
    return None

def save_data_to_files(league_info, teams, members, my_team_owner):
    """Sauvegarde les données dans différents formats"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Sauvegarde JSON complète
    complete_data = {
        'league_info': league_info,
        'teams': teams,
        'members': members,
        'my_team_owner': my_team_owner,
        'extraction_timestamp': timestamp
    }
    
    json_filename = f"espn_complete_data_{timestamp}.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(complete_data, f, indent=2, ensure_ascii=False)
    
    # Sauvegarde CSV des équipes
    teams_df = pd.DataFrame(teams)
    teams_csv = f"espn_teams_{timestamp}.csv"
    teams_df.to_csv(teams_csv, index=False, encoding='utf-8')
    
    # Sauvegarde CSV des membres
    members_df = pd.DataFrame(members)
    members_csv = f"espn_members_{timestamp}.csv"
    members_df.to_csv(members_csv, index=False, encoding='utf-8')
    
    return json_filename, teams_csv, members_csv

def main():
    """Fonction principale"""
    print("🚀 EXTRACTION COMPLÈTE DES DONNÉES ESPN")
    print("=" * 60)
    
    # Récupérer les données
    print("📡 Récupération des données...")
    data = get_espn_data()
    
    if not data:
        print("❌ Impossible de récupérer les données")
        return
    
    print("✅ Données récupérées avec succès")
    
    # Extraire les informations
    print("\n🔍 Extraction des informations...")
    
    league_info = extract_league_info(data)
    teams = extract_teams_info(data)
    members = extract_members_info(data)
    my_team_owner = find_my_team_owner(teams, members)
    
    # Afficher les résultats
    print(f"\n📊 INFORMATIONS DE LIGUE :")
    print(f"   🏆 Nom : {league_info['league_name']}")
    print(f"   📅 Saison : {league_info['season']}")
    print(f"   👥 Équipes : {league_info['total_teams']}")
    print(f"   🎯 Type : {league_info['scoring_type']}")
    
    print(f"\n👥 ÉQUIPES TROUVÉES :")
    for team in teams:
        status = "🎉 VOTRE ÉQUIPE" if team['is_my_team'] else "   "
        print(f"   {status} {team['abbrev']} (ID: {team['team_id']}) - {team['name']}")
    
    if my_team_owner:
        print(f"\n👤 VOTRE ÉQUIPE :")
        print(f"   🏆 Équipe : {MY_TEAM_ABBREV} (ID: {MY_TEAM_ID})")
        print(f"   👤 Propriétaire : {my_team_owner['display_name']}")
        print(f"   🎯 Manager : {'Oui' if my_team_owner['is_league_manager'] else 'Non'}")
    
    # Sauvegarder les données
    print(f"\n💾 Sauvegarde des données...")
    json_file, teams_csv, members_csv = save_data_to_files(league_info, teams, members, my_team_owner)
    
    print(f"✅ Données sauvegardées :")
    print(f"   📄 JSON complet : {json_file}")
    print(f"   📊 Équipes CSV : {teams_csv}")
    print(f"   👤 Membres CSV : {members_csv}")
    
    print(f"\n🎉 EXTRACTION TERMINÉE !")
    print(f"📊 {len(teams)} équipes trouvées")
    print(f"👤 {len(members)} membres trouvés")
    print(f"🎯 Votre équipe '{MY_TEAM_ABBREV}' identifiée")

if __name__ == "__main__":
    main()
