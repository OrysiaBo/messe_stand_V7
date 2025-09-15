#!/usr/bin/env python3
"""
Централізований стейт для синхронізації між Creator та Demo
"""

import threading
from typing import Dict, Any, List, Callable
from datetime import datetime

class PresentationState:
    """Централізований стан презентації"""
    
    def __init__(self):
        self.current_slide = 1
        self.slides_data = {}
        self.last_modified = datetime.now()
        self._observers = []
        self._lock = threading.Lock()
    
    def add_observer(self, callback: Callable):
        """Додати спостерігача для змін стану"""
        with self._lock:
            self._observers.append(callback)
    
    def remove_observer(self, callback: Callable):
        """Видалити спостерігача"""
        with self._lock:
            if callback in self._observers:
                self._observers.remove(callback)
    
    def _notify_observers(self, slide_id=None, action='update'):
        """Сповістити всіх спостерігачів про зміни"""
        for callback in self._observers:
            try:
                callback(slide_id, action)
            except Exception as e:
                print(f"Error notifying observer: {e}")
    
    def update_slide_content(self, slide_id, title, content):
        """Оновити контент слайду"""
        with self._lock:
            self.slides_data[slide_id] = {
                'title': title,
                'content': content,
                'slide_number': slide_id,
                'last_modified': datetime.now()
            }
            self.last_modified = datetime.now()
        
        # Оновити також content_manager
        from models.content import content_manager
        content_manager.update_slide_content(slide_id, title, content)
        
        # Сповістити спостерігачів
        self._notify_observers(slide_id, 'update')
    
    def get_slide_data(self, slide_id):
        """Отримати дані слайду"""
        with self._lock:
            if slide_id in self.slides_data:
                return self.slides_data[slide_id].copy()
            
            # Fallback до content_manager
            from models.content import content_manager
            slide = content_manager.get_slide(slide_id)
            if slide:
                return {
                    'title': slide.title,
                    'content': slide.content,
                    'slide_number': slide_id
                }
        return None
    
    def set_current_slide(self, slide_id):
        """Встановити поточний слайд"""
        with self._lock:
            self.current_slide = slide_id
        self._notify_observers(slide_id, 'navigate')

# Глобальний стейт
presentation_state = PresentationState()
