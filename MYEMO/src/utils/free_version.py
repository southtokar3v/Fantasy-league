#!/usr/bin/env python3
"""
Version Gratuite - ESPN NBA Fantasy
Collecte des données sans Google Sheets
Export vers fichiers locaux (JSON, CSV, Excel)
"""

import json
import csv
import pandas as pd
from datetime import datetime
import logging
from espn_api.basketball import League

# Configuration
LEAGUE_ID = 1557635339
SEASON = 2025
MY_TEAM_NAME = "Neon Cobras 99"

def setup_logging():
    """Configure le logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('espn_free.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def collect_espn_data():
    """Collecte les données ESPN"""
    try:
        logger.info("🏀 Connexion à ESPN...")
        league = League(league_id=LEAGUE_ID, year=SEASON)
        
        logger.info(f"✅ Connecté : {league.settings.name}")
        logger.info(f"👥 {len(league.teams)} équipes")
        
        return league
    except Exception as e:
        logger.error(f"❌ Erreur ESPN : {e}")
        return None

def extract_team_data(league):
    """Extrait les données des équipes"""
    teams_data = []
    
    for team in league.teams:
        team_info = {
            'team_id': team.team_id,
            'team_name': team.team_name,
            'manager': team.owner,
            'is_my_team': team.team_name == MY_TEAM_NAME,
            'ranking': team.standing,
            'wins': team.wins,
            'losses': team.losses,
            'ties': team.ties,
            'points_for': team.points_for,
            'points_against': team.points_against,
            'win_percentage': team.win_percentage
        }
        
        # Ajouter les joueurs
        team_info['players'] = []
        for player in team.roster:
            player_info = {
                'player_id': player.playerId,
                'name': player.name,
                'position': player.position,
                'team': player.proTeam,
                'status': 'active' if player.lineupSlot not in ['BE', 'IR'] else 'bench',
                'lineup_slot': player.lineupSlot,
                'points': player.total_points,
                'rebounds': player.rebounds,
                'assists': player.assists,
                'steals': player.steals,
                'blocks': player.blocks,
                'fg_percentage': player.field_goal_percentage,
                'ft_percentage': player.free_throw_percentage,
                'three_pointers': player.three_pointers_made,
                'turnovers': player.turnovers,
                'injury_status': getattr(player, 'injuryStatus', ''),
                'is_bench': player.lineupSlot in ['BE', 'IR']
            }
            team_info['players'].append(player_info)
        
        teams_data.append(team_info)
    
    return teams_data

def extract_transactions(league):
    """Extrait les transactions"""
    try:
        transactions = []
        for activity in league.recent_activity(25):
            transactions.append({
                'date': activity.date,
                'type': activity.type,
                'description': activity.description,
                'team': getattr(activity, 'team_name', 'N/A')
            })
        return transactions
    except Exception as e:
        logger.error(f"❌ Erreur transactions : {e}")
        return []

def save_to_json(data, filename):
    """Sauvegarde en JSON"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        logger.info(f"💾 JSON sauvegardé : {filename}")
    except Exception as e:
        logger.error(f"❌ Erreur sauvegarde JSON : {e}")

def save_to_csv(teams_data, filename):
    """Sauvegarde en CSV"""
    try:
        # Données des équipes
        teams_csv = []
        for team in teams_data:
            teams_csv.append({
                'team_id': team['team_id'],
                'team_name': team['team_name'],
                'manager': team['manager'],
                'is_my_team': team['is_my_team'],
                'ranking': team['ranking'],
                'wins': team['wins'],
                'losses': team['losses'],
                'points_for': team['points_for'],
                'win_percentage': team['win_percentage']
            })
        
        # Sauvegarde
        df = pd.DataFrame(teams_csv)
        df.to_csv(filename, index=False, encoding='utf-8')
        logger.info(f"💾 CSV sauvegardé : {filename}")
        
    except Exception as e:
        logger.error(f"❌ Erreur sauvegarde CSV : {e}")

def save_players_to_csv(teams_data, filename):
    """Sauvegarde des joueurs en CSV"""
    try:
        players_csv = []
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        for team in teams_data:
            for player in team['players']:
                players_csv.append({
                    'date': current_date,
                    'team_name': team['team_name'],
                    'is_my_team': team['is_my_team'],
                    'player_name': player['name'],
                    'position': player['position'],
                    'status': player['status'],
                    'is_bench': player['is_bench'],
                    'points': player['points'],
                    'rebounds': player['rebounds'],
                    'assists': player['assists'],
                    'steals': player['steals'],
                    'blocks': player['blocks'],
                    'fg_percentage': player['fg_percentage'],
                    'ft_percentage': player['ft_percentage'],
                    'three_pointers': player['three_pointers'],
                    'turnovers': player['turnovers'],
                    'injury_status': player['injury_status']
                })
        
        # Sauvegarde
        df = pd.DataFrame(players_csv)
        df.to_csv(filename, index=False, encoding='utf-8')
        logger.info(f"💾 Joueurs CSV sauvegardé : {filename}")
        
    except Exception as e:
        logger.error(f"❌ Erreur sauvegarde joueurs CSV : {e}")

