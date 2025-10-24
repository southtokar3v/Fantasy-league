#!/bin/bash

# Définir le chemin de base
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$BASE_DIR/.automation.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    
    # Vérifier si le processus existe toujours
    if ps -p $PID > /dev/null; then
        echo "🛑 Arrêt de la collecte automatique (PID: $PID)..."
        kill $PID
        rm "$PID_FILE"
        echo "✅ Collecte automatique arrêtée"
    else
        echo "⚠️ Le processus n'est plus en cours d'exécution"
        rm "$PID_FILE"
    fi
else
    echo "❌ Aucune collecte automatique en cours"
fi
