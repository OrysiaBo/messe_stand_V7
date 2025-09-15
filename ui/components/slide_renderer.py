#!/usr/bin/env python3
"""
Єдиний SlideRenderer для Demo та Creator
Забезпечує ідентичне відображення в обох режимах
"""

import tkinter as tk
from core.theme import theme_manager

class SlideRenderer:
    """Єдиний рендерер слайдів для забезпечення консистентності"""
    
    @staticmethod
    def render_slide_to_canvas(canvas, slide_data, canvas_width, canvas_height):
        """ГОЛОВНИЙ метод рендерингу - використовується для Demo та Creator"""
        # Очистити canvas
        canvas.delete("all")
        
        # ЄДИНІ кольори для обох режимів
        bg_color = '#FFFFFF'      # Білий фон
        title_color = '#1E88E5'   # Bertrandt синій  
        content_color = '#2C3E50' # Темно-сірий для тексту
        accent_color = '#FF6600'  # Bertrandt оранжевий
        border_color = '#CCCCCC'  # Світло-сірий рамка
        
        # Стандартні розміри слайду (16:9)
        slide_width = 1920
        slide_height = 1080
        margin = 40
        
        # Розрахувати оптимальний масштаб
        scale_x = (canvas_width - margin) / slide_width
        scale_y = (canvas_height - margin) / slide_height
        scale_factor = min(scale_x, scale_y, 0.8)  # Максимум 80% від canvas
        
        # Центрування слайду
        scaled_width = slide_width * scale_factor
        scaled_height = slide_height * scale_factor
        offset_x = (canvas_width - scaled_width) / 2
        offset_y = (canvas_height - scaled_height) / 2
        
        # Тінь слайду для глибини
        shadow_offset = max(4, int(6 * scale_factor))
        canvas.create_rectangle(
            offset_x + shadow_offset, offset_y + shadow_offset,
            offset_x + scaled_width + shadow_offset, offset_y + scaled_height + shadow_offset,
            fill='#D0D0D0', outline='', tags='slide_shadow'
        )
        
        # Основний фон слайду
        canvas.create_rectangle(
            offset_x, offset_y, offset_x + scaled_width, offset_y + scaled_height,
            fill=bg_color, outline=border_color, width=2, tags='slide_background'
        )
        
        # Заголовок слайду
        title = slide_data.get('title', '')
        if title:
            title_y = offset_y + (80 * scale_factor)
            canvas.create_text(
                offset_x + scaled_width / 2, title_y,
                text=title,
                font=('Segoe UI', max(16, int(28 * scale_factor)), 'bold'),
                fill=title_color,
                anchor='center',
                width=scaled_width - (100 * scale_factor),
                tags='slide_title'
            )
            
            # Акцентна лінія під заголовком
            line_y = title_y + (40 * scale_factor)
            canvas.create_line(
                offset_x + (80 * scale_factor), line_y,
                offset_x + scaled_width - (80 * scale_factor), line_y,
                fill=accent_color, width=max(2, int(3 * scale_factor)), tags='accent_line'
            )
        
        # Контент слайду
        content = slide_data.get('content', '')
        if content:
            content_y_start = offset_y + (180 * scale_factor)
            content_lines = content.split('\n')
            line_height = max(20, int(28 * scale_factor))
            
            for i, line in enumerate(content_lines[:15]):  # Максимум 15 рядків
                if line.strip():
                    y_pos = content_y_start + (i * line_height)
                    if y_pos < offset_y + scaled_height - (80 * scale_factor):
                        # Додати bullet point для структури
                        display_text = f"• {line.strip()}" if not line.strip().startswith('•') else line.strip()
                        
                        canvas.create_text(
                            offset_x + (80 * scale_factor), y_pos,
                            text=display_text,
                            font=('Segoe UI', max(10, int(14 * scale_factor))),
                            fill=content_color,
                            anchor='nw',
                            width=scaled_width - (160 * scale_factor),
                            tags='slide_content'
                        )
        
        # Брендінг (однаковий для всіх)
        canvas.create_text(
            offset_x + scaled_width - (30 * scale_factor),
            offset_y + scaled_height - (30 * scale_factor),
            text="BERTRANDT",
            font=('Segoe UI', max(8, int(12 * scale_factor)), 'bold'),
            fill='#003366',
            anchor='se',
            tags='slide_branding'
        )
        
        # Номер слайду
        slide_number = slide_data.get('slide_number', 1)
        canvas.create_text(
            offset_x + (30 * scale_factor),
            offset_y + scaled_height - (30 * scale_factor),
            text=f"Folie {slide_number}",
            font=('Segoe UI', max(8, int(10 * scale_factor))),
            fill='#666666',
            anchor='sw',
            tags='slide_number'
        )
    
    @staticmethod
    def render_slide_to_frame(parent_frame, slide_data):
        """Рендерить слайд у Frame (для випадків коли потрібен Frame замість Canvas)"""
        # Очистити frame
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        colors = theme_manager.get_colors()
        
        # PowerPoint-стилізований контейнер
        slide_container = tk.Frame(
            parent_frame,
            bg='#FFFFFF',
            relief='solid',
            bd=2,
            highlightbackground='#CCCCCC',
            highlightthickness=1
        )
        slide_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Заголовок
        title = slide_data.get('title', '')
        if title:
            title_frame = tk.Frame(slide_container, bg='#F8F9FA', height=80)
            title_frame.pack(fill='x', padx=2, pady=(2, 0))
            title_frame.pack_propagate(False)
            
            title_label = tk.Label(
                title_frame,
                text=title,
                font=('Segoe UI', 20, 'bold'),
                fg='#1E88E5',
                bg='#F8F9FA',
                wraplength=800,
                justify='center'
            )
            title_label.pack(expand=True, pady=10)
        
        # Контент
        content = slide_data.get('content', '')
        if content:
            content_frame = tk.Frame(slide_container, bg='#FFFFFF')
            content_frame.pack(fill='both', expand=True, padx=20, pady=20)
            
            content_label = tk.Label(
                content_frame,
                text=content,
                font=('Segoe UI', 12),
                fg='#2C3E50',
                bg='#FFFFFF',
                wraplength=800,
                justify='left',
                anchor='nw'
            )
            content_label.pack(fill='both', expand=True)
        
        # Footer з брендингом
        footer_frame = tk.Frame(slide_container, bg='#F8F9FA', height=30)
        footer_frame.pack(fill='x', padx=2, pady=(0, 2))
        footer_frame.pack_propagate(False)
        
        # Bertrandt брендинг
        branding_label = tk.Label(
            footer_frame,
            text="BERTRANDT",
            font=('Segoe UI', 8, 'bold'),
            fg='#003366',
            bg='#F8F9FA'
        )
        branding_label.pack(side='right', padx=10, pady=5)
        
        # Номер слайду
        slide_number = slide_data.get('slide_number', 1)
        number_label = tk.Label(
            footer_frame,
            text=f"Folie {slide_number}",
            font=('Segoe UI', 8),
            fg='#666666',
            bg='#F8F9FA'
        )
        number_label.pack(side='left', padx=10, pady=5)
    
    @staticmethod
    def get_slide_colors():
        """Повертає стандартні кольори для слайдів"""
        return {
            'background': '#FFFFFF',
            'title': '#1E88E5',
            'content': '#2C3E50', 
            'accent': '#FF6600',
            'border': '#CCCCCC',
            'branding': '#003366',
            'meta': '#666666'
        }
