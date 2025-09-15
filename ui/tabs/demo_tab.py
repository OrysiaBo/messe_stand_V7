#!/usr/bin/env python3
"""
Demo Tab для Dynamic Messe Stand V4
Автоматичне відтворення презентацій з синхронізацією з Creator
"""

import tkinter as tk
from tkinter import ttk
from core.theme import theme_manager
from core.logger import logger
from models.content import content_manager
from ui.components.slide_renderer import SlideRenderer

class DemoTab:
    """Demo Tab для автоматичного відтворення презентацій"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.current_slide = 1
        self.total_slides = 10
        self.is_running = False
        self.slide_duration = 5000  # мілісекунди
        self.demo_timer = None
        
        # Підписка на зміни контенту
        content_manager.add_observer(self.on_content_changed)
        
        self.create_demo_content()
    
    def create_demo_content(self):
        """Створює контент Demo Tab"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        
        # Головний контейнер
        self.container = tk.Frame(self.parent, bg=colors['background_primary'])
        
        # Header з контролами
        self.create_demo_header()
        
        # Головна область презентації
        self.create_presentation_area()
        
        # Навігація та контроли
        self.create_navigation_controls()
        
        # Sidebar зі списком слайдів
        self.create_slides_sidebar()
        
        # Завантажити поточний слайд
        self.load_current_slide()
    
    def create_demo_header(self):
        """Створює header з контролами демо"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        
        header_frame = tk.Frame(
            self.container,
            bg=colors['background_secondary'],
            height=70
        )
        header_frame.pack(fill='x', padx=10, pady=(10, 5))
        header_frame.pack_propagate(False)
        
        # Ліва частина - заголовок
        left_frame = tk.Frame(header_frame, bg=colors['background_secondary'])
        left_frame.pack(side='left', fill='y', padx=15)
        
        title_label = tk.Label(
            left_frame,
            text="📽️ BumbleB Story Demo",
            font=fonts['title'],
            fg=colors['text_primary'],
            bg=colors['background_secondary']
        )
        title_label.pack(anchor='w', pady=(10, 0))
        
        subtitle_label = tk.Label(
            left_frame,
            text="Automatische Präsentation",
            font=fonts['caption'],
            fg=colors['text_secondary'],
            bg=colors['background_secondary']
        )
        subtitle_label.pack(anchor='w')
        
        # Права частина - контроли
        right_frame = tk.Frame(header_frame, bg=colors['background_secondary'])
        right_frame.pack(side='right', fill='y', padx=15)
        
        # Demo контроли
        controls_frame = tk.Frame(right_frame, bg=colors['background_secondary'])
        controls_frame.pack(pady=15)
        
        # Play/Pause кнопка
        self.play_button = tk.Button(
            controls_frame,
            text="▶ Demo Starten",
            font=fonts['button'],
            bg=colors['accent_primary'],
            fg='white',
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.toggle_demo
        )
        self.play_button.pack(side='left', padx=(0, 10))
        
        # Швидкість демо
        speed_frame = tk.Frame(controls_frame, bg=colors['background_secondary'])
        speed_frame.pack(side='left', padx=10)
        
        tk.Label(
            speed_frame,
            text="Dauer:",
            font=fonts['caption'],
            fg=colors['text_secondary'],
            bg=colors['background_secondary']
        ).pack(side='left')
        
        self.speed_var = tk.StringVar(value="5s")
        speed_combo = ttk.Combobox(
            speed_frame,
            textvariable=self.speed_var,
            values=["3s", "5s", "7s", "10s"],
            width=5,
            state="readonly"
        )
        speed_combo.pack(side='left', padx=(5, 0))
        speed_combo.bind('<<ComboboxSelected>>', self.on_speed_changed)
    
    def create_presentation_area(self):
        """Створює головну область презентації"""
        colors = theme_manager.get_colors()
        
        # Контейнер для презентації
        presentation_frame = tk.Frame(self.container, bg=colors['background_primary'])
        presentation_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Створюємо 2-колонковий layout
        presentation_frame.grid_columnconfigure(1, weight=1)
        presentation_frame.grid_rowconfigure(0, weight=1)
        
        # Ліва частина - список слайдів (буде створено в create_slides_sidebar)
        self.sidebar_frame = tk.Frame(
            presentation_frame, 
            bg=colors['background_secondary'],
            width=250
        )
        self.sidebar_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        self.sidebar_frame.grid_propagate(False)
        
        # Права частина - головна презентація
        main_presentation_frame = tk.Frame(
            presentation_frame,
            bg=colors['background_secondary'],
            relief='solid',
            bd=1
        )
        main_presentation_frame.grid(row=0, column=1, sticky='nsew')
        
        # Canvas для відображення слайдів
        self.slide_canvas = tk.Canvas(
            main_presentation_frame,
            bg='#E8E8E8',  # Сірий фон для контрасту з білими слайдами
            relief='flat',
            bd=0,
            highlightthickness=0
        )
        self.slide_canvas.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Bind resize для адаптивності
        self.slide_canvas.bind('<Configure>', self.on_canvas_resize)
    
    def create_navigation_controls(self):
        """Створює навігаційні контроли"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        
        nav_frame = tk.Frame(
            self.container,
            bg=colors['background_secondary'],
            height=60
        )
        nav_frame.pack(fill='x', padx=10, pady=(5, 10))
        nav_frame.pack_propagate(False)
        
        # Центральна навігація
        center_nav = tk.Frame(nav_frame, bg=colors['background_secondary'])
        center_nav.pack(expand=True)
        
        # Кнопка "Назад"
        self.prev_button = tk.Button(
            center_nav,
            text="◀◀ Zurück",
            font=fonts['button'],
            bg=colors['background_tertiary'],
            fg=colors['text_primary'],
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.previous_slide
        )
        self.prev_button.pack(side='left', padx=10, pady=15)
        
        # Лічильник слайдів
        self.slide_counter = tk.Label(
            center_nav,
            text=f"{self.current_slide}/{self.total_slides}",
            font=fonts['subtitle'],
            fg=colors['text_primary'],
            bg=colors['background_secondary']
        )
        self.slide_counter.pack(side='left', padx=20, pady=15)
        
        # Кнопка "Далі"
        self.next_button = tk.Button(
            center_nav,
            text="Weiter ▶▶",
            font=fonts['button'],
            bg=colors['background_tertiary'],
            fg=colors['text_primary'],
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.next_slide
        )
        self.next_button.pack(side='left', padx=10, pady=15)
    
    def create_slides_sidebar(self):
        """Створює sidebar зі списком слайдів"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        
        # Header sidebar
        header_label = tk.Label(
            self.sidebar_frame,
            text="📋 BumbleB Story",
            font=fonts['subtitle'],
            fg=colors['text_primary'],
            bg=colors['background_secondary']
        )
        header_label.pack(fill='x', padx=15, pady=(15, 5))
        
        info_label = tk.Label(
            self.sidebar_frame,
            text="10 Folien verfügbar",
            font=fonts['caption'],
            fg=colors['text_secondary'],
            bg=colors['background_secondary']
        )
        info_label.pack(fill='x', padx=15, pady=(0, 15))
        
        # Scrollable список слайдів
        canvas = tk.Canvas(
            self.sidebar_frame,
            bg=colors['background_secondary'],
            highlightthickness=0
        )
        scrollbar = tk.Scrollbar(
            self.sidebar_frame,
            orient="vertical",
            command=canvas.yview
        )
        self.slides_list_frame = tk.Frame(canvas, bg=colors['background_secondary'])
        
        self.slides_list_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.slides_list_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=(0, 15))
        scrollbar.pack(side="right", fill="y", pady=(0, 15))
        
        # Створити список слайдів
        self.create_slides_list()
        
        # Status внизу
        status_frame = tk.Frame(
            self.sidebar_frame,
            bg=colors['background_secondary']
        )
        status_frame.pack(fill='x', side='bottom', padx=15, pady=15)
        
        self.status_label = tk.Label(
            status_frame,
            text="Demo bereit - BumbleB Story mit 10 Folien geladen",
            font=fonts['caption'],
            fg=colors['text_tertiary'],
            bg=colors['background_secondary'],
            wraplength=200
        )
        self.status_label.pack()
    
    def create_slides_list(self):
        """Створює список слайдів у sidebar"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        
        # Очищуємо існуючі слайди
        for widget in self.slides_list_frame.winfo_children():
            widget.destroy()
        
        self.slide_buttons = {}
        
        # Отримуємо слайди з content_manager
        slides = content_manager.get_all_slides()
        self.total_slides = len(slides)
        
        for slide_id in sorted(slides.keys()):
            slide = slides[slide_id]
            
            # Контейнер для кнопки слайду
            slide_container = tk.Frame(
                self.slides_list_frame,
                bg=colors['background_secondary']
            )
            slide_container.pack(fill='x', padx=5, pady=2)
            
            # Визначити чи активний слайд
            is_active = slide_id == self.current_slide
            bg_color = colors['accent_primary'] if is_active else colors['background_tertiary']
            fg_color = 'white' if is_active else colors['text_primary']
            
            # Скоротити заголовок для відображення
            title = slide.title
            display_title = title[:20] + "..." if len(title) > 20 else title
            
            slide_button = tk.Button(
                slide_container,
                text=f"{slide_id}\n{display_title}",
                font=fonts['body'],
                bg=bg_color,
                fg=fg_color,
                relief='flat',
                bd=0,
                width=22,
                height=3,
                cursor='hand2',
                command=lambda sid=slide_id: self.go_to_slide(sid),
                justify='left'
            )
            slide_button.pack(fill='x', ipady=2)
            
            self.slide_buttons[slide_id] = slide_button
        
        # Оновити лічильник
        self.update_slide_counter()
    
    def on_canvas_resize(self, event):
        """Обробник зміни розміру canvas для адаптивності"""
        # Оновити відображення поточного слайду
        self.render_current_slide()
    
    def load_current_slide(self):
        """Завантажує поточний слайд"""
        self.render_current_slide()
        self.update_slide_list_selection()
        self.update_slide_counter()
    
    def render_current_slide(self):
        """Відображає поточний слайд на canvas"""
        try:
            # Отримати дані слайду
            slide = content_manager.get_slide(self.current_slide)
            
            if slide:
                # Отримати розміри canvas
                canvas_width = self.slide_canvas.winfo_width()
                canvas_height = self.slide_canvas.winfo_height()
                
                if canvas_width > 10 and canvas_height > 10:
                    # Підготувати дані слайду для рендерера
                    slide_data = {
                        'title': slide.title,
                        'content': slide.content,
                        'slide_number': self.current_slide,
                        'background_color': '#FFFFFF',
                        'text_color': '#1F1F1F'
                    }
                    
                    # Використати SlideRenderer для єдиного стилю
                    SlideRenderer.render_slide_to_canvas(
                        self.slide_canvas,
                        slide_data,
                        canvas_width,
                        canvas_height
                    )
                    
                    logger.debug(f"Rendered slide {self.current_slide} in demo")
            else:
                # Показати заглушку якщо слайд не знайдено
                self.render_placeholder()
                
        except Exception as e:
            logger.error(f"Error rendering slide {self.current_slide}: {e}")
            self.render_placeholder()
    
    def render_placeholder(self):
        """Відображає заглушку коли слайд не може бути завантажений"""
        self.slide_canvas.delete("all")
        
        canvas_width = self.slide_canvas.winfo_width()
        canvas_height = self.slide_canvas.winfo_height()
        
        # Центрований плейсхолдер
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        
        self.slide_canvas.create_text(
            center_x, center_y - 20,
            text="📽️",
            font=('Arial', 48),
            fill='#CCCCCC',
            anchor='center'
        )
        
        self.slide_canvas.create_text(
            center_x, center_y + 30,
            text="Slide wird geladen...",
            font=('Segoe UI', 16),
            fill='#999999',
            anchor='center'
        )
    
    def update_slide_list_selection(self):
        """Оновлює виділення в списку слайдів"""
        colors = theme_manager.get_colors()
        
        for slide_id, button in self.slide_buttons.items():
            if slide_id == self.current_slide:
                button.configure(
                    bg=colors['accent_primary'],
                    fg='white'
                )
            else:
                button.configure(
                    bg=colors['background_tertiary'],
                    fg=colors['text_primary']
                )
    
    def update_slide_counter(self):
        """Оновлює лічільник слайдів"""
        self.slide_counter.configure(text=f"{self.current_slide}/{self.total_slides}")
    
    def toggle_demo(self):
        """Переключає режим демо (запуск/зупинка)"""
        if self.is_running:
            self.stop_demo()
        else:
            self.start_demo()
    
    def start_demo(self):
        """Запускає автоматичне демо"""
        self.is_running = True
        self.play_button.configure(
            text="⏸ Demo Stoppen",
            bg=theme_manager.get_colors()['accent_warning']
        )
        
        # Почати автоматичну зміну слайдів
        self.schedule_next_slide()
        
        logger.info("Demo started")
    
    def stop_demo(self):
        """Зупиняє автоматичне демо"""
        self.is_running = False
        self.play_button.configure(
            text="▶ Demo Starten",
            bg=theme_manager.get_colors()['accent_primary']
        )
        
        # Скасувати таймер
        if self.demo_timer:
            self.main_window.root.after_cancel(self.demo_timer)
            self.demo_timer = None
        
        logger.info("Demo stopped")
    
    def schedule_next_slide(self):
        """Планує перехід до наступного слайду"""
        if self.is_running:
            self.demo_timer = self.main_window.root.after(
                self.slide_duration,
                self.auto_next_slide
            )
    
    def auto_next_slide(self):
        """Автоматичний перехід до наступного слайду"""
        if self.is_running:
            if self.current_slide < self.total_slides:
                self.next_slide()
            else:
                # Повернутися до початку або зупинити
                self.current_slide = 1
                self.load_current_slide()
            
            # Запланувати наступний слайд
            self.schedule_next_slide()
    
    def previous_slide(self):
        """Перехід до попереднього слайду"""
        if self.current_slide > 1:
            self.current_slide -= 1
        else:
            self.current_slide = self.total_slides  # Циклічний перехід
        
        self.load_current_slide()
    
    def next_slide(self):
        """Перехід до наступного слайду"""
        if self.current_slide < self.total_slides:
            self.current_slide += 1
        else:
            self.current_slide = 1  # Циклічний перехід
        
        self.load_current_slide()
    
    def go_to_slide(self, slide_id):
        """Перехід до конкретного слайду"""
        if 1 <= slide_id <= self.total_slides:
            self.current_slide = slide_id
            self.load_current_slide()
    
    def on_speed_changed(self, event=None):
        """Обробник зміни швидкості демо"""
        speed_text = self.speed_var.get()
        speed_seconds = int(speed_text.replace('s', ''))
        self.slide_duration = speed_seconds * 1000  # конвертувати в мілісекунди
        
        logger.debug(f"Demo speed changed to {speed_seconds} seconds")
    
    def on_content_changed(self, slide_id, slide_data, action='update'):
        """Обробник зміни контенту (синхронізація з Creator)"""
        try:
            if action == 'update' or action == 'load':
                # Оновити список слайдів
                self.create_slides_list()
                
                # Перемалювати поточний слайд якщо він був змінений
                if slide_id == self.current_slide:
                    self.render_current_slide()
                
                logger.debug(f"Demo synchronized with content changes for slide {slide_id}")
                
            elif action == 'delete':
                # Обробити видалення слайду
                if slide_id == self.current_slide and self.current_slide > 1:
                    self.current_slide -= 1
                
                self.create_slides_list()
                self.load_current_slide()
        
        except Exception as e:
            logger.error(f"Error handling content change in demo: {e}")
    
    def show(self):
        """Показати Demo Tab"""
        self.container.pack(fill='both', expand=True)
        
        # Оновити контент при показі
        self.create_slides_list()
        self.load_current_slide()
    
    def hide(self):
        """Приховати Demo Tab"""
        # Зупинити демо при переключенні табів
        if self.is_running:
            self.stop_demo()
        
        self.container.pack_forget()
