#!/usr/bin/env python3
"""
Analyse des Données Brutes ESPN
Script pour analyser les données brutes récupérées
"""

import json
import os
from datetime import datetime

def find_latest_raw_data():
    """Trouve le fichier de données brutes le plus récent"""
    files = [f for f in os.listdir('.') if f.startswith('espn_raw_data_') and f.endswith('.json')]
    if files:
        # Trier par date de modification
        files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return files[0]
    return None

def analyze_raw_data(filename):
    """Analyse les données brutes"""
    print(f"🔍 ANALYSE DES DONNÉES BRUTES")
    print("=" * 50)
    print(f"📁 Fichier : {filename}")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Fichier chargé avec succès")
        
        # Analyser la structure
        print(f"\n📊 STRUCTURE GÉNÉRALE :")
        print(f"   Clés principales : {list(data.keys())}")
        
        # Analyser les équipes
        if 'teams' in data:
            teams = data['teams']
            print(f"\n👥 ÉQUIPES :")
            print(f"   Nombre : {len(teams)}")
            print(f"   Type : {type(teams)}")
            
            if teams:
                print(f"   Premier élément : {teams[0]}")
                print(f"   Type premier élément : {type(teams[0])}")
                
                if isinstance(teams[0], dict):
                    print(f"   Clés premier élément : {list(teams[0].keys())}")
                elif isinstance(teams[0], str):
                    print(f"   Premier élément (string) : {teams[0]}")
                else:
                    print(f"   Premier élément (autre) : {teams[0]}")
        
        # Analyser les paramètres
        if 'settings' in data:
            settings = data['settings']
            print(f"\n⚙️ PARAMÈTRES :")
            print(f"   Type : {type(settings)}")
            if isinstance(settings, dict):
                print(f"   Clés : {list(settings.keys())}")
                print(f"   Nom : {settings.get('name', 'N/A')}")
                print(f"   Saison : {settings.get('seasonId', 'N/A')}")
                print(f"   Type scoring : {settings.get('scoringType', 'N/A')}")
        
        # Analyser les membres
        if 'members' in data:
            members = data['members']
            print(f"\n👤 MEMBRES :")
            print(f"   Nombre : {len(members)}")
            if members:
                print(f"   Premier membre : {members[0]}")
                if isinstance(members[0], dict):
                    print(f"   Clés premier membre : {list(members[0].keys())}")
        
        # Chercher des indices de votre équipe
        print(f"\n🔍 RECHERCHE DE VOTRE ÉQUIPE :")
        data_str = json.dumps(data, ensure_ascii=False).lower()
        
        if 'neon cobras' in data_str:
            print(f"   ✅ 'Neon Cobras' trouvé dans les données")
        if 'cobras' in data_str:
            print(f"   ✅ 'Cobras' trouvé dans les données")
        if 'team' in data_str:
            print(f"   ✅ 'Team' trouvé dans les données")
        if 'league' in data_str:
            print(f"   ✅ 'League' trouvé dans les données")
        
        return data
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return None

def extract_teams_from_data(data):
    """Extrait les équipes des données"""
    print(f"\n📋 EXTRACTION DES ÉQUIPES")
    print("=" * 50)
    
    if not data:
        print("❌ Pas de données à analyser")
        return []
    
    teams = []
    
    # Méthode 1 : Depuis 'teams'
    if 'teams' in data:
        teams_data = data['teams']
        print(f"📊 Équipes depuis 'teams' : {len(teams_data)}")
        
        for i, team in enumerate(teams_data):
            if isinstance(team, dict):
                team_info = {
                    'index': i,
                    'id': team.get('id', 'N/A'),
                    'name': team.get('name', 'N/A'),
                    'abbrev': team.get('abbrev', 'N/A'),
                    'owners': team.get('owners', [])
                }
            else:
                team_info = {
                    'index': i,
                    'raw_data': str(team)
                }
            
            teams.append(team_info)
            print(f"   {i+1}. {team_info}")
    
    # Méthode 2 : Depuis 'members'
    if 'members' in data:
        members_data = data['members']
        print(f"\n📊 Membres depuis 'members' : {len(members_data)}")
        
        for i, member in enumerate(members_data):
            if isinstance(member, dict):
                member_info = {
                    'index': i,
                    'id': member.get('id', 'N/A'),
                    'displayName': member.get('displayName', 'N/A'),
                    'firstName': member.get('firstName', 'N/A'),
                    'lastName': member.get('lastName', 'N/A')
                }
                print(f"   {i+1}. {member_info}")
    
    return teams

def main():
    """Fonction principale"""
    print("🔍 ANALYSE DES DONNÉES BRUTES ESPN")
    print("=" * 60)
    
    # Trouver le fichier de données brutes
    filename = find_latest_raw_data()
    
    if not filename:
        print("❌ Aucun fichier de données brutes trouvé")
        print("💡 Lancez d'abord 'python extract_espn_data.py'")
        return
    
    # Analyser les données
    data = analyze_raw_data(filename)
    
    if data:
        # Extraire les équipes
        teams = extract_teams_from_data(data)
        
        print(f"\n✅ ANALYSE TERMINÉE")
        print(f"📊 {len(teams)} équipes/membres trouvés")
        
        # Chercher votre équipe
        for team in teams:
            if isinstance(team, dict) and 'name' in team:
                if 'Neon Cobras' in team['name'] or 'Cobras' in team['name']:
                    print(f"🎉 VOTRE ÉQUIPE TROUVÉE : {team}")
                    break
        else:
            print(f"⚠️ Votre équipe 'Neon Cobras 99' non trouvée dans les données")
            print(f"💡 Vérifiez les noms d'équipes dans votre ligue ESPN")

if __name__ == "__main__":
    main()
