#!/usr/bin/env python3
"""
Trouver le Vrai ID de Ligue
Script pour tester différents IDs de ligue
"""

from espn_api.basketball import League
import requests
from datetime import datetime

def test_league_id(league_id, season):
    """Test un ID de ligue spécifique"""
    try:
        print(f"🏀 Test ID {league_id} - Saison {season}")
        league = League(league_id=league_id, year=season)
        
        print(f"   ✅ Connecté : {league.settings.name}")
        print(f"   👥 Équipes : {len(league.teams)}")
        print(f"   🏆 Type : {league.settings.scoring_type}")
        
        # Vérifier si c'est votre ligue
        team_names = [team.team_name for team in league.teams]
        if "Neon Cobras 99" in team_names:
            print(f"   🎉 TROUVÉ ! Votre équipe 'Neon Cobras 99' est dans cette ligue !")
            return True
        else:
            print(f"   ⚠️ Votre équipe 'Neon Cobras 99' non trouvée")
            print(f"   📋 Équipes : {team_names[:3]}...")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        return False

def test_common_league_ids():
    """Test des IDs de ligue courants"""
    print("🔍 TEST D'IDS DE LIGUE COURANTS")
    print("=" * 50)
    
    # IDs courants à tester
    common_ids = [
        1557635339,  # Votre ID actuel
        1557635340,  # ID + 1
        1557635338,  # ID - 1
        123456789,   # ID générique
        987654321,   # Autre ID générique
        555555555,   # Autre ID générique
        111111111,   # Autre ID générique
        222222222,   # Autre ID générique
    ]
    
    seasons = [2025, 2024, 2023]
    
    for league_id in common_ids:
        for season in seasons:
            success = test_league_id(league_id, season)
            if success:
                print(f"\n🎉 SUCCÈS ! ID {league_id} - Saison {season} fonctionne")
                return league_id, season
    
    print(f"\n❌ Aucun ID testé ne fonctionne")
    return None, None

def test_url_parsing():
    """Test de parsing d'URL ESPN"""
    print(f"\n🌐 TEST PARSING URL ESPN")
    print("=" * 50)
    
    # URLs ESPN à tester
    test_urls = [
        "https://fantasy.espn.com/basketball/league/standings?leagueId=1557635339&seasonId=2025",
        "https://fantasy.espn.com/basketball/league/standings?leagueId=1557635339&seasonId=2024",
        "https://fantasy.espn.com/basketball/league/standings?leagueId=1557635339&seasonId=2023",
    ]
    
    for url in test_urls:
        try:
            print(f"\n🌐 Test URL : {url}")
            response = requests.get(url, timeout=10)
            print(f"   Status : {response.status_code}")
            
            if response.status_code == 200:
                # Chercher des indices de ligue dans le HTML
                html_content = response.text.lower()
                
                if "league" in html_content:
                    print(f"   ✅ Contient 'league'")
                if "team" in html_content:
                    print(f"   ✅ Contient 'team'")
                if "standings" in html_content:
                    print(f"   ✅ Contient 'standings'")
                if "neon cobras" in html_content:
                    print(f"   🎉 TROUVÉ ! Contient 'Neon Cobras'")
                if "basketball" in html_content:
                    print(f"   ✅ Contient 'basketball'")
                
                # Chercher l'ID de ligue dans le HTML
                if "leagueId" in html_content:
                    print(f"   ✅ Contient 'leagueId'")
                    # Extraire l'ID de ligue du HTML
                    import re
                    league_id_match = re.search(r'leagueId["\']?\s*:\s*["\']?(\d+)', html_content)
                    if league_id_match:
                        found_id = league_id_match.group(1)
                        print(f"   🎯 ID trouvé dans HTML : {found_id}")
            else:
                print(f"   ❌ URL non accessible")
                
        except Exception as e:
            print(f"   ❌ Erreur : {e}")

def main():
    """Fonction principale"""
    print("🔍 TROUVER LE VRAI ID DE LIGUE")
    print("=" * 60)
    
    # Test 1 : IDs courants
    league_id, season = test_common_league_ids()
    
    if league_id:
        print(f"\n🎉 SUCCÈS ! ID {league_id} - Saison {season} fonctionne")
        print("💡 Utilisez cet ID dans vos scripts")
    else:
        # Test 2 : Parsing URL
        test_url_parsing()
        
        print(f"\n💡 SOLUTIONS POUR TROUVER VOTRE ID :")
        print("   1. Aller sur ESPN Fantasy")
        print("   2. Ouvrir votre ligue")
        print("   3. Regarder l'URL complète")
        print("   4. Copier l'ID après 'leagueId='")
        print("   5. Tester avec cet ID")

if __name__ == "__main__":
    main()
