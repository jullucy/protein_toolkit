"""
Centralized styling system for the Protein Tool application.
Provides consistent themes and reusable style components.
"""

from enum import Enum
from typing import Dict, Optional

class Theme(Enum):
    """Available themes for the application"""
    LIGHT_BLUE = "light_blue"
    DARK_BLUE = "dark_blue"
    LIGHT = "light"
    DARK = "dark"

class StyleManager:
    """Manages application-wide styling and themes"""
    
    def __init__(self, theme: Theme = Theme.LIGHT_BLUE):
        self.current_theme = theme
        self._themes = self._define_themes()
    
    def _define_themes(self) -> Dict[Theme, Dict[str, str]]:
        """Define color palettes for different themes"""
        return {
            Theme.LIGHT_BLUE: {
                'primary': '#1E6FBC',           # Main blue
                'primary_dark': '#0D47A1',      # Dark blue
                'primary_light': '#BBDEFB',     # Light blue for text/borders
                'secondary': '#42A5F5',         # Secondary blue
                'background': '#333333',        # Dark gray background
                'surface': '#2F2F2F',           # Darker gray surface
                'surface_variant': '#424242',   # Medium gray surface
                'text': '#BBDEFB',              # Light blue text
                'text_secondary': '#90A4AE',    # Light gray text
                'success': '#4CAF50',           # Green
                'warning': '#FF9800',           # Orange
                'error': '#F44336',             # Red
                'border': '#BBDEFB',            # Light blue border
                'hover': '#404040',             # Dark hover
                'disabled': '#555555',          # Gray disabled
            },
            Theme.DARK_BLUE: {
                'primary': '#1E6FBC',
                'primary_dark': '#0D47A1',
                'primary_light': '#BBDEFB',
                'secondary': '#42A5F5',
                'background': '#333333',
                'surface': '#2F2F2F',
                'surface_variant': '#424242',
                'text': '#BBDEFB',
                'text_secondary': '#90A4AE',
                'success': '#4CAF50',
                'warning': '#FF9800',
                'error': '#F44336',
                'border': '#BBDEFB',
                'hover': '#404040',
                'disabled': '#555555',
            },
            Theme.LIGHT: {
                'primary': '#2196F3',
                'primary_dark': '#1976D2',
                'primary_light': '#E3F2FD',
                'secondary': '#FF9800',
                'background': '#FAFAFA',
                'surface': '#FFFFFF',
                'surface_variant': '#F5F5F5',
                'text': '#212121',
                'text_secondary': '#757575',
                'success': '#4CAF50',
                'warning': '#FF9800',
                'error': '#F44336',
                'border': '#E0E0E0',
                'hover': '#F5F5F5',
                'disabled': '#EEEEEE',
            }
        }
    
    def get_colors(self) -> Dict[str, str]:
        """Get current theme colors"""
        return self._themes[self.current_theme]
    
    def set_theme(self, theme: Theme):
        """Change the current theme"""
        self.current_theme = theme
    
    def get_color(self, color_name: str) -> str:
        """Get a specific color from current theme"""
        colors = self.get_colors()
        return colors.get(color_name, colors['primary'])

# Global style manager instance
style_manager = StyleManager(Theme.LIGHT_BLUE)

def get_group_box_style() -> str:
    """Standard group box styling"""
    colors = style_manager.get_colors()
    return f"""
        QGroupBox {{
            font-size: 14px;
            font-weight: bold;
            color: {colors['text']};
            border: 2px solid {colors['border']};
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 15px;
            background-color: {colors['surface']};
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 15px;
            padding: 0 8px;
            background-color: {colors['primary']};
            color: white;
            border-radius: 4px;
        }}
    """

def get_button_style(variant: str = 'primary') -> str:
    """Standard button styling with variants"""
    colors = style_manager.get_colors()
    
    color_map = {
        'primary': colors['primary'],
        'secondary': colors['secondary'], 
        'success': colors['success'],
        'warning': colors['warning'],
        'error': colors['error']
    }
    
    bg_color = color_map.get(variant, colors['primary'])
    
    # Calculate hover color (slightly darker)
    hover_color = colors['primary_dark'] if variant == 'primary' else bg_color
    
    return f"""
        QPushButton {{
            background-color: {bg_color};
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            min-width: 80px;
        }}
        QPushButton:hover {{
            background-color: {hover_color};
        }}
        QPushButton:pressed {{
            background-color: {colors['primary_dark']};
        }}
        QPushButton:disabled {{
            background-color: {colors['disabled']};
            color: {colors['text_secondary']};
        }}
    """