def save_to_excel(teams_data, transactions, filename):
    """Sauvegarde en Excel"""
    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Feuille équipes
            teams_df = pd.DataFrame([
                {
                    'team_name': team['team_name'],
                    'manager': team['manager'],
                    'is_my_team': team['is_my_team'],
                    'ranking': team['ranking'],
                    'wins': team['wins'],
                    'losses': team['losses'],
                    'points_for': team['points_for']
                }
                for team in teams_data
            ])
            teams_df.to_excel(writer, sheet_name='Équipes', index=False)
            
            # Feuille joueurs
            players_data = []
            for team in teams_data:
                for player in team['players']:
                    players_data.append({
                        'team_name': team['team_name'],
                        'is_my_team': team['is_my_team'],
                        'player_name': player['name'],
                        'position': player['position'],
                        'status': player['status'],
                        'is_bench': player['is_bench'],
                        'points': player['points'],
                        'rebounds': player['rebounds'],
                        'assists': player['assists'],
                        'steals': player['steals'],
                        'blocks': player['blocks']
                    })
            
            players_df = pd.DataFrame(players_data)
            players_df.to_excel(writer, sheet_name='Joueurs', index=False)
            
            # Feuille transactions
            if transactions:
                trans_df = pd.DataFrame(transactions)
                trans_df.to_excel(writer, sheet_name='Transactions', index=False)
        
        logger.info(f"💾 Excel sauvegardé : {filename}")
        
    except Exception as e:
        logger.error(f"❌ Erreur sauvegarde Excel : {e}")

def analyze_my_team(teams_data):
    """Analyse mon équipe"""
    my_team = next((team for team in teams_data if team['is_my_team']), None)
    
    if not my_team:
        logger.warning("⚠️ Mon équipe non trouvée")
        return
    
    print(f"\n👑 MON ÉQUIPE : {my_team['team_name']}")
    print(f"📈 Rang : {my_team['ranking']}")
    print(f"🏆 Victoires : {my_team['wins']}")
    print(f"❌ Défaites : {my_team['losses']}")
    print(f"⚡ Points : {my_team['points_for']:.1f}")
    
    # Analyse des joueurs sur le banc
    bench_players = [p for p in my_team['players'] if p['is_bench']]
    bench_points = sum(p['points'] for p in bench_players)
    
    print(f"\n🪑 JOUEURS SUR LE BANC : {len(bench_players)}")
    print(f"📊 Points perdus sur le banc : {bench_points:.1f}")
    
    if bench_points > 20:
        print("⚠️ ALERTE : Beaucoup de points perdus sur le banc!")
        print("💡 Considérez des changements de lineup")
    
    # Top 3 joueurs
    top_players = sorted(my_team['players'], key=lambda x: x['points'], reverse=True)[:3]
    print(f"\n🔥 TOP 3 JOUEURS :")
    for i, player in enumerate(top_players, 1):
        print(f"   {i}. {player['name']} - {player['points']:.1f} pts")

def display_rankings(teams_data):
    """Affiche le classement"""
    print(f"\n🏆 CLASSEMENT DE LA LIGUE")
    print("=" * 60)
    
    sorted_teams = sorted(teams_data, key=lambda x: x['ranking'])
    
    for team in sorted_teams:
        marker = "👑" if team['is_my_team'] else "  "
        print(f"{marker} {team['ranking']:2d}. {team['team_name']:<25} {team['points_for']:6.1f} pts")
    
    print("=" * 60)

def main():
    """Fonction principale"""
    global logger
    logger = setup_logging()
    
    print("🆓 ESPN NBA Fantasy - Version Gratuite")
    print("=" * 50)
    print(f"📅 Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🏀 Ligue : {LEAGUE_ID} - Saison {SEASON}")
    print(f"👑 Mon équipe : {MY_TEAM_NAME}")
    print()
    
    try:
        # Collecte des données
        logger.info("📊 Collecte des données ESPN...")
        league = collect_espn_data()
        
        if not league:
            print("❌ Impossible de se connecter à ESPN")
            return
        
        # Extraction des données
        logger.info("🔍 Extraction des données...")
        teams_data = extract_team_data(league)
        transactions = extract_transactions(league)
        
        # Timestamp pour les fichiers
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Sauvegarde en différents formats
        logger.info("💾 Sauvegarde des données...")
        
        # JSON complet
        complete_data = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'league_info': {
                'league_id': LEAGUE_ID,
                'season': SEASON,
                'name': league.settings.name,
                'scoring_type': league.settings.scoring_type
            },
            'teams': teams_data,
            'transactions': transactions
        }
        
        save_to_json(complete_data, f"espn_complete_{timestamp}.json")
        
        # CSV équipes
        save_to_csv(teams_data, f"espn_teams_{timestamp}.csv")
        
        # CSV joueurs
        save_players_to_csv(teams_data, f"espn_players_{timestamp}.csv")
        
        # Excel complet
        save_to_excel(teams_data, transactions, f"espn_fantasy_{timestamp}.xlsx")
        
        # Analyses
        analyze_my_team(teams_data)
        display_rankings(teams_data)
        
        print(f"\n✅ COLLECTE TERMINÉE AVEC SUCCÈS!")
        print(f"📁 Fichiers créés :")
        print(f"   📊 espn_complete_{timestamp}.json")
        print(f"   📋 espn_teams_{timestamp}.csv")
        print(f"   👥 espn_players_{timestamp}.csv")
        print(f"   📈 espn_fantasy_{timestamp}.xlsx")
        
    except Exception as e:
        logger.error(f"❌ Erreur dans le script principal : {e}")
        print(f"❌ ERREUR : {e}")

if __name__ == "__main__":
    main()
