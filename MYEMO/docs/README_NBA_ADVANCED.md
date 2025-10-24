# 🏀 ESPN Fantasy NBA Advanced Data Collector

Système complet de collecte et analyse de données pour piloter une ligue Fantasy NBA au maximum. Collecte quotidienne structurée pour analyses IA et optimisations.

## 🎯 Objectifs

- **Collecte exhaustive** : Toutes les données ESPN Fantasy NBA quotidiennement
- **Analyse IA** : Détection des tendances, optimisations, recommandations
- **Export structuré** : Données exploitables dans Google Sheets, Perplexity, ChatGPT
- **Pilotage optimal** : Comprendre la dynamique et optimiser les décisions ROTO

## 📊 Données Collectées

### 1. Infos Générales Ligue
- `league_id`, `season_id`, `scoring_type` ("roto" ou "H2H")
- Liste complète des équipes (`team_id`, nom, manager)
- Identification de votre équipe ("Neon Cobras 99")

### 2. Teams : Roster Complet et Bench Status
- **Roster quotidien** : Liste des joueurs dans chaque équipe
- **Statuts détaillés** : Titulaire/benché, INJ (blessé), position
- **Minutes et statuts** : INJ, OUT, day-to-day, etc.
- **Historique des moves** : Date de chaque changement (bench, start)

### 3. Stats des Joueurs (par jour, par équipe, par statut)
- **Stats principales** : PTS, REB, AST, STL, BLK, FG%, 3PM, TO, +/-
- **Séparation bench/active** : Points "perdus sur le banc"
- **Moyennes et totaux** : Average (moyenne/jour) ET Total (cumul)
- **Stats avancées** : EFF, USG% si disponibles

### 4. Classements & Tableaux ROTO
- **Classement global** : Rang, moyenne, cumul quotidien
- **Classement par stat** : Leaderboards 3pts, assists, reb, etc.
- **Historique des classements** : Courbes de progression

### 5. Transactions, Waivers, Trades, Free Agents
- **Historique complet** : Ajouts/Drop/Trade/Move/Bench timestampés
- **Trades** : Joueurs échangés, date, équipes impliquées
- **Free Agents** : Stats récentes (7/14/30 derniers jours)
- **Popularité** : %roster, %start, tendances "hot pickup"

### 6. Planning NBA, Opposition, Back-to-back
- **Calendrier** : À venir sur 7/14 jours pour chaque joueur
- **Adversaires** : Contre qui il joue chaque jour
- **Back-to-back** : Détection des matches consécutifs
- **Home/Away** : Impact des déplacements
- **Proba de repos** : Estimation des "rest days"

### 7. Blessures & Statuts
- **Statuts à jour** : INJ, GTD, OUT, QUESTIONABLE
- **Durée prévue** : Date et durée suspectée d'absence
- **News associées** : Sources, commentaires injury NBA/ESPN

### 8. Dynamique, Tendances, Hot/Cold Streaks
- **Mouvements de production** : Variation stats sur 3/7/14 jours
- **Variation équipe** : Qui "chauffe" ou "plonge"
- **Évolution classement** : Performance dans chaque catégorie
- **Bench catastrophes** : Points perdus à cause des mauvais choix

### 9. Notifications IA / Logs de Décision
- **Logs événements** : "Why did you win/lose a stat?"
- **Historique conseils** : "X recommandait de streamer tel joueur, résultat: +points"
- **Analyse des décisions** : Impact des choix sur les résultats

### 10. Marquage "Moi vs les Autres"
- **Identification automatique** : "Mon équipe = Neon Cobras 99"
- **Différenciation** : Stats personnelles VS adversaires
- **Analyse comparative** : Performance relative

## 🚀 Installation

### Prérequis
```bash
# Python 3.8+
python --version

# Installation des dépendances
pip install -r requirements_nba_advanced.txt
```

### Configuration
1. **Credentials Google Sheets** (optionnel)
   ```bash
   # Téléchargez credentials.json depuis Google Cloud Console
   # Placez-le dans le répertoire du projet
   ```