def get_input_style() -> str:
    """Standard input field styling"""
    colors = style_manager.get_colors()
    return f"""
        QDoubleSpinBox, QSpinBox, QLineEdit, QComboBox {{
            padding: 8px;
            border: 2px solid {colors['border']};
            border-radius: 4px;
            background-color: {colors['surface']};
            color: {colors['text']};
            font-size: 14px;
        }}
        QDoubleSpinBox:focus, QSpinBox:focus, QLineEdit:focus, QComboBox:focus {{
            border-color: {colors['primary']};
        }}
        QDoubleSpinBox:disabled, QSpinBox:disabled, QLineEdit:disabled {{
            background-color: {colors['disabled']};
            color: {colors['text_secondary']};
        }}
        QComboBox::drop-down {{
            border: none;
            background: {colors['primary']};
            width: 20px;
            border-radius: 0 4px 4px 0;
        }}
        QComboBox::down-arrow {{
            image: none;
            width: 0;
            height: 0;
            border: 4px solid transparent;
            border-top: 6px solid white;
            margin: 4px;
        }}
    """

def get_input_highlighted_style() -> str:
    """Highlighted input style for calculated fields"""
    colors = style_manager.get_colors()
    return f"""
        QDoubleSpinBox:disabled, QSpinBox:disabled {{
            background-color: {colors['surface_variant']};
            border: 2px solid {colors['primary']};
            color: {colors['text']};
            font-weight: bold;
        }}
    """

def get_label_style(variant: str = 'normal') -> str:
    """Standard label styling with variants"""
    colors = style_manager.get_colors()
    
    if variant == 'title':
        return f"""
            QLabel {{
                color: {colors['primary']};
                font-size: 18px;
                font-weight: bold;
                background: {colors['surface_variant']};
                padding: 20px;
                border: 2px solid {colors['border']};
                border-radius: 10px;
                margin-bottom: 15px;
            }}
        """
    elif variant == 'subtitle':
        return f"""
            QLabel {{
                color: {colors['text']};
                font-size: 16px;
                font-weight: bold;
            }}
        """
    elif variant == 'result_success':
        return f"""
            QLabel {{
                background-color: #E8F5E9;
                color: #2E7D32;
                padding: 15px;
                border-radius: 8px;
                border: 2px solid {colors['success']};
                font-size: 14px;
                font-weight: bold;
            }}
        """
    elif variant == 'result_error':
        return f"""
            QLabel {{
                background-color: #FFEBEE;
                color: #C62828;
                padding: 15px;
                border-radius: 8px;
                border: 2px solid {colors['error']};
                font-size: 14px;
                font-weight: bold;
            }}
        """
    else:  # normal
        return f"""
            QLabel {{
                color: {colors['text']};
                font-weight: bold;
                font-size: 14px;
            }}
        """

def get_table_style() -> str:
    """Standard table styling"""
    colors = style_manager.get_colors()
    return f"""
        QTableWidget {{
            border: 2px solid {colors['border']};
            border-radius: 8px;
            background-color: {colors['surface']};
            color: {colors['text']};
            gridline-color: {colors['border']};
            selection-background-color: {colors['hover']};
        }}
        QHeaderView::section {{
            background-color: {colors['primary']};
            color: white;
            padding: 10px;
            border: none;
            font-weight: bold;
        }}
        QTableWidget::item {{
            padding: 8px;
            border-bottom: 1px solid {colors['border']};
        }}
        QTableWidget::item:selected {{
            background-color: {colors['hover']};
        }}
    """

def get_text_edit_style() -> str:
    """Standard text edit styling"""
    colors = style_manager.get_colors()
    return f"""
        QTextEdit {{
            border: 2px solid {colors['border']};
            border-radius: 8px;
            background-color: {colors['surface']};
            color: {colors['text']};
            padding: 10px;
            font-size: 14px;
        }}
        QTextEdit:focus {{
            border-color: {colors['primary']};
        }}
    """

def get_tab_widget_style() -> str:
    """Standard tab widget styling"""
    colors = style_manager.get_colors()
    return f"""
        QTabWidget::pane {{
            border: 2px solid {colors['border']};
            border-radius: 8px;
            background-color: {colors['surface']};
        }}
        QTabBar::tab {{
            background-color: {colors['background']};
            color: {colors['text']};
            padding: 12px 20px;
            margin: 2px;
            border: 2px solid {colors['border']};
            border-bottom: none;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            font-weight: bold;
            min-width: 120px;
        }}
        QTabBar::tab:selected {{
            background-color: {colors['primary']};
            color: white;
            border-color: {colors['primary']};
        }}
        QTabBar::tab:hover:!selected {{
            background-color: {colors['hover']};
        }}
    """

