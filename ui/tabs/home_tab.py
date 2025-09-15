#!/usr/bin/env python3
"""
Home Tab für Dynamic Messe Stand V4
Bertrandt Glass Design Layout
"""

import tkinter as tk
from tkinter import ttk
from core.theme import theme_manager
from core.logger import logger

class HomeTab:
    """Home-Tab mit Bertrandt Glass Cards"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.visible = False
        
        self.create_home_content()
    
    def create_home_content(self):
        """Erstellt den Home-Tab im optimierten Bertrandt Grid-Layout"""
        from core.theme import THEME_VARS, _mix
        
        # Haupt-Container mit optimiertem Padding
        self.container = ttk.Frame(self.parent, style="TFrame")
        
        # Optimiertes Grid-Layout für 24" Display (1920x1080)
        # 3 Spalten mit gleichmäßiger Verteilung
        self.container.columnconfigure((0,1,2), weight=1, minsize=600)
        # 2 Zeilen - obere Zeile etwas kleiner, untere größer
        self.container.rowconfigure(0, weight=2, minsize=300)  # Obere Zeile
        self.container.rowconfigure(1, weight=3, minsize=400)  # Untere Zeile
        
        # Bertrandt Glass Cards mit optimierten Größen erstellen
        self.create_bertrandt_cards()
    
    def create_bertrandt_cards(self):
        """Erstellt optimierte Bertrandt Glass Cards für 24" Display"""
        from core.theme import THEME_VARS, _mix
        
        # Noch größere Padding und Spacing für 24" Display
        card_padding = 30  # Deutlich mehr Padding für bessere Lesbarkeit
        grid_spacing = 18  # Größere Abstände zwischen Cards
        
        # Card 1: System Status (Spalte 0, Zeile 0) - Größere Card
        c1_outer, c1 = self.main_window.make_glass_card(self.container, padding=card_padding)
        c1_outer.grid(row=0, column=0, sticky="nsew", padx=grid_spacing, pady=grid_spacing, ipadx=20, ipady=20)
        
        # Größere Überschriften und Texte - volle Breite
        ttk.Label(c1, text="System Status", style="H1.TLabel").pack(fill="x", pady=(0, 8))
        ttk.Label(c1, text="Hardware-Verbindungen", style="H2.TLabel").pack(fill="x", pady=(0, 15))
        
        # Noch größere Progressbar - volle Breite
        pb = ttk.Progressbar(c1, style="Glass.Horizontal.TProgressbar", mode="determinate")
        pb["value"] = 85
        pb.pack(fill="x", pady=(15, 20))
        
        # Action Buttons - volle Breite
        btnrow = ttk.Frame(c1, style="TFrame")
        btnrow.pack(fill="x", pady=(15, 0))
        btnrow.columnconfigure((0, 1), weight=1)
        ttk.Button(btnrow, text="Details", style="Glass.TButton", 
                  command=lambda: self.show_toast("System-Details angezeigt")).grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ttk.Button(btnrow, text="Demo Starten", style="Primary.TButton", 
                  command=lambda: self.main_window.switch_tab('demo')).grid(row=0, column=1, sticky="ew", padx=(8, 0))
        
        # Card 2: Module (Spalte 1, Zeile 0) - Optimierte Größe
        c2_outer, c2 = self.main_window.make_glass_card(self.container, padding=card_padding)
        c2_outer.grid(row=0, column=1, sticky="nsew", padx=grid_spacing, pady=grid_spacing, ipadx=10, ipady=10)
        
        ttk.Label(c2, text="Module", style="H2.TLabel").pack(fill="x")
        ttk.Label(c2, text="3 aktive • 1 Update", style="Muted.TLabel").pack(fill="x", pady=(0, 10))
        
        # Module Liste - volle Breite
        modules = ["ESP32 Receiver – aktiv", "Arduino GIGA – aktiv", "GUI Engine – aktiv", "Demo Service – bereit"]
        for txt in modules:
            ttk.Label(c2, text="• " + txt).pack(fill="x", pady=4)
        
        # Card 3: Quick Actions (Spalte 2, Zeile 0) - Optimierte Größe
        c3_outer, c3 = self.main_window.make_glass_card(self.container, padding=card_padding)
        c3_outer.grid(row=0, column=2, sticky="nsew", padx=grid_spacing, pady=grid_spacing, ipadx=10, ipady=10)
        
        ttk.Label(c3, text="Quick Actions", style="H2.TLabel").pack(fill="x")
        ttk.Label(c3, text="Schnellzugriffe", style="Muted.TLabel").pack(fill="x", pady=(0, 15))
        
        # Quick Action Buttons - volle Breite
        action_row1 = ttk.Frame(c3, style="TFrame")
        action_row1.pack(fill="x", pady=(10, 8))
        ttk.Button(action_row1, text="Creator", style="Glass.TButton", 
                  command=lambda: self.main_window.switch_tab('creator')).pack(fill="x")
        
        action_row2 = ttk.Frame(c3, style="TFrame")
        action_row2.pack(fill="x", pady=(8, 0))
        ttk.Button(action_row2, text="Präsentation", style="Primary.TButton", 
                  command=lambda: self.main_window.switch_tab('presentation')).pack(fill="x")
        
        # Card 4: Timeline (Spalte 0-1, Zeile 1) - breite Card, optimierte Größe
        c4_outer, c4 = self.main_window.make_glass_card(self.container, padding=card_padding)
        c4_outer.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=grid_spacing, pady=grid_spacing, ipadx=15, ipady=15)
        
        ttk.Label(c4, text="Timeline", style="H2.TLabel").pack(fill="x")
        ttk.Label(c4, text="Letzte Ereignisse", style="Muted.TLabel").pack(fill="x", pady=(0, 15))
        
        # Timeline Events - besserer Abstand und Layout
        events = [
            "12:45 – GUI erfolgreich gestartet",
            "12:42 – Hardware-Verbindungen hergestellt", 
            "12:40 – System initialisiert",
            "12:38 – Bertrandt Theme geladen"
        ]
        
        # Timeline in 2 Spalten für bessere Nutzung des Platzes
        timeline_frame = ttk.Frame(c4, style="TFrame")
        timeline_frame.pack(fill="both", expand=True)
        timeline_frame.columnconfigure((0,1), weight=1)
        
        for i, txt in enumerate(events):
            col = i % 2
            row = i // 2
            ttk.Label(timeline_frame, text="• " + txt).grid(row=row, column=col, sticky="w", padx=(0, 20), pady=6)
        
        # Card 5: Hardware Status (Spalte 2, Zeile 1) - Optimierte Größe
        c5_outer, c5 = self.main_window.make_glass_card(self.container, padding=card_padding)
        c5_outer.grid(row=1, column=2, sticky="nsew", padx=grid_spacing, pady=grid_spacing, ipadx=10, ipady=15)
        
        ttk.Label(c5, text="Hardware", style="H2.TLabel").pack(fill="x")
        ttk.Label(c5, text="Verbindungsstatus", style="Muted.TLabel").pack(fill="x", pady=(0, 15))
        
        # Hardware Status - volle Breite Progressbar
        pb2 = ttk.Progressbar(c5, style="Glass.Horizontal.TProgressbar", mode="determinate")
        pb2["value"] = 92
        pb2.pack(fill="x", pady=(10, 15))
        
        # Hardware Details - volle Breite
        ttk.Label(c5, text="ESP32 & GIGA verbunden", style="TLabel").pack(fill="x", pady=(0, 8))
        ttk.Label(c5, text="Latenz: 12ms", style="Muted.TLabel").pack(fill="x")
    
    def refresh_theme(self):
        """Aktualisiert das Theme für den Home-Tab"""
        from core.theme import THEME_VARS
        
        # Container-Hintergrund aktualisieren (nur für tk.Frame, nicht ttk.Frame)
        if hasattr(self, 'container'):
            try:
                # Prüfen ob es ein tk.Frame ist (hat bg-Option)
                if hasattr(self.container, 'configure') and 'bg' in self.container.configure():
                    self.container.configure(bg=THEME_VARS["bg"])
            except:
                pass  # ttk.Frame unterstützt kein bg
        
        logger.debug("Home-Tab Theme aktualisiert")
    
    def show_toast(self, message):
        """Zeigt eine Toast-Nachricht"""
        from core.theme import _toast
        _toast(self.main_window.root, message)
    
    def show(self):
        """Zeigt den Home-Tab"""
        if not self.visible:
            # Grid-Layout verwenden statt pack, da parent bereits Grid verwendet
            # Optimierte Positionierung für bessere Display-Nutzung
            self.container.grid(row=0, column=0, rowspan=2, columnspan=3, sticky="nsew", padx=20, pady=20)
            self.visible = True
            logger.debug("Home-Tab angezeigt")
    
    def hide(self):
        """Versteckt den Home-Tab"""
        if self.visible:
            self.container.grid_forget()
            self.visible = False
            logger.debug("Home-Tab versteckt")