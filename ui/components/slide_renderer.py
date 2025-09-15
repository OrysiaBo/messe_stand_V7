#!/usr/bin/env python3
"""
PowerPoint-подібний Slide Renderer
Єдиний дизайн для Demo та Creator
"""

import tkinter as tk
from core.theme import theme_manager

class SlideRenderer:
    """PowerPoint-подібний Slide Renderer для єдиного дизайну"""
    
    @staticmethod
    def render_slide_to_canvas(canvas, slide_data, canvas_width, canvas_height):
        """Рендерить слайд на canvas в PowerPoint стилі"""
        # Очищення canvas
        canvas.delete("all")
        
        # Уніфіковані кольори для кращої читабельності
        bg_color = slide_data.get('background_color', '#FFFFFF')
        text_color = slide_data.get('text_color', '#1F1F1F')
        title_color = '#1E88E5'   # Bertrandt синій
        accent_color = '#FF6600'  # Bertrandt помаранчевий
        
        # Розрахунок оптимального масштабування
        margin = 40
        slide_width = 1920
        slide_height = 1080
        
        scale_x = (canvas_width - margin) / slide_width
        scale_y = (canvas_height - margin) / slide_height
        scale_factor = min(scale_x, scale_y, 1.0)
        
        # Центрована позиція
        scaled_width = slide_width * scale_factor
        scaled_height = slide_height * scale_factor
        offset_x = (canvas_width - scaled_width) / 2
        offset_y = (canvas_height - scaled_height) / 2
        
        # Тінь
        shadow_offset = max(6, int(8 * scale_factor))
        canvas.create_rectangle(
            offset_x + shadow_offset, offset_y + shadow_offset,
            offset_x + scaled_width + shadow_offset, offset_y + scaled_height + shadow_offset,
            fill='#D0D0D0', outline='', tags='slide_shadow'
        )
        
        # Основний фон (білий)
        canvas.create_rectangle(
            offset_x, offset_y, offset_x + scaled_width, offset_y + scaled_height,
            fill=bg_color, outline='#CCCCCC', width=2, tags='slide_background'
        )
        
        # Заголовок
        title = slide_data.get('title', '')
        if title:
            title_y = offset_y + (60 * scale_factor)
            canvas.create_text(
                offset_x + scaled_width / 2, title_y,
                text=title,
                font=('Segoe UI', max(20, int(28 * scale_factor)), 'bold'),
                fill=title_color,
                anchor='center',
                width=scaled_width - (80 * scale_factor),
                tags='slide_title'
            )
            
            # Акцентна лінія під заголовком
            line_y = title_y + (40 * scale_factor)
            canvas.create_line(
                offset_x + (60 * scale_factor), line_y,
                offset_x + scaled_width - (60 * scale_factor), line_y,
                fill=accent_color,
                width=max(3, int(4 * scale_factor)),
                tags='slide_accent'
            )
        
        # Контент
        content = slide_data.get('content', '')
        if content:
            content_y_start = offset_y + (140 * scale_factor)
            content_lines = content.replace('\n\n', '\n').split('\n')
            line_height = max(24, int(30 * scale_factor))
            
            for i, line in enumerate(content_lines[:15]):
                if line.strip():
                    y_pos = content_y_start + (i * line_height)
                    if y_pos < offset_y + scaled_height - (80 * scale_factor):
                        display_text = f"• {line.strip()}" if not line.strip().startswith('•') else line.strip()
                        
                        canvas.create_text(
                            offset_x + (80 * scale_factor),
                            y_pos,
                            text=display_text,
                            font=('Segoe UI', max(10, int(14 * scale_factor))),
                            fill=text_color,
                            anchor='nw',
                            width=scaled_width - (160 * scale_factor),
                            tags='slide_content'
                        )
        
        # Брендинг - логотип Bertrandt (внизу справа)
        canvas.create_text(
            offset_x + scaled_width - (40 * scale_factor),
            offset_y + scaled_height - (30 * scale_factor),
            text="BERTRANDT",
            font=('Segoe UI', max(8, int(12 * scale_factor)), 'bold'),
            fill='#003366',
            anchor='se',
            tags='slide_branding'
        )
        
        # Номер слайду (внизу зліва)
        slide_number = slide_data.get('slide_number', 1)
        canvas.create_text(
            offset_x + (40 * scale_factor),
            offset_y + scaled_height - (30 * scale_factor),
            text=f"Folie {slide_number}",
            font=('Segoe UI', max(6, int(10 * scale_factor))),
            fill='#666666',
            anchor='sw',
            tags='slide_number'
        )
