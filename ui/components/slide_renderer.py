#!/usr/bin/env python3
"""
PowerPoint-ähnlicher Slide Renderer
Einheitliches Design für Demo und Creator
"""

import tkinter as tk
from core.theme import theme_manager

class SlideRenderer:
    """PowerPoint-ähnlicher Slide Renderer für einheitliches Design"""
    
    @staticmethod
    def render_slide_to_canvas(canvas, slide_data, canvas_width, canvas_height):
    # Canvas leeren
    canvas.delete("all")
    
    # EINHEITLICHE FARBEN für bessere Lesbarkeit
    bg_color = slide_data.get('background_color', '#FFFFFF')
    text_color = slide_data.get('text_color', '#1F1F1F')
    title_color = '#1E88E5'   # Bertrandt Blau
    accent_color = '#FF6600'  # Bertrandt Orange
    
    # Optimale Skalierung berechnen
    margin = 40
    scale_x = (canvas_width - margin) / 1920
    scale_y = (canvas_height - margin) / 1080
    scale_factor = min(scale_x, scale_y, 1.0)  # Nie größer als Original
    
    # Zentrierte Position
    scaled_width = 1920 * scale_factor
    scaled_height = 1080 * scale_factor
    offset_x = (canvas_width - scaled_width) / 2
    offset_y = (canvas_height - scaled_height) / 2
    
    # MODERNE SLIDE mit Schatten
    shadow_offset = max(6, int(8 * scale_factor))
    
    # Schatten
    canvas.create_rectangle(
        offset_x + shadow_offset, offset_y + shadow_offset,
        offset_x + scaled_width + shadow_offset, offset_y + scaled_height + shadow_offset,
        fill='#D0D0D0', outline='', tags='slide_shadow'
    )
    
    # Hauptbereich (weiß für gute Lesbarkeit)
    canvas.create_rectangle(
        offset_x, offset_y, offset_x + scaled_width, offset_y + scaled_height,
        fill=bg_color, outline='#CCCCCC', width=2, tags='slide_background'
    )
    
    # TITEL-BEREICH mit besserer Lesbarkeit
    title_height = 100 * scale_factor
    title_y = offset_y + (60 * scale_factor)
    
    title = slide_data.get('title', '')
    if title:
        canvas.create_text(
            offset_x + scaled_width / 2, title_y,
            text=title,
            font=('Segoe UI', max(24, int(32 * scale_factor)), 'bold'),
            fill=title_color,  # Bertrandt Blau für Titel
            anchor='center',
            width=scaled_width - (80 * scale_factor),
            tags='slide_title'
        )
    
    # AKZENT-LINIE unter dem Titel
    line_y = title_y + (50 * scale_factor)
    canvas.create_line(
        offset_x + (60 * scale_factor), line_y,
        offset_x + scaled_width - (60 * scale_factor), line_y,
        fill=accent_color,  # Bertrandt Orange
        width=max(3, int(4 * scale_factor)),
        tags='slide_accent'
    )
    
    # CONTENT-BEREICH mit besserer Formatierung
    content = slide_data.get('content', '')
    if content:
        content_y_start = line_y + (40 * scale_factor)
        content_lines = content.replace('\n\n', '\n').split('\n')
        line_height = max(28, int(35 * scale_factor))
        
        for i, line in enumerate(content_lines[:12]):  # Max 12 Zeilen
            if line.strip() and content_y_start + (i * line_height) < offset_y + scaled_height - (80 * scale_factor):
                # Bullet-Points für bessere Struktur
                display_text = f"• {line.strip()}" if not line.strip().startswith('•') else line.strip()
                
                canvas.create_text(
                    offset_x + (80 * scale_factor),
                    content_y_start + (i * line_height),
                    text=display_text,
                    font=('Segoe UI', max(12, int(16 * scale_factor))),
                    fill=text_color,  # Dunkler Text für gute Lesbarkeit
                    anchor='nw',
                    width=scaled_width - (160 * scale_factor),
                    tags='slide_content'
                )
    
    # BRANDING (konsistent)
    # Bertrandt-Logo (unten rechts)
    canvas.create_text(
        offset_x + scaled_width - (40 * scale_factor),
        offset_y + scaled_height - (40 * scale_factor),
        text="BERTRANDT",
        font=('Segoe UI', max(10, int(14 * scale_factor)), 'bold'),
        fill='#003366',  # Bertrandt Corporate Blau
        anchor='se',
        tags='slide_branding'
    )
    
    # Folien-Nummer (unten links)
    slide_number = slide_data.get('slide_number', 1)
    canvas.create_text(
        offset_x + (40 * scale_factor),
        offset_y + scaled_height - (40 * scale_factor),
        text=f"Folie {slide_number}",
        font=('Segoe UI', max(8, int(12 * scale_factor))),
        fill='#666666',
        anchor='sw',
        tags='slide_number'
    )
    
    @staticmethod
    def render_slide_to_canvas(canvas, slide_data, canvas_width, canvas_height):
        """Rendert eine Slide auf eine Canvas im PowerPoint-Stil"""
        # Canvas leeren
        canvas.delete("all")
        
        # PowerPoint-ähnlicher Hintergrund
        bg_color = slide_data.get('background_color', '#FFFFFF')
        text_color = slide_data.get('text_color', '#1F1F1F')
        
        # Slide-Hintergrund (weißer Bereich mit Schatten)
        shadow_offset = 8
        slide_margin = 40
        
        # Schatten
        canvas.create_rectangle(
            slide_margin + shadow_offset, 
            slide_margin + shadow_offset,
            canvas_width - slide_margin + shadow_offset,
            canvas_height - slide_margin + shadow_offset,
            fill='#D0D0D0',
            outline='',
            tags='slide_shadow'
        )
        
        # Hauptbereich
        canvas.create_rectangle(
            slide_margin, 
            slide_margin,
            canvas_width - slide_margin,
            canvas_height - slide_margin,
            fill=bg_color,
            outline='#CCCCCC',
            width=2,
            tags='slide_background'
        )
        
        # Titel-Bereich (oberer Teil)
        title_height = 120
        canvas.create_rectangle(
            slide_margin + 1, 
            slide_margin + 1,
            canvas_width - slide_margin - 1,
            slide_margin + title_height,
            fill='#F8F9FA',
            outline='#E9ECEF',
            width=1,
            tags='title_area'
        )
        
        # Titel anzeigen
        title = slide_data.get('title', '')
        if title:
            canvas.create_text(
                canvas_width / 2,
                slide_margin + title_height / 2,
                text=title,
                font=('Segoe UI', 24, 'bold'),
                fill='#2C3E50',
                anchor='center',
                width=canvas_width - slide_margin * 2 - 40,
                tags='slide_title'
            )
        
        # Content-Bereich
        content = slide_data.get('content', '')
        if content:
            content_y_start = slide_margin + title_height + 40
            
            # Content in Zeilen aufteilen
            content_lines = content.replace('\n\n', '\n').split('\n')
            line_height = 35
            y_position = content_y_start
            
            for line in content_lines:
                if line.strip() and y_position < canvas_height - slide_margin - 40:
                    canvas.create_text(
                        slide_margin + 60,
                        y_position,
                        text=line.strip(),
                        font=('Segoe UI', 14),
                        fill=text_color,
                        anchor='nw',
                        width=canvas_width - slide_margin * 2 - 120,
                        tags='slide_content'
                    )
                    y_position += line_height
        
        # Bertrandt-Branding (unten rechts)
        canvas.create_text(
            canvas_width - slide_margin - 20,
            canvas_height - slide_margin - 20,
            text="BERTRANDT",
            font=('Segoe UI', 10, 'bold'),
            fill='#003366',
            anchor='se',
            tags='branding'
        )
        
        # Folien-Nummer (unten links)
        slide_number = slide_data.get('slide_number', 1)
        canvas.create_text(
            slide_margin + 20,
            canvas_height - slide_margin - 20,
            text=f"Folie {slide_number}",
            font=('Segoe UI', 10),
            fill='#666666',
            anchor='sw',
            tags='slide_number'
        )
    
    @staticmethod
    def render_slide_to_frame(parent_frame, slide_data):
        """Rendert eine Slide in einem Frame im PowerPoint-Stil"""
        # Frame leeren
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        colors = theme_manager.get_colors()
        
        # PowerPoint-ähnlicher Container
        slide_container = tk.Frame(
            parent_frame,
            bg='#FFFFFF',
            relief='solid',
            bd=2,
            highlightbackground='#CCCCCC',
            highlightthickness=1
        )
        slide_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Titel-Bereich
        title_frame = tk.Frame(
            slide_container,
            bg='#F8F9FA',
            height=80
        )
        title_frame.pack(fill='x', padx=2, pady=(2, 0))
        title_frame.pack_propagate(False)
        
        # Titel
        title = slide_data.get('title', '')
        if title:
            title_label = tk.Label(
                title_frame,
                text=title,
                font=('Segoe UI', 20, 'bold'),
                fg='#2C3E50',
                bg='#F8F9FA',
                wraplength=800,
                justify='center'
            )
            title_label.pack(expand=True, pady=10)
        
        # Content-Bereich
        content_frame = tk.Frame(
            slide_container,
            bg='#FFFFFF'
        )
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Content
        content = slide_data.get('content', '')
        if content:
            # Scrollbarer Text-Bereich
            text_frame = tk.Frame(content_frame, bg='#FFFFFF')
            text_frame.pack(fill='both', expand=True)
            
            scrollbar = tk.Scrollbar(text_frame)
            scrollbar.pack(side='right', fill='y')
            
            text_widget = tk.Text(
                text_frame,
                font=('Segoe UI', 12),
                bg='#FFFFFF',
                fg='#1F1F1F',
                wrap='word',
                relief='flat',
                bd=0,
                state='disabled',
                yscrollcommand=scrollbar.set,
                padx=20,
                pady=20
            )
            text_widget.pack(side='left', fill='both', expand=True)
            scrollbar.config(command=text_widget.yview)
            
            # Content einfügen
            text_widget.configure(state='normal')
            text_widget.insert('1.0', content)
            text_widget.configure(state='disabled')
        
        # Footer
        footer_frame = tk.Frame(
            slide_container,
            bg='#F8F9FA',
            height=30
        )
        footer_frame.pack(fill='x', padx=2, pady=(0, 2))
        footer_frame.pack_propagate(False)
        
        # Bertrandt-Branding
        branding_label = tk.Label(
            footer_frame,
            text="BERTRANDT",
            font=('Segoe UI', 8, 'bold'),
            fg='#003366',
            bg='#F8F9FA'
        )
        branding_label.pack(side='right', padx=10, pady=5)
        
        # Folien-Nummer
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
    def get_powerpoint_colors():
        """Gibt PowerPoint-ähnliche Farben zurück"""
        return {
            'slide_bg': '#FFFFFF',
            'title_bg': '#F8F9FA',
            'border': '#CCCCCC',
            'shadow': '#D0D0D0',
            'title_text': '#2C3E50',
            'content_text': '#1F1F1F',
            'branding': '#003366',
            'meta_text': '#666666'
        }
