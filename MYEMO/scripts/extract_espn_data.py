#!/usr/bin/env python3
"""
Extraction Améliorée ESPN
Script pour extraire correctement les données ESPN
"""

import requests
import json
from datetime import datetime

def extract_league_data():
    """Extraction améliorée des données de ligue"""
    print("🔍 EXTRACTION AMÉLIORÉE ESPN")
    print("=" * 50)
    
    # Configuration
    LEAGUE_ID = 1557635339
    SEASON = 2026
    
    # Endpoint qui fonctionne
    endpoint = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/FBA/seasons/{SEASON}/segments/0/leagues/{LEAGUE_ID}"
    
    try:
        print(f"🌐 Endpoint : {endpoint}")
        response = requests.get(endpoint, timeout=10)
        print(f"📊 Status : {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Données récupérées")
            
            # Sauvegarder les données brutes pour analyse
            filename = f"espn_raw_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"💾 Données brutes sauvegardées : {filename}")
            
            # Analyser la structure des données
            print(f"\n🔍 ANALYSE DE LA STRUCTURE :")
            print(f"   Clés principales : {list(data.keys())}")
            
            # Analyser les équipes
            if 'teams' in data:
                teams = data['teams']
                print(f"   👥 Nombre d'équipes : {len(teams)}")
                
                if teams:
                    print(f"   📋 Structure première équipe : {list(teams[0].keys())}")
                    
                    # Extraire les noms d'équipes
                    print(f"\n📋 ÉQUIPES TROUVÉES :")
                    for i, team in enumerate(teams):
                        # Vérifier le type de données
                        if isinstance(team, dict):
                            team_name = team.get('name', 'N/A')
                            team_id = team.get('id', 'N/A')
                            owner = team.get('owners', [{}])[0].get('displayName', 'N/A') if team.get('owners') else 'N/A'
                        else:
                            # Si c'est une string, l'afficher directement
                            team_name = str(team)
                            team_id = 'N/A'
                            owner = 'N/A'
                        
                        print(f"   {i+1}. {team_name} (ID: {team_id}) - {owner}")
                        
                        # Vérifier si c'est votre équipe
                        if 'Neon Cobras' in str(team_name) or 'Cobras' in str(team_name):
                            print(f"      🎉 TROUVÉ ! Votre équipe : {team_name}")
            
            # Analyser les paramètres
            if 'settings' in data:
                settings = data['settings']
                print(f"\n⚙️ PARAMÈTRES DE LIGUE :")
                print(f"   Nom : {settings.get('name', 'N/A')}")
                print(f"   Type : {settings.get('scoringType', 'N/A')}")
                print(f"   Saison : {settings.get('seasonId', 'N/A')}")
                print(f"   Équipes : {settings.get('size', 'N/A')}")
            
            # Analyser les joueurs
            if 'teams' in data and data['teams']:
                first_team = data['teams'][0]
                if 'roster' in first_team:
                    roster = first_team['roster']
                    print(f"\n👥 JOUEURS (Première équipe) :")
                    for i, player in enumerate(roster[:5]):  # Top 5
                        player_name = player.get('playerPoolEntry', {}).get('player', {}).get('fullName', 'N/A')
                        position = player.get('playerPoolEntry', {}).get('player', {}).get('defaultPositionId', 'N/A')
                        print(f"   {i+1}. {player_name} - {position}")
            
            return data
            
        else:
            print(f"❌ Erreur : {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return None

def create_processed_data(raw_data):
    """Crée des données traitées à partir des données brutes"""
    print(f"\n📊 CRÉATION DE DONNÉES TRAITÉES")
    print("=" * 50)
    
    if not raw_data:
        print("❌ Pas de données à traiter")
        return None
    
    # Traitement des données
    processed_data = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'league_info': {
            'league_id': 1557635339,
            'season': 2026,
            'name': raw_data.get('settings', {}).get('name', 'Ma Ligue'),
            'scoring_type': raw_data.get('settings', {}).get('scoringType', 'roto'),
            'total_teams': len(raw_data.get('teams', [])),
            'source': 'ESPN API Endpoint'
        },
        'teams': [],
        'my_team': None
    }
    
    # Traitement des équipes
    for team in raw_data.get('teams', []):
        team_data = {
            'team_id': team.get('id', 'N/A'),
            'team_name': team.get('name', 'N/A'),
            'manager': team.get('owners', [{}])[0].get('displayName', 'N/A') if team.get('owners') else 'N/A',
            'is_my_team': 'Neon Cobras' in team.get('name', '') or 'Cobras' in team.get('name', ''),
            'ranking': team.get('rank', 'N/A'),
            'points': team.get('points', 0),
            'rebounds': team.get('rebounds', 0),
            'assists': team.get('assists', 0),
            'steals': team.get('steals', 0),
            'blocks': team.get('blocks', 0),
            'fg_percentage': team.get('fieldGoalPercentage', 0),
            'ft_percentage': team.get('freeThrowPercentage', 0),
            'three_pointers': team.get('threePointersMade', 0),
            'turnovers': team.get('turnovers', 0)
        }
        
        processed_data['teams'].append(team_data)
        
        if team_data['is_my_team']:
            processed_data['my_team'] = team_data
    
    # Sauvegarde des données traitées
    filename = f"espn_processed_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Données traitées sauvegardées : {filename}")
    
    # Affichage des résultats
    print(f"\n🏀 RÉSULTATS TRAITÉS")
    print("=" * 50)
    
    if processed_data['my_team']:
        my_team = processed_data['my_team']
        print(f"👑 MON ÉQUIPE : {my_team['team_name']}")
        print(f"📈 RANG : {my_team['ranking']}")
        print(f"⚡ POINTS : {my_team['points']:.1f}")
        print(f"📊 REBONDS : {my_team['rebounds']:.1f}")
        print(f"🎯 ASSISTS : {my_team['assists']:.1f}")
        print(f"🔥 STEALS : {my_team['steals']:.1f}")
        print(f"🛡️ BLOCKS : {my_team['blocks']:.1f}")
    else:
        print(f"⚠️ Votre équipe 'Neon Cobras 99' non trouvée")
        print(f"📋 Équipes disponibles :")
        for team in processed_data['teams'][:5]:
            print(f"   - {team['team_name']} ({team['manager']})")
    
    print(f"\n✅ EXTRACTION TERMINÉE!")
    print(f"📁 Fichiers créés :")
    print(f"   📊 Données brutes : espn_raw_data_*.json")
    print(f"   📋 Données traitées : espn_processed_data_*.json")
    
    return processed_data

def main():
    """Fonction principale"""
    print("🚀 EXTRACTION AMÉLIORÉE ESPN")
    print("=" * 60)
    
    # Étape 1 : Extraire les données brutes
    raw_data = extract_league_data()
    
    if raw_data:
        # Étape 2 : Traiter les données
        processed_data = create_processed_data(raw_data)
        
        if processed_data:
            print(f"\n🎉 SUCCÈS ! Données ESPN extraites et traitées")
            print("💡 Vous pouvez maintenant utiliser ces données")
        else:
            print(f"\n❌ Erreur dans le traitement des données")
    else:
        print(f"\n❌ Erreur dans l'extraction des données")

if __name__ == "__main__":
    main()
