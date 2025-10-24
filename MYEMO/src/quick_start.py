#!/usr/bin/env python3
"""
Quick Start - ESPN NBA Fantasy
Script de démarrage rapide avec vérifications automatiques
"""

import os
import sys
import subprocess
from datetime import datetime

def check_python_version():
    """Vérifie la version de Python"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ requis")
        print(f"   Version actuelle: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} OK")
    return True

def check_required_files():
    """Vérifie les fichiers requis"""
    required_files = [
        "requirements.txt",
        "run_simple_collection.py",
        "test_google_sheets.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Fichiers manquants: {', '.join(missing_files)}")
        return False
    
    print("✅ Fichiers requis présents")
    return True

def install_dependencies():
    """Installe les dépendances"""
    try:
        print("📦 Installation des dépendances...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dépendances installées")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur installation: {e}")
        return False

def check_credentials():
    """Vérifie les credentials Google"""
    if not os.path.exists("credentials.json"):
        print("❌ Fichier credentials.json manquant")
        print("📋 Instructions pour obtenir les credentials:")
        print("   1. Aller sur https://console.cloud.google.com/")
        print("   2. Créer un nouveau projet")
        print("   3. Activer l'API Google Sheets")
        print("   4. Créer un compte de service")
        print("   5. Télécharger le fichier JSON")
        print("   6. Le renommer 'credentials.json'")
        print("   7. Le placer dans ce répertoire")
        return False
    
    print("✅ Fichier credentials.json trouvé")
    return True

def run_tests():
    """Lance les tests de configuration"""
    try:
        print("🧪 Lancement des tests de configuration...")
        subprocess.check_call([sys.executable, "test_google_sheets.py"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur dans les tests: {e}")
        return False

def run_simple_collection():
    """Lance la collecte simple"""
    try:
        print("🚀 Lancement de la collecte simple...")
        subprocess.check_call([sys.executable, "run_simple_collection.py"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur dans la collecte: {e}")
        return False

def main():
    """Fonction principale de démarrage rapide"""
    print("🚀 ESPN NBA Fantasy - Quick Start")
    print("=" * 50)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Étape 1: Vérification Python
    print("1️⃣ Vérification de Python...")
    if not check_python_version():
        return
    
    # Étape 2: Vérification des fichiers
    print("\n2️⃣ Vérification des fichiers...")
    if not check_required_files():
        return
    
    # Étape 3: Installation des dépendances
    print("\n3️⃣ Installation des dépendances...")
    if not install_dependencies():
        return
    
    # Étape 4: Vérification des credentials
    print("\n4️⃣ Vérification des credentials...")
    if not check_credentials():
        print("\n💡 Configurez d'abord les credentials Google Sheets")
        return
    
    # Étape 5: Tests de configuration
    print("\n5️⃣ Tests de configuration...")
    if not run_tests():
        print("\n💡 Corrigez les erreurs de configuration")
        return
    
    # Étape 6: Collecte simple
    print("\n6️⃣ Collecte simple...")
    if not run_simple_collection():
        print("\n💡 Vérifiez la configuration ESPN")
        return
    
    # Succès
    print("\n" + "="*50)
    print("✅ SYSTÈME CONFIGURÉ AVEC SUCCÈS!")
    print("="*50)
    print("🎯 Prochaines étapes:")
    print("   - Vérifiez les fichiers JSON créés")
    print("   - Consultez les logs pour plus de détails")
    print("   - Lancez 'python run_simple_collection.py' pour une nouvelle collecte")
    print("   - Configurez la synchronisation automatique si souhaité")

if __name__ == "__main__":
    main()
