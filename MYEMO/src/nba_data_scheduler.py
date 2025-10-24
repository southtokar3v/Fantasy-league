#!/usr/bin/env python3
"""
Scheduler pour la collecte automatique quotidienne des données ESPN NBA
Système de collecte programmée avec notifications et alertes
"""

import schedule
import time
import logging
from datetime import datetime, timedelta
import json
import os
from espn_nba_advanced_analyzer import ESPNNBAAdvancedAnalyzer
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
LEAGUE_ID = 1557635339
SEASON = 2026
MY_TEAM_NAME = "Neon Cobras 99"

# Configuration des notifications
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': 'your_email@gmail.com',
    'password': 'your_app_password'
}

class NBADataScheduler:
    """Scheduler pour la collecte automatique des données NBA"""
    
    def __init__(self):
        self.analyzer = ESPNNBAAdvancedAnalyzer(LEAGUE_ID, SEASON, MY_TEAM_NAME)
        self.setup_logging()
        
    def setup_logging(self):
        """Configure le système de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('nba_scheduler.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def daily_data_collection(self):
        """Collecte quotidienne des données"""
        try:
            self.logger.info("🚀 Début de la collecte quotidienne programmée")
            
            # Collecte des données
            snapshot = self.analyzer.collect_daily_data()
            
            # Sauvegarde
            self.analyzer.save_daily_snapshot(snapshot)
            
            # Génération du rapport
            self.analyzer.generate_daily_report(snapshot)
            
            # Analyse des alertes
            alerts = self.analyze_alerts(snapshot)
            
            # Envoi des notifications si nécessaire
            if alerts:
                self.send_notifications(alerts)
            
            self.logger.info("✅ Collecte quotidienne terminée avec succès")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur dans la collecte quotidienne: {e}")
            self.send_error_notification(str(e))
    
    def analyze_alerts(self, snapshot) -> list:
        """Analyse les données pour générer des alertes"""
        alerts = []
        
        # Trouve mon équipe
        my_team = None
        for team in snapshot.teams:
            if team.is_my_team:
                my_team = team
                break
        
        if not my_team:
            return alerts
        
        # Alerte: Points perdus sur le banc
        bench_points = my_team.bench_stats.get('points', 0)
        if bench_points > 20:
            alerts.append({
                'type': 'bench_optimization',
                'priority': 'high',
                'message': f"⚠️ {bench_points:.1f} points perdus sur le banc!",
                'action': "Vérifiez votre lineup et considérez des changements"
            })
        
        # Alerte: Classement en chute
        if my_team.ranking > 6:  # Seuil arbitraire
            alerts.append({
                'type': 'ranking_alert',
                'priority': 'medium',
                'message': f"📉 Classement actuel: {my_team.ranking}",
                'action': "Analysez vos faiblesses et considérez des trades"
            })
        
        # Alerte: Joueurs blessés
        injured_players = [p for p in my_team.roster if p.injury_status in ['OUT', 'INJ']]
        if len(injured_players) > 2:
            alerts.append({
                'type': 'injury_alert',
                'priority': 'high',
                'message': f"🏥 {len(injured_players)} joueurs blessés",
                'action': "Considérez des pickups ou des trades"
            })
        
        # Alerte: Transactions importantes
        recent_transactions = [t for t in snapshot.transactions 
                             if datetime.now() - datetime.strptime(t['date'], '%Y-%m-%d') < timedelta(days=1)]
        if len(recent_transactions) > 5:
            alerts.append({
                'type': 'activity_alert',
                'priority': 'low',
                'message': f"🔄 {len(recent_transactions)} transactions récentes",
                'action': "Restez informé de l'activité de la ligue"
            })
        
        return alerts
    
    def send_notifications(self, alerts):
        """Envoie les notifications par email"""
        if not alerts:
            return
        
        try:
            # Préparation de l'email
            msg = MIMEMultipart()
            msg['From'] = EMAIL_CONFIG['email']
            msg['To'] = EMAIL_CONFIG['email']  # Auto-notification
            msg['Subject'] = f"🏀 ESPN NBA Fantasy - Alertes du {datetime.now().strftime('%Y-%m-%d')}"
            
            # Corps du message
            body = "🚀 RAPPORT QUOTIDIEN ESPN NBA FANTASY\n"
            body += "=" * 50 + "\n\n"
            
            for alert in alerts:
                priority_emoji = "🔴" if alert['priority'] == 'high' else "🟡" if alert['priority'] == 'medium' else "🟢"
                body += f"{priority_emoji} {alert['message']}\n"
                body += f"   💡 Action suggérée: {alert['action']}\n\n"
            
            body += "\n📊 Consultez les fichiers de données pour plus de détails."
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Envoi
            server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
            server.starttls()
            server.login(EMAIL_CONFIG['email'], EMAIL_CONFIG['password'])
            server.send_message(msg)
            server.quit()
            
            self.logger.info("📧 Notifications envoyées avec succès")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur envoi notifications: {e}")
    
    def send_error_notification(self, error_message):
        """Envoie une notification d'erreur"""
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_CONFIG['email']
            msg['To'] = EMAIL_CONFIG['email']
            msg['Subject'] = "❌ Erreur ESPN NBA Data Collector"
            
            body = f"❌ ERREUR DANS LA COLLECTE DE DONNÉES\n\n"
            body += f"Date: {datetime.now()}\n"
            body += f"Erreur: {error_message}\n\n"
            body += "Vérifiez les logs pour plus de détails."
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
            server.starttls()
            server.login(EMAIL_CONFIG['email'], EMAIL_CONFIG['password'])
            server.send_message(msg)
            server.quit()
            
        except Exception as e:
            self.logger.error(f"❌ Impossible d'envoyer notification d'erreur: {e}")
    
    def weekly_analysis(self):
        """Analyse hebdomadaire approfondie"""
        self.logger.info("📊 Début de l'analyse hebdomadaire")
        
        try:
            # Collecte des données
            snapshot = self.analyzer.collect_daily_data()
            
            # Analyse des tendances sur 7 jours
            weekly_trends = self.analyze_weekly_trends()
            
            # Génération du rapport hebdomadaire
            self.generate_weekly_report(snapshot, weekly_trends)
            
            self.logger.info("✅ Analyse hebdomadaire terminée")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur analyse hebdomadaire: {e}")
    
    def analyze_weekly_trends(self) -> dict:
        """Analyse les tendances sur une semaine"""
        # Cette fonction analyserait les données historiques
        # pour identifier les tendances et patterns
        return {
            'hot_players': [],
            'cold_players': [],
            'team_trends': [],
            'category_trends': []
        }
    
    def generate_weekly_report(self, snapshot, trends):
        """Génère un rapport hebdomadaire détaillé"""
        filename = f"espn_nba_weekly_report_{datetime.now().strftime('%Y-%m-%d')}.json"
        
        report = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'type': 'weekly_analysis',
            'snapshot': snapshot.__dict__,
            'trends': trends,
            'recommendations': self.generate_weekly_recommendations(snapshot, trends)
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        self.logger.info(f"📊 Rapport hebdomadaire sauvegardé: {filename}")
    
    def generate_weekly_recommendations(self, snapshot, trends) -> list:
        """Génère des recommandations hebdomadaires"""
        recommendations = []
        
        # Recommandations basées sur les tendances
        # Cette fonction serait étendue avec de la logique IA avancée
        
        return recommendations
    
    def start_scheduler(self):
        """Démarre le scheduler"""
        self.logger.info("🚀 Démarrage du scheduler ESPN NBA")
        
        # Collecte quotidienne à 8h00
        schedule.every().day.at("08:00").do(self.daily_data_collection)
        
        # Collecte quotidienne à 20h00
        schedule.every().day.at("20:00").do(self.daily_data_collection)
        
        # Analyse hebdomadaire le dimanche à 9h00
        schedule.every().sunday.at("09:00").do(self.weekly_analysis)
        
        self.logger.info("⏰ Scheduler configuré:")
        self.logger.info("   - Collecte quotidienne: 8h00 et 20h00")
        self.logger.info("   - Analyse hebdomadaire: Dimanche 9h00")
        
        # Boucle principale
        while True:
            schedule.run_pending()
            time.sleep(60)  # Vérification toutes les minutes

def main():
    """Fonction principale du scheduler"""
    print("🚀 ESPN NBA Data Scheduler")
    print("=" * 50)
    
    scheduler = NBADataScheduler()
    
    # Test initial
    print("🧪 Test de collecte initial...")
    try:
        scheduler.daily_data_collection()
        print("✅ Test réussi!")
    except Exception as e:
        print(f"❌ Erreur dans le test: {e}")
        return
    
    # Démarrage du scheduler
    print("\n⏰ Démarrage du scheduler...")
    print("Appuyez sur Ctrl+C pour arrêter")
    
    try:
        scheduler.start_scheduler()
    except KeyboardInterrupt:
        print("\n🛑 Scheduler arrêté par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur dans le scheduler: {e}")

if __name__ == "__main__":
    main()
