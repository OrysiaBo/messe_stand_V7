# 🚀 Dynamic Messe Stand V4
**Bertrandt Interactive Display System**

## 📋 Übersicht
Professionelles GUI-System für interaktive Messe-Präsentationen mit ESP32/Arduino GIGA Hardware-Integration.

## 🏗️ Projektstruktur
```
├── main.py                 # Hauptanwendung
├── assets/                 # Bertrandt Logos und Medien
├── content/                # Präsentationsinhalte (Seiten 1-10)
├── core/                   # Kern-Module
│   ├── config.py          # Zentrale Konfiguration
│   ├── logger.py          # Logging-System
│   └── theme.py           # Bertrandt Dark Theme
├── models/                 # Datenmodelle
│   ├── content.py         # Content-Management
│   ├── hardware.py        # Hardware-Verbindungen
│   └── presentation.py    # Präsentations-Logic
├── services/               # Business Logic
│   └── demo.py            # Demo-Services
├── ui/                     # Benutzeroberfläche
│   ├── main_window.py     # Hauptfenster
│   ├── components/        # UI-Komponenten
│   └── tabs/              # Tab-Module
├── presentations/          # Beispiel-Präsentationen
├── docs/                   # Dokumentation
└── logs/                   # Log-Dateien
```

## 🚀 Schnellstart
```bash
# Anwendung starten
python main.py

# Mit Hardware-Verbindungen
python main.py --esp32-port /dev/ttyUSB0

# Ohne Hardware (Demo-Modus)
python main.py --no-hardware

# Debug-Modus
python main.py --debug
```

## 🎨 Features
- **Bertrandt Corporate Design** - Liquid Glass Dark Theme
- **Hardware-Integration** - ESP32 & Arduino GIGA Support
- **Präsentations-Creator** - Drag & Drop Editor
- **Demo-System** - Automatische Präsentationen
- **Responsive Design** - Optimiert für 24" Displays

## 📚 Dokumentation
Siehe `docs/` Verzeichnis für detaillierte Dokumentation:
- Code-Verständnis und Architektur
- ToolBox Design-Konzepte
- Verbesserungsvorschläge

## 🔧 Entwicklung
**Autor:** Marvin Mayer  
**Version:** 4.0.0  
**Lizenz:** © 2025 Bertrandt AG