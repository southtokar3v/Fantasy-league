#!/usr/bin/env python3
"""
Test Nouvel Endpoint ESPN
Script pour tester le nouvel endpoint ESPN API
"""

import requests
import json
from datetime import datetime

def test_new_endpoint():
    """Test du nouvel endpoint ESPN"""
    print("🔍 TEST NOUVEL ENDPOINT ESPN")
    print("=" * 50)
    
    # Configuration
    LEAGUE_ID = 1557635339
    SEASON = 2026
    
    # Nouvel endpoint
    endpoint = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/FBA/seasons/{SEASON}/segments/0/leagues/{LEAGUE_ID}"
    
    print(f"🌐 Endpoint : {endpoint}")
    
    try:
        # Test de l'endpoint
        response = requests.get(endpoint, timeout=10)
        print(f"📊 Status Code : {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Succès ! Données récupérées")
            
            # Analyser les données
            if 'settings' in data:
                settings = data['settings']
                print(f"🏀 Ligue : {settings.get('name', 'N/A')}")
                print(f"👥 Équipes : {len(data.get('teams', []))}")
                print(f"🏆 Type : {settings.get('scoringType', 'N/A')}")
                
                # Vérifier si c'est votre ligue
                teams = data.get('teams', [])
                for team in teams:
                    if 'Neon Cobras 99' in team.get('name', ''):
                        print(f"🎉 TROUVÉ ! Votre équipe 'Neon Cobras 99' est dans cette ligue !")
                        return True
                
                print(f"⚠️ Votre équipe 'Neon Cobras 99' non trouvée")
                print(f"📋 Équipes disponibles :")
                for team in teams[:5]:
                    print(f"   - {team.get('name', 'N/A')}")
            
            return True
            
        else:
            print(f"❌ Erreur : {response.status_code}")
            print(f"📄 Réponse : {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False

def test_alternative_endpoints():
    """Test d'endpoints alternatifs"""
    print(f"\n🔍 TEST ENDPOINTS ALTERNATIFS")
    print("=" * 50)
    
    LEAGUE_ID = 1557635339
    SEASON = 2026
    
    # Endpoints alternatifs
    endpoints = [
        f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/FBA/seasons/{SEASON}/segments/0/leagues/{LEAGUE_ID}",
        f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/FBA/seasons/{SEASON}/segments/1/leagues/{LEAGUE_ID}",
        f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/FBA/seasons/{SEASON}/segments/2/leagues/{LEAGUE_ID}",
        f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/FBA/seasons/{SEASON}/segments/3/leagues/{LEAGUE_ID}",
    ]
    
    for i, endpoint in enumerate(endpoints):
        try:
            print(f"\n🌐 Test endpoint {i+1} : {endpoint}")
            response = requests.get(endpoint, timeout=10)
            print(f"   Status : {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Succès ! Données récupérées")
                
                if 'settings' in data:
                    settings = data['settings']
                    print(f"   🏀 Ligue : {settings.get('name', 'N/A')}")
                    print(f"   👥 Équipes : {len(data.get('teams', []))}")
                    
                    # Vérifier si c'est votre ligue
                    teams = data.get('teams', [])
                    for team in teams:
                        if 'Neon Cobras 99' in team.get('name', ''):
                            print(f"   🎉 TROUVÉ ! Votre équipe 'Neon Cobras 99' est dans cette ligue !")
                            return endpoint
                
                print(f"   ⚠️ Votre équipe 'Neon Cobras 99' non trouvée")
            else:
                print(f"   ❌ Erreur : {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erreur : {e}")
    
    return None

def test_scraping_alternative():
    """Test de scraping alternatif"""
    print(f"\n🔍 TEST SCRAPING ALTERNATIF")
    print("=" * 50)
    
    # URLs ESPN à scraper
    urls = [
        "https://fantasy.espn.com/basketball/league/standings?leagueId=1557635339&seasonId=2026",
        "https://fantasy.espn.com/basketball/league/settings?leagueId=1557635339&seasonId=2026",
        "https://fantasy.espn.com/basketball/league/roster?leagueId=1557635339&seasonId=2026",
    ]
    
    for url in urls:
        try:
            print(f"\n🌐 Test scraping : {url}")
            response = requests.get(url, timeout=10)
            print(f"   Status : {response.status_code}")
            
            if response.status_code == 200:
                html_content = response.text
                
                # Chercher des indices de ligue
                if "league" in html_content.lower():
                    print(f"   ✅ Contient 'league'")
                if "team" in html_content.lower():
                    print(f"   ✅ Contient 'team'")
                if "neon cobras" in html_content.lower():
                    print(f"   🎉 TROUVÉ ! Contient 'Neon Cobras'")
                if "basketball" in html_content.lower():
                    print(f"   ✅ Contient 'basketball'")
                
                print(f"   📊 Taille HTML : {len(html_content)} caractères")
                print(f"   ✅ Scraping possible")
            else:
                print(f"   ❌ Erreur : {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erreur : {e}")

def main():
    """Fonction principale"""
    print("🚀 TEST NOUVEL ENDPOINT ESPN")
    print("=" * 60)
    
    # Test 1 : Nouvel endpoint
    success = test_new_endpoint()
    
    if success:
        print(f"\n🎉 SUCCÈS ! Nouvel endpoint fonctionne")
        print("💡 Vous pouvez utiliser cet endpoint dans vos scripts")
    else:
        # Test 2 : Endpoints alternatifs
        working_endpoint = test_alternative_endpoints()
        
        if working_endpoint:
            print(f"\n🎉 SUCCÈS ! Endpoint alternatif fonctionne : {working_endpoint}")
        else:
            # Test 3 : Scraping alternatif
            test_scraping_alternative()
            
            print(f"\n💡 SOLUTIONS ALTERNATIVES :")
            print("   1. Utiliser le scraping direct des pages ESPN")
            print("   2. Attendre que l'API ESPN soit corrigée")
            print("   3. Utiliser des données manuelles en attendant")

if __name__ == "__main__":
    main()