2. **Configuration Email** (optionnel)
   ```python
   # Éditez nba_data_scheduler.py
   EMAIL_CONFIG = {
       'smtp_server': 'smtp.gmail.com',
       'smtp_port': 587,
       'email': 'your_email@gmail.com',
       'password': 'your_app_password'
   }
   ```

## 📁 Structure des Fichiers

```
MYEMO/
├── espn_nba_advanced_analyzer.py    # Script principal
├── nba_data_scheduler.py            # Scheduler automatique
├── google_sheets_integration.py     # Export Google Sheets
├── requirements_nba_advanced.txt     # Dépendances
├── README_NBA_ADVANCED.md           # Documentation
├── credentials.json                 # Google Sheets credentials (optionnel)
└── data/                           # Données collectées
    ├── daily_snapshots/            # Snapshots quotidiens
    ├── weekly_reports/              # Rapports hebdomadaires
    └── exports/                    # Exports structurés
```

## 🔧 Utilisation

### Collecte Manuelle
```bash
# Collecte unique des données
python espn_nba_advanced_analyzer.py
```

### Collecte Automatique
```bash
# Démarrage du scheduler (collecte 2x/jour + analyse hebdo)
python nba_data_scheduler.py
```

### Export Google Sheets
```bash
# Configuration de l'export Google Sheets
python google_sheets_integration.py
```

## 📊 Exports et Formats

### Fichiers JSON Quotidiens
```json
{
  "date": "2026-01-15",
  "league_info": {...},
  "teams_summary": [...],
  "players_detailed": [...],
  "transactions": [...],
  "free_agents": [...],
  "injuries": [...],
  "ai_insights": [...]
}
```

### Google Sheets Structure
- **Données Quotidiennes** : Infos générales ligue
- **Résumé Équipes** : Stats et classements
- **Joueurs Détaillés** : Stats individuelles avec statuts
- **Transactions** : Historique complet
- **Agents Libres** : FA disponibles avec stats
- **Blessures** : Statuts injury
- **Analyse Banc** : Points perdus sur le banc
- **Insights IA** : Recommandations et alertes

### Format CSV pour Analyses
```csv
date,team,is_my_team,player_name,position,status,is_bench,points,rebounds,assists,steals,blocks,efficiency,injury_status
2026-01-15,Neon Cobras 99,TRUE,LeBron James,SF,active,FALSE,25.5,8.2,6.8,1.2,0.8,32.1,healthy
```

## 🤖 Fonctionnalités IA

### Détection des Tendances
- **Hot Streaks** : Joueurs en forme récente
- **Cold Streaks** : Joueurs en baisse
- **Bench Optimization** : Points perdus sur le banc
- **Trade Opportunities** : Opportunités d'échanges

### Recommandations Automatiques
- **Lineup Optimization** : Suggestions de changements
- **Streaming Targets** : Joueurs à ajouter temporairement
- **Trade Targets** : Joueurs à échanger
- **Injury Management** : Gestion des blessures

### Alertes Intelligentes
- **Points perdus** : Quand vous perdez des points sur le banc
- **Classement** : Alertes de chute de classement
- **Blessures** : Joueurs blessés de votre équipe
- **Transactions** : Activité importante de la ligue

## 📈 Analyses Avancées

### Bench Analysis
```python
# Points perdus sur le banc
bench_points = team.bench_stats.get('points', 0)
if bench_points > 20:
    alert("⚠️ Points perdus sur le banc: {bench_points:.1f}")
```

### Hot/Cold Detection
```python
# Détection des tendances
for player in roster:
    recent_avg = calculate_recent_average(player, days=7)
    season_avg = calculate_season_average(player)
    
    if recent_avg > season_avg * 1.2:
        mark_as_hot(player)
    elif recent_avg < season_avg * 0.8:
        mark_as_cold(player)
```

### ROTO Optimization
```python
# Analyse des catégories faibles
weak_categories = identify_weak_categories(my_team)
for category in weak_categories:
    suggest_improvements(category)
```

