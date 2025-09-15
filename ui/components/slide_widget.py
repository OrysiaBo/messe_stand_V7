#!/usr/bin/env python3
"""
Slide Widget для Dynamic Messe Stand V4
Уніфікований віджет слайду для Demo і Creator режимів - TKINTER VERSION
"""

import tkinter as tk
from tkinter import ttk
from core.theme import theme_manager
from core.logger import logger

class SlideWidget(tk.Frame):
    """
    Уніфікований віджет слайду для Demo і Creator режимів
    """
    
    def __init__(self, parent, slide_id, mode='demo', main_window=None):
        super().__init__(parent)
        self.slide_id = slide_id
        self.mode = mode  # 'demo' або 'creator'
        self.main_window = main_window
        self.content_elements = {}
        self.content_changed_callbacks = []
        
        self.setup_ui()
        self.load_content()
        
    def setup_ui(self):
        """Налаштування інтерфейсу"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts if self.main_window else {
            'title': ('Segoe UI', 24, 'bold'),
            'body': ('Segoe UI', 14, 'normal'),
            'caption': ('Segoe UI', 12, 'normal')
        }
        
        self.configure(bg=colors['background_secondary'])
        
        # Головний layout
        self.main_frame = tk.Frame(self, bg=colors['background_secondary'])
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Контейнер для контенту (PowerPoint-стиль)
        self.content_container = tk.Frame(
            self.main_frame,
            bg='white',
            relief='solid',
            bd=2,
            highlightbackground='#CCCCCC',
            highlightthickness=1
        )
        self.content_container.pack(fill='both', expand=True)
        
        # Заголовок слайду
        self.setup_title(colors, fonts)
        
        # Контент слайду
        self.setup_content(colors, fonts)
        
    def setup_title(self, colors, fonts):
        """Налаштування заголовка"""
        title_frame = tk.Frame(
            self.content_container,
            bg='#F8F9FA',
            height=80
        )
        title_frame.pack(fill='x', padx=2, pady=(2, 0))
        title_frame.pack_propagate(False)
        
        if self.mode == 'creator':
            self.title_edit = tk.Text(
                title_frame,
                height=2,
                font=fonts['title'],
                bg='#F8F9FA',
                fg='#2C3E50',
                relief='flat',
                bd=0,
                wrap='word'
            )
            self.title_edit.pack(expand=True, fill='both', padx=10, pady=10)
            self.title_edit.bind('<KeyRelease>', self.on_content_changed)
            self.content_elements['title'] = self.title_edit
        else:
            self.title_label = tk.Label(
                title_frame,
                font=fonts['title'],
                fg='#2C3E50',
                bg='#F8F9FA',
                wraplength=800,
                justify='center'
            )
            self.title_label.pack(expand=True, pady=10)
            self.content_elements['title'] = self.title_label
            
    def setup_content(self, colors, fonts):
        """Налаштування контенту"""
        content_frame = tk.Frame(
            self.content_container,
            bg='white'
        )
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        if self.mode == 'creator':
            self.content_edit = tk.Text(
                content_frame,
                font=fonts['body'],
                bg='white',
                fg='#1F1F1F',
                relief='flat',
                bd=1,
                wrap='word'
            )
            self.content_edit.pack(fill='both', expand=True)
            self.content_edit.bind('<KeyRelease>', self.on_content_changed)
            self.content_elements['content'] = self.content_edit
        else:
            # Scrollable text area для demo
            text_frame = tk.Frame(content_frame, bg='white')
            text_frame.pack(fill='both', expand=True)
            
            scrollbar = tk.Scrollbar(text_frame)
            scrollbar.pack(side='right', fill='y')
            
            self.content_label = tk.Text(
                text_frame,
                font=fonts['body'],
                bg='white',
                fg='#1F1F1F',
                wrap='word',
                relief='flat',
                bd=0,
                state='disabled',
                yscrollcommand=scrollbar.set
            )
            self.content_label.pack(side='left', fill='both', expand=True)
            scrollbar.config(command=self.content_label.yview)
            self.content_elements['content'] = self.content_label
        
        # Footer з брендингом
        self.setup_footer(colors, fonts)
            
    def setup_footer(self, colors, fonts):
        """Налаштування футера з брендингом"""
        footer_frame = tk.Frame(
            self.content_container,
            bg='#F8F9FA',
            height=30
        )
        footer_frame.pack(fill='x', padx=2, pady=(0, 2))
        footer_frame.pack_propagate(False)
        
        # Bertrandt-Branding
        branding_label = tk.Label(
            footer_frame,
            text="BERTRANDT",
            font=fonts['caption'],
            fg='#003366',
            bg='#F8F9FA'
        )
        branding_label.pack(side='right', padx=10, pady=5)
        
        # Folien-Nummer
        number_label = tk.Label(
            footer_frame,
            text=f"Folie {self.slide_id}",
            font=fonts['caption'],
            fg='#666666',
            bg='#F8F9FA'
        )
        number_label.pack(side='left', padx=10, pady=5)
        
    def load_content(self):
        """Завантаження збереженого контенту"""
        try:
            # Завантажуємо з content manager
            from models.content import content_manager
            slide_data = content_manager.get_slide(self.slide_id)
            
            if slide_data:
                # Завантажуємо заголовок
                title_text = slide_data.title
                if self.mode == 'creator':
                    self.title_edit.delete('1.0', 'end')
                    self.title_edit.insert('1.0', title_text)
                else:
                    self.title_label.configure(text=title_text)
                    
                # Завантажуємо контент
                content_text = slide_data.content
                if self.mode == 'creator':
                    self.content_edit.delete('1.0', 'end')
                    self.content_edit.insert('1.0', content_text)
                else:
                    self.content_label.configure(state='normal')
                    self.content_label.delete('1.0', 'end')
                    self.content_label.insert('1.0', content_text)
                    self.content_label.configure(state='disabled')
                    
                logger.debug(f"Slide {self.slide_id} content loaded successfully")
            else:
                # Встановлюємо контент за замовчуванням
                self.set_default_content()
                
        except Exception as e:
            logger.error(f"Error loading slide content: {e}")
            self.set_default_content()
            
    def set_default_content(self):
        """Встановлення контенту за замовчуванням"""
        default_titles = {
            1: "BumbleB - Das automatisierte Shuttle",
            2: "BumbleB - Wie die Hummel fährt",
            3: "Einsatzgebiete und Vorteile",
            4: "Sicherheitssysteme",
            5: "Nachhaltigkeit & Umwelt"
        }
        
        default_content = {
            1: "Schonmal ein automatisiert Shuttle gesehen, das aussieht wie eine Hummel?\n\nShuttle fährt los von Bushaltestelle an Bahnhof...",
            2: "Wie die Hummel ihre Flügel nutzt, so nutzt unser BumbleB innovative Technologie für autonomes Fahren.",
            3: "Vielseitige Einsatzmöglichkeiten in urbanen Gebieten für nachhaltigen Transport.",
            4: "Moderne Sicherheitssysteme gewährleisten maximale Sicherheit für alle Passagiere.",
            5: "Nachhaltiger Transport für eine grüne Zukunft - umweltfreundlich und effizient."
        }
        
        title = default_titles.get(self.slide_id, f"Slide {self.slide_id}")
        content = default_content.get(self.slide_id, f"Content für Slide {self.slide_id}")
        
        if self.mode == 'creator':
            self.title_edit.delete('1.0', 'end')
            self.title_edit.insert('1.0', title)
            self.content_edit.delete('1.0', 'end')
            self.content_edit.insert('1.0', content)
        else:
            self.title_label.configure(text=title)
            self.content_label.configure(state='normal')
            self.content_label.delete('1.0', 'end')
            self.content_label.insert('1.0', content)
            self.content_label.configure(state='disabled')
            
    def on_content_changed(self, event=None):
        """Обробка змін контенту"""
        if self.mode == 'creator':
            try:
                # Отримуємо оновлений контент
                title_text = self.title_edit.get('1.0', 'end-1c')
                content_text = self.content_edit.get('1.0', 'end-1c')
                
                # Зберігаємо зміни через content manager
                from models.content import content_manager
                content_manager.update_slide_content(
                    self.slide_id,
                    title_text,
                    content_text
                )
                
                # Викликаємо callbacks для оновлення інших компонентів
                for callback in self.content_changed_callbacks:
                    callback(self.slide_id, {
                        'title': title_text,
                        'content': content_text
                    })
                    
                logger.debug(f"Slide {self.slide_id} content updated")
                
            except Exception as e:
                logger.error(f"Error updating slide content: {e}")
                
    def get_content_data(self):
        """Отримання даних контенту"""
        if self.mode == 'creator':
            return {
                'title': self.title_edit.get('1.0', 'end-1c'),
                'content': self.content_edit.get('1.0', 'end-1c')
            }
        else:
            return {
                'title': self.title_label.cget('text'),
                'content': self.content_label.get('1.0', 'end-1c') if hasattr(self.content_label, 'get') else ""
            }
            
    def update_content(self, content_data):
        """Оновлення контенту слайду"""
        try:
            if 'title' in content_data:
                if self.mode == 'creator':
                    self.title_edit.delete('1.0', 'end')
                    self.title_edit.insert('1.0', content_data['title'])
                else:
                    self.title_label.configure(text=content_data['title'])
                    
            if 'content' in content_data:
                if self.mode == 'creator':
                    self.content_edit.delete('1.0', 'end')
                    self.content_edit.insert('1.0', content_data['content'])
                else:
                    self.content_label.configure(state='normal')
                    self.content_label.delete('1.0', 'end')
                    self.content_label.insert('1.0', content_data['content'])
                    self.content_label.configure(state='disabled')
                    
            logger.debug(f"Slide {self.slide_id} content updated externally")
            
        except Exception as e:
            logger.error(f"Error updating slide content externally: {e}")
    
    def add_content_changed_callback(self, callback):
        """Додає callback для сповіщення про зміни контенту"""
        self.content_changed_callbacks.append(callback)
    
    def save_content(self):
        """Примусове збереження контенту"""
        if self.mode == 'creator':
            self.on_content_changed()
