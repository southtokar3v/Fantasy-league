import logging
import os
from datetime import datetime

class Logger:
    @staticmethod
    def setup(name: str, log_dir: str = "logs"):
        """Configure le logger"""
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        logging.basicConfig(
            filename=os.path.join(log_dir, f"{name}_{datetime.now().strftime('%Y%m%d')}.log"),
            level=logging.INFO,
            format="%(asctime)s - [%(error_code)s] - %(levelname)s - %(source)s - %(message)s"
        )
        return logging.getLogger(name)

    @staticmethod
    def log_error(logger, error: Exception, error_code: str, source: str):
        """Log une erreur avec son code et sa source"""
        extra = {
            "error_code": error_code,
            "source": source
        }
        logger.error(str(error), extra=extra)
