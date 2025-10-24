# 🚀 Guide de Configuration - Système ESPN NBA Fantasy

## 📋 Étapes pour Rendre le Système Fonctionnel

### **ÉTAPE 1 : Installation des Dépendances**

```bash
# 1. Installer Python 3.8+ si pas déjà fait
python --version

# 2. Installer les dépendances
pip install espn-api pandas numpy requests gspread google-auth google-auth-oauthlib google-auth-httplib2 schedule

# 3. Ou installer depuis le fichier requirements
pip install -r requirements.txt
```

### **ÉTAPE 2 : Configuration Google Sheets**

#### **2.1 Créer un Projet Google Cloud**
1. Aller sur [Google Cloud Console](https://console.cloud.google.com/)
2. Créer un nouveau projet ou sélectionner un existant
3. Activer l'API Google Sheets et Google Drive

#### **2.2 Créer un Compte de Service**
1. Aller dans "IAM & Admin" > "Service Accounts"
2. Cliquer "Create Service Account"
3. Nommer le compte (ex: "espn-nba-fantasy")
4. Rôle : "Editor" ou "Owner"
5. Cliquer "Done"

#### **2.3 Télécharger les Credentials**
1. Cliquer sur le compte de service créé
2. Aller dans l'onglet "Keys"
3. Cliquer "Add Key" > "Create new key"
4. Sélectionner "JSON"
5. Télécharger le fichier et le renommer `credentials.json`
6. Placer le fichier dans le répertoire du projet

### **ÉTAPE 3 : Configuration du Script Principal**

#### **3.1 Créer le fichier de configuration**
```python
# config.py
LEAGUE_ID = 1557635339
SEASON = 2026
MY_TEAM_NAME = "Neon Cobras 99"
CREDENTIALS_FILE = "credentials.json"
```

#### **3.2 Tester la connexion ESPN**
```python
# test_espn.py
from espn_api.basketball import League

try:
    league = League(league_id=1557635339, year=2026)
    print(f"✅ Connexion ESPN réussie: {league.settings.name}")
    print(f"👥 {len(league.teams)} équipes")
except Exception as e:
    print(f"❌ Erreur ESPN: {e}")
```

### **ÉTAPE 4 : Test de Configuration**

#### **4.1 Test des Credentials Google**
```python
# test_google.py
from google.oauth2.service_account import Credentials
import gspread

try:
    creds = Credentials.from_service_account_file("credentials.json")
    gc = gspread.authorize(creds)
    print("✅ Credentials Google OK")
except Exception as e:
    print(f"❌ Erreur Google: {e}")
```

#### **4.2 Test Complet**
```python
# test_complete.py
from espn_api.basketball import League
from google.oauth2.service_account import Credentials
import gspread

# Test ESPN
try:
    league = League(league_id=1557635339, year=2026)
    print("✅ ESPN API OK")
except Exception as e:
    print(f"❌ ESPN Error: {e}")

# Test Google
try:
    creds = Credentials.from_service_account_file("credentials.json")
    gc = gspread.authorize(creds)
    print("✅ Google Sheets OK")
except Exception as e:
    print(f"❌ Google Error: {e}")
```

### **ÉTAPE 5 : Premier Lancement**

#### **5.1 Lancement Simple**
```bash
python run_simple_collection.py
```

#### **5.2 Vérification des Résultats**
- Vérifier que les fichiers JSON sont créés
- Vérifier que Google Sheets est mis à jour
- Vérifier les logs d'erreur

### **ÉTAPE 6 : Configuration Avancée (Optionnel)**

#### **6.1 Synchronisation Automatique**
```bash
python auto_sync_google_sheets.py
```

#### **6.2 Notifications Email**
- Configurer les paramètres email dans le script
- Tester l'envoi de notifications

## 🔧 Dépannage

### **Erreurs Courantes**

#### **1. Erreur ESPN API**
```
❌ Erreur: HTTP 401 Unauthorized
```
**Solution :** Vérifier l'ID de ligue et la saison

#### **2. Erreur Google Sheets**
```
❌ Erreur: 403 Forbidden
```
**Solution :** Vérifier les permissions du compte de service

#### **3. Erreur de Dépendances**
```
❌ ModuleNotFoundError: No module named 'espn_api'
```
**Solution :** Installer les dépendances avec pip

### **Vérifications**

#### **1. Vérifier Python**
```bash
python --version  # Doit être 3.8+
```

#### **2. Vérifier les Packages**
```bash
pip list | grep espn-api
pip list | grep gspread
```

#### **3. Vérifier les Fichiers**
```bash
ls -la credentials.json  # Doit exister
ls -la *.py             # Scripts Python
```

## 📞 Support

Si vous rencontrez des problèmes :
1. Vérifiez les logs d'erreur
2. Testez chaque composant séparément
3. Consultez la documentation
4. Contactez le support si nécessaire
