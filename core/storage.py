#!/usr/bin/env python3
"""
Storage Manager для Dynamic Messe Stand V4
Централізована система збереження та завантаження даних
"""

import os
import json
import yaml
from datetime import datetime
from core.logger import logger

class StorageManager:
    """Менеджер для роботи з файловою системою"""
    
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.data_dir = os.path.join(self.base_dir, "data")
        self.exports_dir = os.path.join(self.base_dir, "exports")
        self.ensure_directories()
    
    def ensure_directories(self):
        """Створює необхідні директорії"""
        for directory in [self.data_dir, self.exports_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
                logger.debug(f"Created directory: {directory}")
    
    def save_json(self, data, filename, subdirectory=None):
        """Зберігає дані у JSON файл"""
        try:
            if subdirectory:
                directory = os.path.join(self.data_dir, subdirectory)
                os.makedirs(directory, exist_ok=True)
            else:
                directory = self.data_dir
            
            filepath = os.path.join(directory, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"Data saved to JSON: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error saving JSON: {e}")
            return None
    
    def load_json(self, filename, subdirectory=None):
        """Завантажує дані з JSON файлу"""
        try:
            if subdirectory:
                directory = os.path.join(self.data_dir, subdirectory)
            else:
                directory = self.data_dir
            
            filepath = os.path.join(directory, filename)
            
            if not os.path.exists(filepath):
                return None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.debug(f"Data loaded from JSON: {filepath}")
            return data
            
        except Exception as e:
            logger.error(f"Error loading JSON: {e}")
            return None
    
    def save_yaml(self, data, filename, subdirectory=None):
        """Зберігає дані у YAML файл"""
        try:
            if subdirectory:
                directory = os.path.join(self.data_dir, subdirectory)
                os.makedirs(directory, exist_ok=True)
            else:
                directory = self.data_dir
            
            filepath = os.path.join(directory, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, indent=2)
            
            logger.debug(f"Data saved to YAML: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error saving YAML: {e}")
            return None
    
    def load_yaml(self, filename, subdirectory=None):
        """Завантажує дані з YAML файлу"""
        try:
            if subdirectory:
                directory = os.path.join(self.data_dir, subdirectory)
            else:
                directory = self.data_dir
            
            filepath = os.path.join(directory, filename)
            
            if not os.path.exists(filepath):
                return None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            logger.debug(f"Data loaded from YAML: {filepath}")
            return data
            
        except Exception as e:
            logger.error(f"Error loading YAML: {e}")
            return None
    
    def export_json(self, data, filename):
        """Експортує дані у JSON файл в exports директорії"""
        try:
            filepath = os.path.join(self.exports_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Data exported to JSON: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error exporting JSON: {e}")
            return None
    
    def export_yaml(self, data, filename):
        """Експортує дані у YAML файл в exports директорії"""
        try:
            filepath = os.path.join(self.exports_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, indent=2)
            
            logger.info(f"Data exported to YAML: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error exporting YAML: {e}")
            return None
    
    def file_exists(self, filename, subdirectory=None):
        """Перевіряє чи існує файл"""
        if subdirectory:
            directory = os.path.join(self.data_dir, subdirectory)
        else:
            directory = self.data_dir
        
        filepath = os.path.join(directory, filename)
        return os.path.exists(filepath)
    
    def delete_file(self, filename, subdirectory=None):
        """Видаляє файл"""
        try:
            if subdirectory:
                directory = os.path.join(self.data_dir, subdirectory)
            else:
                directory = self.data_dir
            
            filepath = os.path.join(directory, filename)
            
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.debug(f"File deleted: {filepath}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            return False
    
    def list_files(self, subdirectory=None, extension=None):
        """Повертає список файлів в директорії"""
        try:
            if subdirectory:
                directory = os.path.join(self.data_dir, subdirectory)
            else:
                directory = self.data_dir
            
            if not os.path.exists(directory):
                return []
            
            files = os.listdir(directory)
            
            if extension:
                files = [f for f in files if f.endswith(extension)]
            
            return sorted(files)
            
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return []
    
    def get_file_info(self, filename, subdirectory=None):
        """Повертає інформацію про файл"""
        try:
            if subdirectory:
                directory = os.path.join(self.data_dir, subdirectory)
            else:
                directory = self.data_dir
            
            filepath = os.path.join(directory, filename)
            
            if not os.path.exists(filepath):
                return None
            
            stat = os.stat(filepath)
            
            return {
                'filename': filename,
                'filepath': filepath,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'created': datetime.fromtimestamp(stat.st_ctime)
            }
            
        except Exception as e:
            logger.error(f"Error getting file info: {e}")
            return None
    
    def backup_data(self):
        """Створює резервну копію всіх даних"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = os.path.join(self.exports_dir, f"backup_{timestamp}")
            os.makedirs(backup_dir, exist_ok=True)
            
            # Копіювати всі файли з data директорії
            import shutil
            if os.path.exists(self.data_dir):
                shutil.copytree(self.data_dir, os.path.join(backup_dir, "data"))
            
            logger.info(f"Backup created: {backup_dir}")
            return backup_dir
            
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return None

# Глобальна інстанція storage manager
storage_manager = StorageManager()
