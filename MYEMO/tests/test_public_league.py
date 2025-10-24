#!/usr/bin/env python3
"""
Test avec Ligue Publique
Script pour tester avec une ligue publique ESPN
"""

from espn_api.basketball import League
import json
from datetime import datetime

def test_public_leagues():
    """Test avec des ligues publiques connues"""
    print("🏀 TEST AVEC LIGUES PUBLIQUES")
    print("=" * 50)
    
    # IDs de ligues publiques connues (exemples)
    public_leagues = [
        (123456789, 2025),  # ID générique
        (987654321, 2025),  # Autre ID générique
        (555555555, 2025),  # Autre ID générique
    ]
    
    for league_id, season in public_leagues:
        try:
            print(f"\n🏀 Test ligue {league_id} - Saison {season}")
            league = League(league_id=league_id, year=season)
            
            print(f"✅ Connecté : {league.settings.name}")
            print(f"👥 Équipes : {len(league.teams)}")
            print(f"🏆 Type : {league.settings.scoring_type}")
            
            # Afficher les équipes
            print(f"\n📋 ÉQUIPES :")
            for i, team in enumerate(league.teams[:5]):
                print(f"   {i+1}. {team.team_name} - {team.owner}")
            
            print(f"\n🎉 SUCCÈS ! Cette ligue fonctionne")
            return league_id, season
            
        except Exception as e:
            print(f"❌ Erreur : {e}")
            continue
    
    print(f"\n❌ Aucune ligue publique trouvée")
    return None, None

def create_demo_data():
    """Crée des données de démonstration"""
    print(f"\n📊 CRÉATION DE DONNÉES DE DÉMONSTRATION")
    print("=" * 50)
    
    # Données de démonstration
    demo_data = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'league_info': {
            'league_id': 1557635339,
            'season': 2025,
            'name': 'Ma Ligue Privée (Démo)',
            'scoring_type': 'roto',
            'total_teams': 13
        },
        'teams': [
            {
                'team_name': 'Neon Cobras 99',
                'manager': 'Manager',
                'is_my_team': True,
                'ranking': 3,
                'wins': 8,
                'losses': 2,
                'points': 1250.5
            },
            {
                'team_name': 'Équipe Alpha',
                'manager': 'Manager2',
                'is_my_team': False,
                'ranking': 1,
                'wins': 10,
                'losses': 0,
                'points': 1300.2
            },
            {
                'team_name': 'Équipe Beta',
                'manager': 'Manager3',
                'is_my_team': False,
                'ranking': 2,
                'wins': 9,
                'losses': 1,
                'points': 1280.5
            }
        ]
    }
    
    # Sauvegarde
    filename = f"demo_espn_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(demo_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Données de démonstration créées : {filename}")
    
    # Affichage des résultats
    print(f"\n🏀 RÉSULTATS DE DÉMONSTRATION")
    print("=" * 50)
    
    if demo_data['teams']:
        my_team = next((team for team in demo_data['teams'] if team['is_my_team']), None)
        if my_team:
            print(f"👑 MON ÉQUIPE : {my_team['team_name']}")
            print(f"📈 RANG : {my_team['ranking']}")
            print(f"🏆 VICTOIRES : {my_team['wins']}")
            print(f"❌ DÉFAITES : {my_team['losses']}")
            print(f"⚡ POINTS : {my_team['points']:.1f}")
        
        print(f"\n🏆 CLASSEMENT TOP 3 :")
        sorted_teams = sorted(demo_data['teams'], key=lambda x: x['ranking'])
        for team in sorted_teams:
            marker = "👑" if team['is_my_team'] else "  "
            print(f"{marker} {team['ranking']}. {team['team_name']} - {team['points']:.1f} pts")
    
    print(f"\n✅ DÉMONSTRATION TERMINÉE AVEC SUCCÈS!")
    print(f"📁 Fichier créé : {filename}")
    print("💡 Ce sont des données de démonstration pour votre ligue privée")

def main():
    """Fonction principale"""
    print("🆓 ESPN NBA Fantasy - Test Ligue Privée")
    print("=" * 60)
    
    # Test avec ligues publiques
    league_id, season = test_public_leagues()
    
    if league_id:
        print(f"\n🎉 Ligue publique trouvée : {league_id} - Saison {season}")
        print("💡 Vous pouvez utiliser cette ligue pour tester")
    else:
        print(f"\n📊 Création de données de démonstration...")
        create_demo_data()
        
        print(f"\n💡 SOLUTIONS POUR VOTRE LIGUE PRIVÉE :")
        print("   1. Demander au commish de rendre la ligue publique")
        print("   2. Utiliser des données de démonstration")
        print("   3. Créer une ligue publique de test")
        print("   4. Utiliser l'export manuel d'ESPN")

if __name__ == "__main__":
    main()
