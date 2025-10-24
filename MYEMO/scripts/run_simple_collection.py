#!/usr/bin/env python3
"""
Script Simple de Collecte ESPN NBA Fantasy
Point d'entrée facile pour tester le système
"""

import json
from datetime import datetime
import logging
from espn_api.basketball import League

# Configuration
LEAGUE_ID = 1557635339
SEASON = 2026
MY_TEAM_NAME = "Neon Cobras 99"

def setup_logging():
    """Configure le logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('espn_collection.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def test_espn_connection():
    """Test la connexion ESPN"""
    try:
        league = League(league_id=LEAGUE_ID, year=SEASON)
        logger.info(f"✅ Connexion ESPN réussie: {league.settings.name}")
        logger.info(f"👥 {len(league.teams)} équipes")
        return league
    except Exception as e:
        logger.error(f"❌ Erreur connexion ESPN: {e}")
        return None

def collect_basic_data(league):
    """Collecte les données de base"""
    try:
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Données de base
        data = {
            'date': current_date,
            'league_info': {
                'league_id': LEAGUE_ID,
                'season': SEASON,
                'name': league.settings.name,
                'scoring_type': league.settings.scoring_type,
                'total_teams': len(league.teams)
            },
            'teams': [],
            'my_team': None
        }
        
        # Collecte des équipes
        for team in league.teams:
            team_data = {
                'team_id': team.team_id,
                'team_name': team.team_name,
                'manager': team.owner,
                'is_my_team': team.team_name == MY_TEAM_NAME,
                'ranking': team.standing,
                'wins': team.wins,
                'losses': team.losses,
                'points_for': team.points_for
            }
            
            data['teams'].append(team_data)
            
            # Identifier mon équipe
            if team.team_name == MY_TEAM_NAME:
                data['my_team'] = team_data
        
        return data
        
    except Exception as e:
        logger.error(f"❌ Erreur collecte données: {e}")
        return None

def save_data(data):
    """Sauvegarde les données"""
    try:
        filename = f"espn_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"💾 Données sauvegardées: {filename}")
        return filename
        
    except Exception as e:
        logger.error(f"❌ Erreur sauvegarde: {e}")
        return None

def display_results(data):
    """Affiche les résultats"""
    print("\n" + "="*60)
    print("🏀 RÉSULTATS DE LA COLLECTE")
    print("="*60)
    
    if data:
        print(f"\n📊 LIGUE: {data['league_info']['name']}")
        print(f"👥 ÉQUIPES: {data['league_info']['total_teams']}")
        print(f"📅 DATE: {data['date']}")
        
        if data['my_team']:
            my_team = data['my_team']
            print(f"\n👑 MON ÉQUIPE: {my_team['team_name']}")
            print(f"📈 RANG: {my_team['ranking']}")
            print(f"🏆 VICTOIRES: {my_team['wins']}")
            print(f"❌ DÉFAITES: {my_team['losses']}")
            print(f"⚡ POINTS: {my_team['points_for']:.1f}")
        
        print(f"\n🏆 CLASSEMENT TOP 5:")
        sorted_teams = sorted(data['teams'], key=lambda x: x['ranking'])
        for i, team in enumerate(sorted_teams[:5]):
            marker = "👑" if team['is_my_team'] else "  "
            print(f"{marker} {team['ranking']}. {team['team_name']} - {team['points_for']:.1f} pts")
        
        print(f"\n✅ COLLECTE TERMINÉE AVEC SUCCÈS!")
    else:
        print("❌ ÉCHEC DE LA COLLECTE")

def main():
    """Fonction principale"""
    global logger
    logger = setup_logging()
    
    print("🚀 ESPN NBA Fantasy - Collecte Simple")
    print("=" * 50)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🏀 Ligue: {LEAGUE_ID} - Saison {SEASON}")
    print(f"👑 Mon équipe: {MY_TEAM_NAME}")
    print()
    
    try:
        # Test de connexion ESPN
        logger.info("🔧 Test de connexion ESPN...")
        league = test_espn_connection()
        
        if not league:
            print("❌ Impossible de se connecter à ESPN")
            return
        
        # Collecte des données
        logger.info("📊 Collecte des données...")
        data = collect_basic_data(league)
        
        if not data:
            print("❌ Échec de la collecte des données")
            return
        
        # Sauvegarde
        logger.info("💾 Sauvegarde des données...")
        filename = save_data(data)
        
        # Affichage des résultats
        display_results(data)
        
        if filename:
            print(f"\n📁 Fichier créé: {filename}")
        
    except Exception as e:
        logger.error(f"❌ Erreur dans le script principal: {e}")
        print(f"❌ ERREUR: {e}")

if __name__ == "__main__":
    main()
