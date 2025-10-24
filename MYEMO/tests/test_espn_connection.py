#!/usr/bin/env python3
"""
Test de Connexion ESPN
Script pour tester différents IDs de ligue
"""

from espn_api.basketball import League
import json
from datetime import datetime

def test_league_connection(league_id, season):
    """Test la connexion à une ligue"""
    try:
        print(f"🏀 Test ligue {league_id} - Saison {season}")
        league = League(league_id=league_id, year=season)
        
        print(f"✅ Connecté : {league.settings.name}")
        print(f"👥 Équipes : {len(league.teams)}")
        print(f"🏆 Type : {league.settings.scoring_type}")
        
        # Afficher les équipes
        print(f"\n📋 ÉQUIPES :")
        for i, team in enumerate(league.teams[:5]):  # Top 5
            print(f"   {i+1}. {team.team_name} - {team.owner}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False

def main():
    """Test de différentes ligues"""
    print("🧪 TEST DE CONNEXION ESPN")
    print("=" * 50)
    
    # IDs de ligue à tester
    test_leagues = [
        (1557635339, 2024),  # Saison précédente
        (1557635339, 2025),  # Votre ligue
        (1557635339, 2023),  # Saison encore plus ancienne
        (123456789, 2024),   # ID générique
        (987654321, 2024),   # Autre ID générique
    ]
    
    for league_id, season in test_leagues:
        print(f"\n{'='*30}")
        success = test_league_connection(league_id, season)
        
        if success:
            print(f"🎉 SUCCÈS avec ligue {league_id} - Saison {season}")
            break
        else:
            print(f"❌ Échec avec ligue {league_id} - Saison {season}")
    
    print(f"\n{'='*50}")
    print("💡 Si aucun test ne fonctionne, vérifiez :")
    print("   - Votre connexion internet")
    print("   - L'ID de votre ligue ESPN")
    print("   - Les permissions de votre ligue")

if __name__ == "__main__":
    main()
