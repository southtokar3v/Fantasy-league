"""
Script principal pour lancer la collecte en temps réel
"""
from src.collectors.realtime_collector import RealTimeCollector

def main():
    # Créer une instance du collecteur temps réel
    collector = RealTimeCollector()
    
    # Démarrer la collecte avec un intervalle de 30 minutes
    # Vous pouvez modifier l'intervalle selon vos besoins
    collector.start_collection(interval_minutes=30)

if __name__ == "__main__":
    main()
