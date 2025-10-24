#!/usr/bin/env python3
"""
Test de Configuration Complète
ESPN API + Google Sheets
"""

import os
import json
from datetime import datetime

def test_espn_api():
    """Test de l'API ESPN"""
    print("🏀 Test de l'API ESPN...")
    try:
        from espn_api.basketball import League
        
        # Configuration
        LEAGUE_ID = 1557635339
        SEASON = 2026
        
        # Test de connexion
        league = League(league_id=LEAGUE_ID, year=SEASON)
        
        print(f"✅ ESPN API : Connecté")
        print(f"   📊 Ligue : {league.settings.name}")
        print(f"   👥 Équipes : {len(league.teams)}")
        print(f"   🏆 Type : {league.settings.scoring_type}")
        
        # Test des données
        my_team = None
        for team in league.teams:
            if team.team_name == "Neon Cobras 99":
                my_team = team
                break
        
        if my_team:
            print(f"   👑 Mon équipe trouvée : {my_team.team_name}")
            print(f"   📈 Rang : {my_team.standing}")
        else:
            print("   ⚠️ Mon équipe 'Neon Cobras 99' non trouvée")
            print("   📋 Équipes disponibles :")
            for team in league.teams[:3]:
                print(f"      - {team.team_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ ESPN API : Erreur")
        print(f"   🔍 Détail : {e}")
        return False

def test_google_credentials():
    """Test des credentials Google"""
    print("\n📊 Test des credentials Google...")
    
    # Vérifier le fichier
    if not os.path.exists("credentials.json"):
        print("❌ Fichier credentials.json non trouvé")
        print("   📋 Instructions :")
        print("      1. Aller sur https://console.cloud.google.com/")
        print("      2. Créer un projet")
        print("      3. Activer Google Sheets API")
        print("      4. Créer un compte de service")
        print("      5. Télécharger le fichier JSON")
        print("      6. Le renommer 'credentials.json'")
        return False
    
    print("✅ Fichier credentials.json trouvé")
    
    # Vérifier le contenu
    try:
        with open("credentials.json", "r") as f:
            creds = json.load(f)
        
        required_fields = ["type", "project_id", "private_key", "client_email"]
        missing_fields = [field for field in required_fields if field not in creds]
        
        if missing_fields:
            print(f"❌ Champs manquants : {missing_fields}")
            return False
        
        print(f"✅ Credentials valides")
        print(f"   📊 Projet : {creds['project_id']}")
        print(f"   📧 Email : {creds['client_email']}")
        
        return True
        
    except json.JSONDecodeError:
        print("❌ Fichier credentials.json invalide")
        return False
    except Exception as e:
        print(f"❌ Erreur lecture credentials : {e}")
        return False

def test_google_sheets():
    """Test de Google Sheets"""
    print("\n📋 Test de Google Sheets...")
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        
        # Chargement des credentials
        creds = Credentials.from_service_account_file(
            "credentials.json",
            scopes=[
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
        )
        
        # Autorisation
        gc = gspread.authorize(creds)
        
        print("✅ Google Sheets : Connecté")
        
        # Test de création d'un spreadsheet
        test_spreadsheet = gc.create(f"Test ESPN NBA - {datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        print(f"✅ Spreadsheet de test créé")
        print(f"   🔗 URL : {test_spreadsheet.url}")
        
        # Ajout de données de test
        worksheet = test_spreadsheet.add_worksheet("Test Data", rows=10, cols=5)
        test_data = [
            ["Date", "Ligue", "Saison", "Statut"],
            [datetime.now().strftime('%Y-%m-%d'), "1557635339", "2026", "Test OK"]
        ]
        worksheet.update('A1', test_data)
        
        print("✅ Données de test ajoutées")
        
        # Nettoyage (optionnel)
        # gc.del_spreadsheet(test_spreadsheet.id)
        # print("🧹 Spreadsheet de test supprimé")
        
        return True
        
    except Exception as e:
        print(f"❌ Google Sheets : Erreur")
        print(f"   🔍 Détail : {e}")
        return False

def test_dependencies():
    """Test des dépendances Python"""
    print("📦 Test des dépendances...")
    
    required_packages = [
        "espn_api",
        "gspread", 
        "pandas",
        "numpy",
        "requests"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Packages manquants : {', '.join(missing_packages)}")
        print("💡 Installez avec : pip install " + " ".join(missing_packages))
        return False
    
    return True

def main():
    """Fonction principale de test"""
    print("🧪 TEST DE CONFIGURATION COMPLÈTE")
    print("=" * 50)
    print(f"📅 Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Tests
    tests = [
        ("Dépendances Python", test_dependencies),
        ("API ESPN", test_espn_api),
        ("Credentials Google", test_google_credentials),
        ("Google Sheets", test_google_sheets)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        result = test_func()
        results.append((test_name, result))
    
    # Résumé
    print("\n" + "="*50)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*50)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"{test_name:20} : {status}")
        if not result:
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("✅ Votre configuration est prête")
        print("🚀 Vous pouvez maintenant lancer :")
        print("   python run_simple_collection.py")
    else:
        print("⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        print("🔧 Corrigez les erreurs avant de continuer")
    
    print("="*50)

if __name__ == "__main__":
    main()
