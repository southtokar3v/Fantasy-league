#!/bin/bash

# Définir le chemin de base
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$BASE_DIR/.venv"
LOG_DIR="$BASE_DIR/logs"

# Vérifier si le dossier logs existe
if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
fi

# Activer l'environnement virtuel
source "$VENV_DIR/bin/activate"

# Définir PYTHONPATH
export PYTHONPATH="$BASE_DIR/src"

# Lancer l'automatisation
echo "🚀 Démarrage de la collecte automatique..."
python "$BASE_DIR/src/daily_automation.py" > "$LOG_DIR/automation_$(date +%Y%m%d_%H%M%S).log" 2>&1 &

# Récupérer le PID du processus
PID=$!
echo $PID > "$BASE_DIR/.automation.pid"

echo "✅ Collecte automatique démarrée (PID: $PID)"
echo "📝 Logs disponibles dans: $LOG_DIR/automation_$(date +%Y%m%d_%H%M%S).log"
echo "💡 Pour arrêter : ./stop_collection.sh"
