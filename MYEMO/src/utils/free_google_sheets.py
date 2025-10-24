#!/usr/bin/env python3
"""
Version Google Sheets Gratuite
Utilise un compte Google personnel (gratuit)
Limite : 100 requêtes/jour, 1 million de cellules
"""

import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
import os
from datetime import datetime
from espn_api.basketball import League

# Configuration
LEAGUE_ID = 1557635339
SEASON = 2026
MY_TEAM_NAME = "Neon Cobras 99"

# Scopes pour Google Sheets
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def authenticate_google():
    """Authentification Google avec compte personnel"""
    creds = None
    
    # Vérifier si les tokens existent
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Si pas de credentials valides, demander l'authentification
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Créer le fichier client_secret.json d'abord
            if not os.path.exists('client_secret.json'):
                print("❌ Fichier client_secret.json manquant")
                print("📋 Instructions pour l'obtenir :")
                print("   1. Aller sur https://console.cloud.google.com/")
                print("   2. Créer un projet (gratuit)")
                print("   3. Activer Google Sheets API")
                print("   4. Créer des credentials OAuth 2.0")
                print("   5. Télécharger le fichier JSON")
                print("   6. Le renommer 'client_secret.json'")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Sauvegarder les credentials pour la prochaine fois
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

def create_free_spreadsheet(gc):
    """Crée un spreadsheet gratuit"""
    try:
        # Créer un nouveau spreadsheet
        spreadsheet = gc.create(f"ESPN NBA Fantasy - {datetime.now().strftime('%Y%m%d')}")
        
        # Partager avec votre compte email
        spreadsheet.share('', perm_type='anyone', role='reader')
        
        print(f"✅ Spreadsheet créé : {spreadsheet.url}")
        return spreadsheet
        
    except Exception as e:
        print(f"❌ Erreur création spreadsheet : {e}")
        return None

def export_to_free_sheets(league, spreadsheet):
    """Export vers Google Sheets gratuit"""
    try:
        # Feuille 1 : Résumé des équipes
        worksheet1 = spreadsheet.add_worksheet("Résumé Équipes", rows=100, cols=10)
        
        # En-têtes
        headers = [
            'Rang', 'Équipe', 'Manager', 'Victoires', 'Défaites', 
            'Points Pour', 'Points Contre', 'Mon Équipe'
        ]
        worksheet1.update('A1:H1', [headers])
        
        # Données des équipes
        teams_data = []
        for team in league.teams:
            teams_data.append([
                team.standing,
                team.team_name,
                team.owner,
                team.wins,
                team.losses,
                team.points_for,
                team.points_against,
                'OUI' if team.team_name == MY_TEAM_NAME else 'NON'
            ])
        
        worksheet1.update('A2', teams_data)
        
        # Feuille 2 : Mon équipe détaillée
        my_team = next((team for team in league.teams if team.team_name == MY_TEAM_NAME), None)
        if my_team:
            worksheet2 = spreadsheet.add_worksheet("Mon Équipe", rows=100, cols=15)
            
            # En-têtes joueurs
            player_headers = [
                'Joueur', 'Position', 'Statut', 'Points', 'Rebonds', 
                'Assists', 'Steals', 'Blocks', 'FG%', 'FT%', '3PM', 'TO'
            ]
            worksheet2.update('A1:L1', [player_headers])
            
            # Données des joueurs
            players_data = []
            for player in my_team.roster:
                players_data.append([
                    player.name,
                    player.position,
                    'Actif' if player.lineupSlot not in ['BE', 'IR'] else 'Banc',
                    player.total_points,
                    player.rebounds,
                    player.assists,
                    player.steals,
                    player.blocks,
                    player.field_goal_percentage,
                    player.free_throw_percentage,
                    player.three_pointers_made,
                    player.turnovers
                ])
            
            worksheet2.update('A2', players_data)
        
        print("✅ Données exportées vers Google Sheets")
        
    except Exception as e:
        print(f"❌ Erreur export : {e}")

def main():
    """Fonction principale version gratuite"""
    print("🆓 ESPN NBA Fantasy - Google Sheets Gratuit")
    print("=" * 50)
    print("📊 Limite : 100 requêtes/jour, 1M cellules")
    print()
    
    try:
        # Authentification Google
        print("🔐 Authentification Google...")
        creds = authenticate_google()
        
        if not creds:
            return
        
        # Connexion Google Sheets
        gc = gspread.authorize(creds)
        print("✅ Connexion Google Sheets établie")
        
        # Connexion ESPN
        print("🏀 Connexion ESPN...")
        league = League(league_id=LEAGUE_ID, year=SEASON)
        print(f"✅ Connecté : {league.settings.name}")
        
        # Création du spreadsheet
        print("📊 Création du spreadsheet...")
        spreadsheet = create_free_spreadsheet(gc)
        
        if not spreadsheet:
            return
        
        # Export des données
        print("📤 Export des données...")
        export_to_free_sheets(league, spreadsheet)
        
        print(f"\n✅ TERMINÉ AVEC SUCCÈS!")
        print(f"🔗 Lien : {spreadsheet.url}")
        print("💡 Limite : 100 requêtes/jour")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    main()
