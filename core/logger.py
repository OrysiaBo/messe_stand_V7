#!/usr/bin/env python3
"""
Logger System для Dynamic Messe Stand V4
Централізована система логування
"""

import logging
import os
from datetime import datetime

class BertrandtLogger:
    """Кастомний логер для Bertrandt Dynamic Messe Stand"""
    
    def __init__(self, name="DynamicMesseStand", level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Видалити існуючі handlers щоб уникнути дублікатів
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        self.setup_handlers()
    
    def setup_handlers(self):
        """Налаштовує handlers для логування"""
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # File handler
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f"dynamic_messe_stand_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # Додати handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def debug(self, message):
        """Debug level logging"""
        self.logger.debug(message)
    
    def info(self, message):
        """Info level logging"""
        self.logger.info(message)
    
    def warning(self, message):
        """Warning level logging"""
        self.logger.warning(message)
    
    def error(self, message):
        """Error level logging"""
        self.logger.error(message)
    
    def critical(self, message):
        """Critical level logging"""
        self.logger.critical(message)

# Глобальний логер
logger = BertrandtLogger()