def get_main_widget_style() -> str:
    """Main widget background styling"""
    colors = style_manager.get_colors()
    return f"""
        QWidget {{
            background-color: {colors['background']};
            color: {colors['text']};
        }}
    """

def get_scroll_area_style() -> str:
    """Scroll area styling"""
    colors = style_manager.get_colors()
    return f"""
        QScrollArea {{
            border: none;
            background-color: {colors['background']};
        }}
        QScrollBar:vertical {{
            border: none;
            background: {colors['surface']};
            width: 12px;
            border-radius: 6px;
        }}
        QScrollBar::handle:vertical {{
            background: {colors['border']};
            border-radius: 6px;
            min-height: 20px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {colors['primary']};
        }}
    """

def apply_dark_theme():
    """Switch to dark theme"""
    style_manager.set_theme(Theme.DARK_BLUE)

def apply_light_theme():
    """Switch to light theme"""
    style_manager.set_theme(Theme.LIGHT_BLUE)

def get_html_colors() -> Dict[str, str]:
    """Get current theme colors for HTML content"""
    return style_manager.get_colors()

def generate_theory_html(title: str, content: str, equations: str = "", 
                        parameters_table: str = "", applications: str = "") -> str:
    """Generate consistent HTML for theory panels"""
    colors = get_html_colors()
    
    html = f"""
    <div style="padding: 15px; background: {colors['surface']}; border-radius: 8px;">
    <h2 style="color: {colors['primary']}; margin-top: 0;">{title}</h2>
    <p style="color: {colors['text']};">{content}</p>
    """
    
    if equations:
        html += f"""
        <h3 style="color: {colors['primary']};">Key Equations</h3>
        <div style="background: {colors['surface_variant']}; padding: 15px; border-radius: 8px; 
                    border-left: 4px solid {colors['primary']}; margin: 15px 0;">
        {equations}
        </div>
        """
    
    if parameters_table:
        html += f"""
        <h3 style="color: {colors['primary']};">Parameters</h3>
        {parameters_table}
        """
    
    if applications:
        html += f"""
        <h3 style="color: {colors['primary']};">Applications</h3>
        <div style="color: {colors['text']}; padding: 10px;">
        {applications}
        </div>
        """
    
    html += "</div>"
    return html

def generate_parameters_table(parameters: list) -> str:
    """Generate consistent parameter table HTML"""
    colors = get_html_colors()
    
    html = f"""
    <table style="width: 100%; border-collapse: collapse; background: {colors['surface']}; 
                  color: {colors['text']}; border-radius: 8px; overflow: hidden;">
    <tr style="background: {colors['primary']}; color: white;">
        <th style="padding: 12px; text-align: left;">Parameter</th>
        <th style="padding: 12px; text-align: left;">Symbol</th>
        <th style="padding: 12px; text-align: left;">Units</th>
        <th style="padding: 12px; text-align: left;">Typical Range</th>
    </tr>
    """
    
    for i, (name, symbol, units, range_val) in enumerate(parameters):
        bg_color = colors['surface_variant'] if i % 2 == 1 else colors['surface']
        html += f"""
        <tr style="background: {bg_color};">
            <td style="padding: 10px;"><strong>{name}</strong></td>
            <td style="padding: 10px;">{symbol}</td>
            <td style="padding: 10px;">{units}</td>
            <td style="padding: 10px;">{range_val}</td>
        </tr>
        """
    
    html += "</table>"
    return html

def generate_results_html(title: str, results: dict, quality_info: dict = None) -> str:
    """Generate consistent results display HTML"""
    colors = get_html_colors()
    
    html = f"""
    <div style="padding: 15px;">
    <h3 style="color: {colors['primary']}; margin-top: 0;">{title}</h3>
    
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 15px;">
    """
    
    for key, value in results.items():
        html += f"""
        <tr>
            <td style="padding: 8px; font-weight: bold; color: {colors['text']};">{key}:</td>
            <td style="padding: 8px; color: {colors['text']};">{value}</td>
        </tr>
        """
    
    html += "</table>"
    
    if quality_info:
        quality = quality_info.get('quality', 'Unknown')
        if quality == 'Excellent':
            color = colors['success']
        elif quality == 'Good':
            color = colors['warning']
        else:
            color = colors['error']
            
        html += f"""
        <div style="padding: 10px; background-color: {color}20; 
                    border-left: 4px solid {color}; border-radius: 4px;">
            <strong style="color: {color};">Fit Quality: {quality}</strong>
        </div>
        """
    
    html += "</div>"
    return html
