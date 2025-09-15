import json
import os

class StyleManager(QObject):
    """
    Менеджер стилів для забезпечення консистентності між режимами
    """
    style_updated = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.settings = QSettings('Bertrandt', 'MesseStand')
        self.default_styles = self._get_default_styles()
        
    def _get_default_styles(self):
        """Базові стилі для всіх елементів"""
        return {
            'slide_title': {
                'font_family': 'Arial',
                'font_size': 24,
                'font_weight': 'bold',
                'color': '#FFFFFF',
                'background': 'transparent',
                'padding': '10px',
                'margin': '5px',
                'text_align': 'center'
            },
            'slide_content': {
                'font_family': 'Arial', 
                'font_size': 14,
                'font_weight': 'normal',
                'color': '#FFFFFF',
                'background': 'transparent',
                'padding': '15px',
                'margin': '10px',
                'line_height': '1.4'
            },
            'container': {
                'background': '#2b2b2b',
                'border': '1px solid #404040',
                'border_radius': '8px',
                'margin': '5px',
                'padding': '10px'
            }
        }
    
    def get_style_sheet(self, element_type):
        """Генерує CSS стиль для елементу"""
        styles = self.default_styles.get(element_type, {})
        
        css = f"""
        QLabel[elementType="{element_type}"] {{
            font-family: {styles.get('font_family', 'Arial')};
            font-size: {styles.get('font_size', 12)}px;
            font-weight: {styles.get('font_weight', 'normal')};
            color: {styles.get('color', '#FFFFFF')};
            background: {styles.get('background', 'transparent')};
            padding: {styles.get('padding', '5px')};
            margin: {styles.get('margin', '2px')};
        }}
        
        QTextEdit[elementType="{element_type}"] {{
            font-family: {styles.get('font_family', 'Arial')};
            font-size: {styles.get('font_size', 12)}px;
            color: {styles.get('color', '#FFFFFF')};
            background: {styles.get('background', '#2b2b2b')};
            border: {styles.get('border', '1px solid #404040')};
            border-radius: {styles.get('border_radius', '4px')};
            padding: {styles.get('padding', '5px')};
        }}
        """
        return css.strip()
    
    def save_slide_content(self, slide_id, content_data):
        """Зберігає контент слайду з стилями"""
        slide_key = f'slide_{slide_id}'
        self.settings.setValue(slide_key, json.dumps(content_data))
        
    def load_slide_content(self, slide_id):
        """Завантажує контент слайду"""
        slide_key = f'slide_{slide_id}'
        content_json = self.settings.value(slide_key, '{}')
        try:
            return json.loads(content_json)
        except:
            return {}
