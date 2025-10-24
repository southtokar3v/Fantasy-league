#!/usr/bin/env python3
"""
Version Ultra-Simple - 100% Gratuit
Juste les données ESPN, pas de Google Sheets
Export vers fichiers locaux uniquement
"""

from espn_api.basketball import League
import json
from datetime import datetime

# Configuration
LEAGUE_ID = 1557635339
SEASON = 2025
MY_TEAM_NAME = "Neon Cobras 99"

def main():
    """Version ultra-simple - 100% gratuit"""
    print("🆓 ESPN NBA Fantasy - Version Ultra-Simple")
    print("=" * 50)
    print("✅ 100% Gratuit - Aucune configuration requise")
    print()
    
    try:
        # Connexion ESPN
        print("🏀 Connexion à ESPN...")
        league = League(league_id=LEAGUE_ID, year=SEASON)
        
        print(f"✅ Connecté : {league.settings.name}")
        print(f"👥 {len(league.teams)} équipes")
        
        # Collecte des données
        print("📊 Collecte des données...")
        
        # Données de base
        data = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'league': {
                'name': league.settings.name,
                'scoring_type': league.settings.scoring_type,
                'total_teams': len(league.teams)
            },
            'teams': [],
            'my_team': None
        }
        
        # Équipes
        for team in league.teams:
            team_data = {
                'name': team.team_name,
                'manager': team.owner,
                'ranking': team.standing,
                'wins': team.wins,
                'losses': team.losses,
                'points': team.points_for,
                'is_my_team': team.team_name == MY_TEAM_NAME
            }
            
            data['teams'].append(team_data)
            
            if team.team_name == MY_TEAM_NAME:
                data['my_team'] = team_data
        
        # Sauvegarde
        filename = f"espn_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Affichage des résultats
        print("\n" + "="*50)
        print("🏀 RÉSULTATS")
        print("="*50)
        
        if data['my_team']:
            my_team = data['my_team']
            print(f"👑 MON ÉQUIPE : {my_team['name']}")
            print(f"📈 RANG : {my_team['ranking']}")
            print(f"🏆 VICTOIRES : {my_team['wins']}")
            print(f"❌ DÉFAITES : {my_team['losses']}")
            print(f"⚡ POINTS : {my_team['points']:.1f}")
        
        print(f"\n🏆 CLASSEMENT TOP 5 :")
        sorted_teams = sorted(data['teams'], key=lambda x: x['ranking'])
        for team in sorted_teams[:5]:
            marker = "👑" if team['is_my_team'] else "  "
            print(f"{marker} {team['ranking']}. {team['name']} - {team['points']:.1f} pts")
        
        print(f"\n✅ TERMINÉ AVEC SUCCÈS!")
        print(f"📁 Fichier créé : {filename}")
        print("💡 Ouvrez le fichier JSON pour voir toutes les données")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        print("💡 Vérifiez votre connexion internet")

if __name__ == "__main__":
    main()
