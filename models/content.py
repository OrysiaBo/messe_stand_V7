#!/usr/bin/env python3
"""
Content Manager для Dynamic Messe Stand V4
Централізована система управління слайдами
"""

import os
import json
import yaml
from datetime import datetime
from core.logger import logger
from core.storage import storage_manager

class SlideData:
    """Клас для представлення даних слайду"""
    
    def __init__(self, slide_id, title="", content="", config_data=None):
        self.slide_id = slide_id
        self.title = title
        self.content = content
        self.config_data = config_data or {}
        self.last_modified = datetime.now()
    
    def to_dict(self):
        """Конвертація в словник для збереження"""
        return {
            'slide_id': self.slide_id,
            'title': self.title,
            'content': self.content,
            'config_data': self.config_data,
            'last_modified': self.last_modified.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        """Створення об'єкта з словника"""
        slide = cls(
            data.get('slide_id', 1),
            data.get('title', ''),
            data.get('content', ''),
            data.get('config_data', {})
        )
        
        # Відновлення часу модифікації
        try:
            slide.last_modified = datetime.fromisoformat(data.get('last_modified', datetime.now().isoformat()))
        except:
            slide.last_modified = datetime.now()
            
        return slide

class ContentManager:
    """Централізований менеджер контенту"""
    
    def __init__(self):
        self.slides = {}
        self.content_observers = []  # Для сповіщення про зміни
        self.load_default_content()
    
    def load_default_content(self):
        """Завантаження контенту за замовчуванням"""
        default_slides = {
            1: SlideData(1, "BumbleB - Das automatisierte Shuttle", 
                        "Schonmal ein automatisiert Shuttle gesehen, das aussieht wie eine Hummel?\n\nShuttle fährt los von Bushaltestelle an Bahnhof..."),
            2: SlideData(2, "BumbleB - Wie die Hummel fährt",
                        "Wie die Hummel ihre Flügel nutzt, so nutzt unser BumbleB innovative Technologie für autonomes Fahren."),
            3: SlideData(3, "Einsatzgebiete und Vorteile",
                        "Vielseitige Einsatzmöglichkeiten in urbanen Gebieten für nachhaltigen Transport."),
            4: SlideData(4, "Sicherheitssysteme",
                        "Moderne Sicherheitssysteme gewährleisten maximale Sicherheit für alle Passagiere."),
            5: SlideData(5, "Nachhaltigkeit & Umwelt",
                        "Nachhaltiger Transport für eine grüne Zukunft - umweltfreundlich und effizient.")
        }
        
        for slide_id, slide_data in default_slides.items():
            if slide_id not in self.slides:
                self.slides[slide_id] = slide_data
        
        logger.debug(f"Loaded {len(default_slides)} default slides")
    
    def get_slide(self, slide_id):
        """Отримання слайду за ID"""
        return self.slides.get(slide_id)
    
    def get_all_slides(self):
        """Отримання всіх слайдів"""
        return self.slides.copy()
    
    def get_slide_count(self):
        """Отримання кількості слайдів"""
        return len(self.slides)
    
    def update_slide_content(self, slide_id, title, content, config_data=None):
        """Оновлення контенту слайду"""
        if slide_id not in self.slides:
            self.slides[slide_id] = SlideData(slide_id)
        
        slide = self.slides[slide_id]
        slide.title = title
        slide.content = content
        if config_data:
            slide.config_data.update(config_data)
        slide.last_modified = datetime.now()
        
        # Сповістити спостерігачів про зміни
        self.notify_observers(slide_id, slide)
        
        logger.debug(f"Updated slide {slide_id}: {title[:30]}...")
        return True
    
    def create_slide(self, slide_id, title="", content=""):
        """Створення нового слайду"""
        if slide_id in self.slides:
            logger.warning(f"Slide {slide_id} already exists, updating instead")
        
        self.slides[slide_id] = SlideData(slide_id, title, content)
        self.notify_observers(slide_id, self.slides[slide_id])
        
        logger.info(f"Created new slide {slide_id}")
        return True
    
    def delete_slide(self, slide_id):
        """Видалення слайду"""
        if slide_id in self.slides:
            del self.slides[slide_id]
            self.notify_observers(slide_id, None, action='delete')
            logger.info(f"Deleted slide {slide_id}")
            return True
        return False
    
    def add_observer(self, callback):
        """Додавання спостерігача для отримання сповіщень про зміни"""
        self.content_observers.append(callback)
    
    def notify_observers(self, slide_id, slide_data, action='update'):
        """Сповіщення всіх спостерігачів про зміни"""
        for callback in self.content_observers:
            try:
                callback(slide_id, slide_data, action)
            except Exception as e:
                logger.error(f"Error notifying observer: {e}")
    
    def save_to_file(self, filepath=None):
        """Збереження всіх слайдів у файл"""
        if not filepath:
            filepath = os.path.join("data", "slides.json")
        
        # Створюємо директорію якщо не існує
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        data = {
            'slides': {str(k): v.to_dict() for k, v in self.slides.items()},
            'exported_at': datetime.now().isoformat(),
            'version': "4.0.0"
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Slides saved to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving slides: {e}")
            return False
    
    def load_from_file(self, filepath=None):
        """Завантаження слайдів з файлу"""
        if not filepath:
            filepath = os.path.join("data", "slides.json")
        
        if not os.path.exists(filepath):
            logger.warning(f"Slides file not found: {filepath}")
            return False
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'slides' in data:
                self.slides.clear()
                for slide_id_str, slide_data in data['slides'].items():
                    slide_id = int(slide_id_str)
                    self.slides[slide_id] = SlideData.from_dict(slide_data)
                
                logger.info(f"Loaded {len(self.slides)} slides from {filepath}")
                
                # Сповістити всіх спостерігачів
                for slide_id, slide_data in self.slides.items():
                    self.notify_observers(slide_id, slide_data, action='load')
                
                return True
        except Exception as e:
            logger.error(f"Error loading slides: {e}")
            return False
    
    def export_presentation_as_json(self, filepath=None):
        """Експорт презентації у JSON"""
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"exports/presentation_{timestamp}.json"
        
        return self.save_to_file(filepath)
    
    def export_presentation_as_yaml(self, filepath=None):
        """Експорт презентації у YAML"""
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"exports/presentation_{timestamp}.yaml"
        
        # Створюємо директорію якщо не існує
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        data = {
            'slides': {str(k): v.to_dict() for k, v in self.slides.items()},
            'exported_at': datetime.now().isoformat(),
            'version': "4.0.0"
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, indent=2)
            
            logger.info(f"Slides exported to YAML: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error exporting to YAML: {e}")
            return None
    
    def load_presentation_from_file(self):
        """Завантаження презентації з файлу через діалог"""
        try:
            from tkinter import filedialog
            
            filepath = filedialog.askopenfilename(
                title="Презентацію завантажити",
                filetypes=[
                    ("JSON файли", "*.json"),
                    ("YAML файли", "*.yaml *.yml"),
                    ("Усі файли", "*.*")
                ]
            )
            
            if filepath:
                if filepath.endswith(('.yaml', '.yml')):
                    return self.load_from_yaml(filepath)
                else:
                    return self.load_from_file(filepath)
            
            return False
        except Exception as e:
            logger.error(f"Error in load dialog: {e}")
            return False
    
    def load_from_yaml(self, filepath):
        """Завантаження з YAML файлу"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if 'slides' in data:
                self.slides.clear()
                for slide_id_str, slide_data in data['slides'].items():
                    slide_id = int(slide_id_str)
                    self.slides[slide_id] = SlideData.from_dict(slide_data)
                
                logger.info(f"Loaded {len(self.slides)} slides from YAML: {filepath}")
                
                # Сповістити всіх спостерігачів
                for slide_id, slide_data in self.slides.items():
                    self.notify_observers(slide_id, slide_data, action='load')
                
                return True
        except Exception as e:
            logger.error(f"Error loading from YAML: {e}")
            return False

# Глобальна інстанція менеджера контенту
content_manager = ContentManager()
