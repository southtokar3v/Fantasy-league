class ESPNDataCollectorError(Exception):
    """Classe personnalisée pour les erreurs de collecte"""
    def __init__(self, message: str, error_code: str, source: str):
        self.error_code = error_code
        self.source = source
        super().__init__(f"[{error_code}] {source}: {message}")

ERROR_CODES = {
    "CONN": "Erreur de connexion ESPN",
    "DATA": "Erreur de données",
    "AUTH": "Erreur d'authentification",
    "PARSE": "Erreur de parsing",
    "API": "Erreur API ESPN"
}
