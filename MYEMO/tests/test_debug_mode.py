#!/usr/bin/env python3
"""
Test avec Debug Mode - Version 0.45.1
Script pour tester avec le mode debug de l'API ESPN
"""

from espn_api.basketball import League
import json
from datetime import datetime

def test_with_debug_mode():
    """Test avec le mode debug activé"""
    print("🔍 TEST AVEC DEBUG MODE - Version 0.45.1")
    print("=" * 60)
    
    # Configuration
    LEAGUE_ID = 1557635339
    SEASON = 2025
    
    try:
        print(f"🏀 Test ligue {LEAGUE_ID} - Saison {SEASON}")
        print("🔍 Mode debug activé - Vérifiez les logs ci-dessous...")
        
        # Test avec debug mode
        league = League(league_id=LEAGUE_ID, year=SEASON, debug=True)
        
        print(f"✅ Connecté : {league.settings.name}")
        print(f"👥 Équipes : {len(league.teams)}")
        print(f"🏆 Type : {league.settings.scoring_type}")
        
        # Test des données
        if league.teams:
            print(f"\n📋 ÉQUIPES :")
            for i, team in enumerate(league.teams[:5]):
                print(f"   {i+1}. {team.team_name} - {team.owner}")
            
            # Test des joueurs
            if league.teams[0].roster:
                print(f"\n👥 JOUEURS (Première équipe) :")
                for i, player in enumerate(league.teams[0].roster[:3]):
                    print(f"   {i+1}. {player.name} - {player.position}")
        
        print(f"\n🎉 SUCCÈS avec debug mode !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur avec debug mode : {e}")
        print(f"🔍 Vérifiez les logs ci-dessus pour plus de détails")
        return False

def test_different_seasons():
    """Test avec différentes saisons"""
    print(f"\n🏀 TEST DIFFÉRENTES SAISONS")
    print("=" * 50)
    
    seasons = [2025, 2024, 2023]
    LEAGUE_ID = 1557635339
    
    for season in seasons:
        try:
            print(f"\n🏀 Test saison {season}")
            league = League(league_id=LEAGUE_ID, year=season)
            
            print(f"   ✅ Connecté : {league.settings.name}")
            print(f"   👥 Équipes : {len(league.teams)}")
            print(f"   🏆 Type : {league.settings.scoring_type}")
            
            print(f"   🎉 SUCCÈS avec saison {season} !")
            return season
            
        except Exception as e:
            print(f"   ❌ Erreur saison {season} : {e}")
            continue
    
    print(f"\n❌ Aucune saison ne fonctionne")
    return None

def main():
    """Fonction principale"""
    print("🚀 ESPN API - Test Version 0.45.1")
    print("=" * 60)
    
    # Test 1 : Debug mode
    debug_success = test_with_debug_mode()
    
    if debug_success:
        print(f"\n🎉 SUCCÈS ! Votre ligue fonctionne avec la version 0.45.1")
        print("💡 Vous pouvez maintenant utiliser le script principal")
    else:
        # Test 2 : Différentes saisons
        working_season = test_different_seasons()
        
        if working_season:
            print(f"\n🎉 SUCCÈS ! Saison {working_season} fonctionne")
            print(f"💡 Utilisez la saison {working_season} dans vos scripts")
        else:
            print(f"\n❌ Aucune configuration ne fonctionne")
            print("💡 Vérifiez que la ligue est bien 'visible au public'")

if __name__ == "__main__":
    main()
