#!/usr/bin/env python3
"""
Test de Configuration Google Sheets
Script pour tester la connexion et créer un spreadsheet de test
"""

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json

def test_google_credentials():
    """Test les credentials Google"""
    try:
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
        
        print("✅ Credentials Google chargés avec succès")
        return gc
        
    except FileNotFoundError:
        print("❌ Fichier credentials.json non trouvé")
        print("💡 Téléchargez le fichier depuis Google Cloud Console")
        return None
    except Exception as e:
        print(f"❌ Erreur credentials Google: {e}")
        return None

def create_test_spreadsheet(gc):
    """Crée un spreadsheet de test"""
    try:
        # Création du spreadsheet
        spreadsheet = gc.create(f"ESPN NBA Fantasy Test - {datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        print(f"✅ Spreadsheet créé: {spreadsheet.url}")
        
        # Configuration des permissions
        spreadsheet.share('', perm_type='anyone', role='reader')
        
        # Création d'une feuille de test
        worksheet = spreadsheet.add_worksheet("Test Data", rows=100, cols=10)
        
        # Ajout de données de test
        test_data = [
            ['Date', 'Ligue', 'Saison', 'Mon Équipe', 'Statut'],
            [datetime.now().strftime('%Y-%m-%d'), '1557635339', '2026', 'Neon Cobras 99', 'Test OK'],
            ['', '', '', '', ''],
            ['Configuration', 'Valeur', 'Statut', '', ''],
            ['ESPN API', 'Connecté', '✅', '', ''],
            ['Google Sheets', 'Connecté', '✅', '', ''],
            ['Credentials', 'Valides', '✅', '', '']
        ]
        
        worksheet.update('A1', test_data)
        
        print("✅ Données de test ajoutées")
        print(f"🔗 Lien: {spreadsheet.url}")
        
        return spreadsheet
        
    except Exception as e:
        print(f"❌ Erreur création spreadsheet: {e}")
        return None

def test_espn_connection():
    """Test la connexion ESPN"""
    try:
        from espn_api.basketball import League
        
        league = League(league_id=1557635339, year=2026)
        print(f"✅ Connexion ESPN réussie: {league.settings.name}")
        print(f"👥 {len(league.teams)} équipes")
        
        return league
        
    except Exception as e:
        print(f"❌ Erreur connexion ESPN: {e}")
        return None

def main():
    """Fonction principale de test"""
    print("🧪 Test de Configuration - ESPN NBA Fantasy")
    print("=" * 60)
    
    # Test 1: Credentials Google
    print("\n1️⃣ Test des credentials Google...")
    gc = test_google_credentials()
    
    if not gc:
        print("\n❌ ÉCHEC: Credentials Google non configurés")
        print("📋 Instructions:")
        print("   1. Aller sur Google Cloud Console")
        print("   2. Créer un projet")
        print("   3. Activer l'API Google Sheets")
        print("   4. Créer un compte de service")
        print("   5. Télécharger credentials.json")
        return
    
    # Test 2: Création spreadsheet
    print("\n2️⃣ Test de création spreadsheet...")
    spreadsheet = create_test_spreadsheet(gc)
    
    if not spreadsheet:
        print("\n❌ ÉCHEC: Impossible de créer le spreadsheet")
        return
    
    # Test 3: Connexion ESPN
    print("\n3️⃣ Test de connexion ESPN...")
    league = test_espn_connection()
    
    if not league:
        print("\n❌ ÉCHEC: Impossible de se connecter à ESPN")
        print("📋 Vérifiez:")
        print("   - ID de ligue: 1557635339")
        print("   - Saison: 2026")
        print("   - Connexion internet")
        return
    
    # Résumé des tests
    print("\n" + "="*60)
    print("✅ TOUS LES TESTS RÉUSSIS!")
    print("="*60)
    print(f"📊 Spreadsheet créé: {spreadsheet.url}")
    print("🏀 ESPN API: Connecté")
    print("📋 Google Sheets: Connecté")
    print("🔧 Configuration: Prête")
    
    print("\n🚀 Vous pouvez maintenant lancer:")
    print("   python run_simple_collection.py")

if __name__ == "__main__":
    main()
