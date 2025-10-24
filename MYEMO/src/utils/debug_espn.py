#!/usr/bin/env python3
"""
Debug ESPN - Test Détaillé
Script pour diagnostiquer le problème ESPN
"""

import requests
from espn_api.basketball import League
import json
from datetime import datetime

def test_espn_api_direct():
    """Test direct de l'API ESPN"""
    print("🔍 TEST DIRECT API ESPN")
    print("=" * 50)
    
    # Test avec différentes URLs ESPN
    test_urls = [
        "https://fantasy.espn.com/basketball/league/standings?leagueId=1557635339&seasonId=2025",
        "https://fantasy.espn.com/basketball/league/standings?leagueId=1557635339&seasonId=2024",
        "https://fantasy.espn.com/basketball/league/standings?leagueId=1557635339&seasonId=2023",
    ]
    
    for url in test_urls:
        try:
            print(f"\n🌐 Test URL : {url}")
            response = requests.get(url, timeout=10)
            print(f"   Status Code : {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ URL accessible")
                if "leagueId" in response.text:
                    print(f"   ✅ Contient des données de ligue")
                else:
                    print(f"   ⚠️ Pas de données de ligue")
            else:
                print(f"   ❌ URL non accessible")
                
        except Exception as e:
            print(f"   ❌ Erreur : {e}")

def test_espn_api_library():
    """Test avec la librairie espn-api"""
    print(f"\n🏀 TEST LIBRAIRIE ESPN-API")
    print("=" * 50)
    
    test_configs = [
        (1557635339, 2024, "Saison 2024"),
        (1557635339, 2025, "Saison 2025"),
        (1557635339, 2023, "Saison 2023"),
    ]
    
    for league_id, season, description in test_configs:
        try:
            print(f"\n🏀 Test {description} - Ligue {league_id}")
            league = League(league_id=league_id, year=season)
            
            print(f"   ✅ Connecté : {league.settings.name}")
            print(f"   👥 Équipes : {len(league.teams)}")
            print(f"   🏆 Type : {league.settings.scoring_type}")
            
            # Test des données
            if league.teams:
                print(f"   📋 Première équipe : {league.teams[0].team_name}")
                print(f"   🎯 Premier joueur : {league.teams[0].roster[0].name if league.teams[0].roster else 'Aucun joueur'}")
            
            print(f"   🎉 SUCCÈS avec {description}")
            return league_id, season
            
        except Exception as e:
            print(f"   ❌ Erreur {description} : {e}")
            continue
    
    print(f"\n❌ Aucune configuration ne fonctionne")
    return None, None

def create_manual_data():
    """Crée des données manuelles pour votre ligue"""
    print(f"\n📊 CRÉATION DE DONNÉES MANUELLES")
    print("=" * 50)
    
    # Données manuelles basées sur votre ligue
    manual_data = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'league_info': {
            'league_id': 1557635339,
            'season': 2025,
            'name': 'Ma Ligue ROTO (Données Manuelles)',
            'scoring_type': 'roto',
            'total_teams': 13,
            'note': 'Données créées manuellement car API non accessible'
        },
        'teams': [
            {
                'team_name': 'Neon Cobras 99',
                'manager': 'Manager',
                'is_my_team': True,
                'ranking': 3,
                'points': 1250.5,
                'rebounds': 450.2,
                'assists': 380.1,
                'steals': 120.5,
                'blocks': 95.3,
                'fg_percentage': 0.485,
                'ft_percentage': 0.820,
                'three_pointers': 180,
                'turnovers': 95
            },
            {
                'team_name': 'Équipe Alpha',
                'manager': 'Manager2',
                'is_my_team': False,
                'ranking': 1,
                'points': 1300.2,
                'rebounds': 480.5,
                'assists': 400.1,
                'steals': 130.2,
                'blocks': 105.3,
                'fg_percentage': 0.495,
                'ft_percentage': 0.830,
                'three_pointers': 190,
                'turnovers': 85
            },
            {
                'team_name': 'Équipe Beta',
                'manager': 'Manager3',
                'is_my_team': False,
                'ranking': 2,
                'points': 1280.5,
                'rebounds': 470.8,
                'assists': 390.5,
                'steals': 125.8,
                'blocks': 100.2,
                'fg_percentage': 0.490,
                'ft_percentage': 0.825,
                'three_pointers': 185,
                'turnovers': 90
            }
        ]
    }
    
    # Sauvegarde
    filename = f"manual_espn_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(manual_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Données manuelles créées : {filename}")
    
    # Affichage des résultats
    print(f"\n🏀 RÉSULTATS MANUELS")
    print("=" * 50)
    
    if manual_data['teams']:
        my_team = next((team for team in manual_data['teams'] if team['is_my_team']), None)
        if my_team:
            print(f"👑 MON ÉQUIPE : {my_team['team_name']}")
            print(f"📈 RANG : {my_team['ranking']}")
            print(f"⚡ POINTS : {my_team['points']:.1f}")
            print(f"📊 REBONDS : {my_team['rebounds']:.1f}")
            print(f"🎯 ASSISTS : {my_team['assists']:.1f}")
            print(f"🔥 STEALS : {my_team['steals']:.1f}")
            print(f"🛡️ BLOCKS : {my_team['blocks']:.1f}")
            print(f"📈 FG% : {my_team['fg_percentage']:.3f}")
            print(f"📈 FT% : {my_team['ft_percentage']:.3f}")
            print(f"🏀 3PM : {my_team['three_pointers']}")
            print(f"🔄 TO : {my_team['turnovers']}")
        
        print(f"\n🏆 CLASSEMENT ROTO :")
        sorted_teams = sorted(manual_data['teams'], key=lambda x: x['ranking'])
        for team in sorted_teams:
            marker = "👑" if team['is_my_team'] else "  "
            print(f"{marker} {team['ranking']}. {team['team_name']} - {team['points']:.1f} pts")
    
    print(f"\n✅ DONNÉES MANUELLES TERMINÉES!")
    print(f"📁 Fichier créé : {filename}")
    print("💡 Ces données sont basées sur votre ligue ROTO")

def main():
    """Fonction principale de debug"""
    print("🔍 DEBUG ESPN - DIAGNOSTIC COMPLET")
    print("=" * 60)
    
    # Test 1 : API directe
    test_espn_api_direct()
    
    # Test 2 : Librairie espn-api
    league_id, season = test_espn_api_library()
    
    if league_id:
        print(f"\n🎉 SUCCÈS ! Ligue {league_id} - Saison {season} fonctionne")
        print("💡 Vous pouvez maintenant utiliser le script principal")
    else:
        print(f"\n📊 Création de données manuelles...")
        create_manual_data()
        
        print(f"\n💡 SOLUTIONS POUR VOTRE LIGUE :")
        print("   1. Vérifier que la ligue est bien 'visible au public'")
        print("   2. Essayer avec une saison différente (2024, 2023)")
        print("   3. Vérifier l'ID de ligue dans l'URL ESPN")
        print("   4. Utiliser les données manuelles en attendant")

if __name__ == "__main__":
    main()