## 🔄 Automatisation

### Scheduler Quotidien
- **8h00** : Collecte matinale
- **20h00** : Collecte vespérale
- **Dimanche 9h00** : Analyse hebdomadaire

### Notifications Email
- **Alertes importantes** : Points perdus, blessures
- **Rapports quotidiens** : Résumé de la journée
- **Analyses hebdomadaires** : Tendances et recommandations

## 📱 Intégration avec IA

### ChatGPT/Perplexity
```python
# Export des données pour analyse IA
data_for_ai = {
    "my_team": my_team_data,
    "bench_analysis": bench_analysis,
    "trends": hot_cold_trends,
    "recommendations": ai_recommendations
}
```

### Google Sheets Dashboard
- **Graphiques automatiques** : Évolution des stats
- **Alertes conditionnelles** : Mise en forme des problèmes
- **Filtres dynamiques** : Analyse par période/équipe

## 🛠️ Personnalisation

### Configuration de Votre Équipe
```python
# Dans espn_nba_advanced_analyzer.py
MY_TEAM_NAME = "Neon Cobras 99"  # Votre nom d'équipe
```

### Seuils d'Alerte
```python
# Personnalisation des alertes
BENCH_POINTS_THRESHOLD = 20  # Points perdus sur le banc
RANKING_ALERT_THRESHOLD = 6  # Seuil d'alerte classement
INJURY_ALERT_COUNT = 2       # Nombre de blessés pour alerte
```

### Catégories ROTO
```python
# Configuration des catégories à analyser
ROTO_CATEGORIES = [
    'points', 'rebounds', 'assists', 'steals', 'blocks',
    'fg_percentage', 'ft_percentage', 'three_pointers', 'turnovers'
]
```

## 📊 Exemples d'Utilisation

### Analyse Quotidienne
```bash
# Lancement manuel
python espn_nba_advanced_analyzer.py

# Résultat
📊 RAPPORT QUOTIDIEN - 2026-01-15
🏀 MON ÉQUIPE: Neon Cobras 99 (Rang: 3)
📈 Points totaux: 1250.5
🪑 Points sur le banc: 45.2
⚡ Points actifs: 1205.3
⚠️  ATTENTION: 45.2 points perdus sur le banc!
```

### Export Google Sheets
```bash
# Configuration automatique
python google_sheets_integration.py

# Résultat
✅ Intégration Google Sheets configurée avec succès!
📊 Feuilles de calcul créées:
   - Données Quotidiennes
   - Résumé Équipes
   - Joueurs Détaillés
   - Analyse Banc
```

## 🔍 Dépannage

### Erreurs Courantes
1. **Connexion ESPN** : Vérifiez l'ID de ligue et la saison
2. **Credentials Google** : Vérifiez le fichier credentials.json
3. **Dépendances** : Installez tous les packages requis

### Logs et Debug
```bash
# Vérification des logs
tail -f espn_nba_analyzer.log
tail -f nba_scheduler.log
```

## 🚀 Roadmap

### Fonctionnalités Futures
- [ ] Intégration API NBA officielle
- [ ] Machine Learning pour prédictions
- [ ] Interface web dashboard
- [ ] Notifications push mobiles
- [ ] Analyse de sentiment des news
- [ ] Prédiction des blessures

### Améliorations
- [ ] Cache intelligent des données
- [ ] Optimisation des performances
- [ ] Support multi-ligues
- [ ] Export vers d'autres plateformes

## 📞 Support

Pour toute question ou problème :
1. Vérifiez les logs d'erreur
2. Consultez la documentation
3. Testez avec des données de test
4. Contactez le support si nécessaire

---

**🎯 Objectif** : Transformer votre ligue Fantasy NBA en machine de guerre optimisée avec des données complètes et des analyses IA avancées !

**📊 Résultat** : Compréhension totale de la dynamique de votre ligue, optimisation des décisions, et pilotage au maximum de vos performances ROTO.
