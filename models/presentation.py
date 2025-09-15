#!/usr/bin/env python3
"""
Presentation Manager für Dynamic Messe Stand V4
Speichern und Laden von kompletten Präsentationen als JSON/YAML
"""

import json
import yaml
import os
from datetime import datetime
from tkinter import filedialog, messagebox
from core.logger import logger
from models.content import content_manager

class PresentationManager:
    """Verwaltet das Speichern und Laden von kompletten Präsentationen"""
    
    def __init__(self):
        self.current_presentation = None
        self.presentations_dir = "presentations"
        self.ensure_presentations_directory()
    
    def ensure_presentations_directory(self):
        """Stellt sicher, dass das Presentations-Verzeichnis existiert"""
        if not os.path.exists(self.presentations_dir):
            os.makedirs(self.presentations_dir)
            logger.info(f"Presentations-Verzeichnis erstellt: {self.presentations_dir}")
    
    def export_presentation_as_json(self, filename=None):
        """Exportiert die aktuelle Präsentation als JSON"""
        try:
            # Alle Slides sammeln
            slides_data = {}
            all_slides = content_manager.get_all_slides()
            
            for slide_id, slide in all_slides.items():
                slides_data[str(slide_id)] = {
                    'slide_id': slide.slide_id,
                    'title': slide.title,
                    'content': slide.content,
                    'layout': slide.layout,
                    'config_data': slide.config_data,
                    'canvas_elements': slide.config_data.get('canvas_elements', []),
                    'slide_width': slide.config_data.get('slide_width', 1920),
                    'slide_height': slide.config_data.get('slide_height', 1080),
                    'created_at': slide.created_at.isoformat(),
                    'modified_at': slide.modified_at.isoformat()
                }
            
            # Präsentations-Metadaten
            presentation_data = {
                'metadata': {
                    'title': 'BumbleB Präsentation',
                    'description': 'Automatisierte Shuttle-Präsentation',
                    'created_at': datetime.now().isoformat(),
                    'version': '1.0',
                    'total_slides': len(slides_data),
                    'format': 'json'
                },
                'settings': {
                    'slide_duration': 5,
                    'loop_mode': True,
                    'auto_start': False
                },
                'slides': slides_data
            }
            
            # Dateiname bestimmen
            if not filename:
                filename = filedialog.asksaveasfilename(
                    title="Präsentation speichern",
                    defaultextension=".json",
                    filetypes=[
                        ("JSON-Dateien", "*.json"),
                        ("Alle Dateien", "*.*")
                    ],
                    initialdir=self.presentations_dir,
                    initialname=f"bumbleb_presentation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(presentation_data, f, indent=2, ensure_ascii=False)
                
                logger.info(f"Präsentation als JSON gespeichert: {filename}")
                messagebox.showinfo(
                    "Export erfolgreich", 
                    f"Präsentation wurde erfolgreich gespeichert:\n{os.path.basename(filename)}\n\n"
                    f"Folien: {len(slides_data)}\n"
                    f"Format: JSON"
                )
                return filename
            
        except Exception as e:
            logger.error(f"Fehler beim JSON-Export: {e}")
            messagebox.showerror("Export-Fehler", f"Präsentation konnte nicht gespeichert werden:\n{e}")
        
        return None
    
    def export_presentation_as_yaml(self, filename=None):
        """Exportiert die aktuelle Präsentation als YAML"""
        try:
            # Alle Slides sammeln
            slides_data = {}
            all_slides = content_manager.get_all_slides()
            
            for slide_id, slide in all_slides.items():
                slides_data[f"slide_{slide_id}"] = {
                    'id': slide.slide_id,
                    'title': slide.title,
                    'content': slide.content,
                    'layout': slide.layout,
                    'config': slide.config_data,
                    'canvas_elements': slide.config_data.get('canvas_elements', []),
                    'slide_dimensions': {
                        'width': slide.config_data.get('slide_width', 1920),
                        'height': slide.config_data.get('slide_height', 1080)
                    },
                    'timestamps': {
                        'created': slide.created_at.isoformat(),
                        'modified': slide.modified_at.isoformat()
                    }
                }
            
            # Präsentations-Metadaten (YAML-freundlich)
            presentation_data = {
                'presentation': {
                    'metadata': {
                        'title': 'BumbleB Präsentation',
                        'description': 'Automatisierte Shuttle-Präsentation',
                        'created_at': datetime.now().isoformat(),
                        'version': '1.0',
                        'total_slides': len(slides_data),
                        'format': 'yaml'
                    },
                    'settings': {
                        'slide_duration': 5,
                        'loop_mode': True,
                        'auto_start': False
                    }
                },
                'slides': slides_data
            }
            
            # Dateiname bestimmen
            if not filename:
                filename = filedialog.asksaveasfilename(
                    title="Präsentation speichern (YAML)",
                    defaultextension=".yaml",
                    filetypes=[
                        ("YAML-Dateien", "*.yaml"),
                        ("YML-Dateien", "*.yml"),
                        ("Alle Dateien", "*.*")
                    ],
                    initialdir=self.presentations_dir,
                    initialname=f"bumbleb_presentation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
                )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    yaml.dump(presentation_data, f, default_flow_style=False, allow_unicode=True, indent=2)
                
                logger.info(f"Präsentation als YAML gespeichert: {filename}")
                messagebox.showinfo(
                    "Export erfolgreich", 
                    f"Präsentation wurde erfolgreich gespeichert:\n{os.path.basename(filename)}\n\n"
                    f"Folien: {len(slides_data)}\n"
                    f"Format: YAML"
                )
                return filename
            
        except Exception as e:
            logger.error(f"Fehler beim YAML-Export: {e}")
            messagebox.showerror("Export-Fehler", f"Präsentation konnte nicht gespeichert werden:\n{e}")
        
        return None
    
    def load_presentation_from_file(self, filename=None):
        """Lädt eine Präsentation aus einer JSON/YAML-Datei"""
        try:
            if not filename:
                filename = filedialog.askopenfilename(
                    title="Präsentation laden",
                    filetypes=[
                        ("Präsentations-Dateien", "*.json *.yaml *.yml"),
                        ("JSON-Dateien", "*.json"),
                        ("YAML-Dateien", "*.yaml *.yml"),
                        ("Alle Dateien", "*.*")
                    ],
                    initialdir=self.presentations_dir
                )
            
            if not filename or not os.path.exists(filename):
                return False
            
            # Dateiformat bestimmen
            file_ext = os.path.splitext(filename)[1].lower()
            
            with open(filename, 'r', encoding='utf-8') as f:
                if file_ext == '.json':
                    data = json.load(f)
                elif file_ext in ['.yaml', '.yml']:
                    data = yaml.safe_load(f)
                else:
                    raise ValueError(f"Unbekanntes Dateiformat: {file_ext}")
            
            # Daten validieren und laden
            if self.validate_presentation_data(data):
                self.import_slides_from_data(data)
                self.current_presentation = filename
                
                # Erfolgs-Nachricht
                metadata = data.get('metadata', data.get('presentation', {}).get('metadata', {}))
                total_slides = metadata.get('total_slides', 0)
                
                messagebox.showinfo(
                    "Import erfolgreich", 
                    f"Präsentation wurde erfolgreich geladen:\n{os.path.basename(filename)}\n\n"
                    f"Folien: {total_slides}\n"
                    f"Format: {file_ext[1:].upper()}"
                )
                
                logger.info(f"Präsentation geladen: {filename}")
                return True
            
        except Exception as e:
            logger.error(f"Fehler beim Laden der Präsentation: {e}")
            messagebox.showerror("Import-Fehler", f"Präsentation konnte nicht geladen werden:\n{e}")
        
        return False
    
    def validate_presentation_data(self, data):
        """Validiert die Struktur der Präsentationsdaten"""
        try:
            # JSON-Format
            if 'slides' in data and 'metadata' in data:
                return True
            
            # YAML-Format
            if 'presentation' in data and 'slides' in data:
                return True
            
            logger.error("Ungültige Präsentationsstruktur")
            return False
            
        except Exception as e:
            logger.error(f"Fehler bei der Datenvalidierung: {e}")
            return False
    
    def import_slides_from_data(self, data):
        """Importiert Slides aus den Präsentationsdaten"""
        try:
            # Format bestimmen und Slides extrahieren
            if 'slides' in data and 'metadata' in data:
                # JSON-Format
                slides_data = data['slides']
                settings = data.get('settings', {})
            else:
                # YAML-Format
                slides_data = data['slides']
                settings = data.get('presentation', {}).get('settings', {})
            
            # Bestehende Slides löschen (nach Bestätigung)
            if content_manager.get_slide_count() > 0:
                result = messagebox.askyesno(
                    "Bestehende Folien", 
                    "Sollen die bestehenden Folien überschrieben werden?\n\n"
                    "Ja = Alle bestehenden Folien löschen und neue laden\n"
                    "Nein = Neue Folien zu bestehenden hinzufügen"
                )
                
                if result:
                    # Alle bestehenden Slides löschen
                    for slide_id in list(content_manager.slides.keys()):
                        content_manager.delete_slide(slide_id)
            
            # Neue Slides importieren
            imported_count = 0
            for slide_key, slide_data in slides_data.items():
                try:
                    # Slide-ID extrahieren
                    if isinstance(slide_data, dict):
                        slide_id = slide_data.get('slide_id', slide_data.get('id', 1))
                        title = slide_data.get('title', f'Slide {slide_id}')
                        content = slide_data.get('content', '')
                        layout = slide_data.get('layout', 'text')
                        config_data = slide_data.get('config_data', slide_data.get('config', {}))
                        
                        # Canvas-Elemente und Dimensionen
                        canvas_elements = slide_data.get('canvas_elements', [])
                        slide_width = slide_data.get('slide_width', slide_data.get('slide_dimensions', {}).get('width', 1920))
                        slide_height = slide_data.get('slide_height', slide_data.get('slide_dimensions', {}).get('height', 1080))
                        
                        # Slide erstellen oder aktualisieren
                        if content_manager.create_slide(slide_id, title, content, layout):
                            # Config-Daten mit Canvas-Elementen aktualisieren
                            slide = content_manager.get_slide(slide_id)
                            if slide:
                                slide.config_data.update(config_data)
                                slide.config_data['canvas_elements'] = canvas_elements
                                slide.config_data['slide_width'] = slide_width
                                slide.config_data['slide_height'] = slide_height
                                content_manager.save_slide(slide_id)
                            
                            imported_count += 1
                        
                except Exception as e:
                    logger.error(f"Fehler beim Importieren von Slide {slide_key}: {e}")
            
            logger.info(f"{imported_count} Slides erfolgreich importiert")
            
            # Demo-Service über neue Slides informieren
            from services.demo import demo_service
            demo_service.reset_to_first_slide()
            
        except Exception as e:
            logger.error(f"Fehler beim Importieren der Slides: {e}")
            raise
    
    def get_available_presentations(self):
        """Gibt eine Liste verfügbarer Präsentationen zurück"""
        presentations = []
        
        try:
            if os.path.exists(self.presentations_dir):
                for filename in os.listdir(self.presentations_dir):
                    if filename.endswith(('.json', '.yaml', '.yml')):
                        filepath = os.path.join(self.presentations_dir, filename)
                        stat = os.stat(filepath)
                        presentations.append({
                            'filename': filename,
                            'filepath': filepath,
                            'size': stat.st_size,
                            'modified': datetime.fromtimestamp(stat.st_mtime)
                        })
        
        except Exception as e:
            logger.error(f"Fehler beim Auflisten der Präsentationen: {e}")
        
        return sorted(presentations, key=lambda x: x['modified'], reverse=True)

# Globale Presentation-Manager Instanz
presentation_manager = PresentationManager()