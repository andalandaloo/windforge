"""
Theme Loader for WindForge
Handles loading and applying Qt Style Sheets (QSS)
"""

import os
from typing import Optional
from PyQt6.QtWidgets import QApplication


class ThemeLoader:
    """Handles loading and applying themes to the application"""
    
    def __init__(self):
        self.current_theme = None
        self.themes_dir = os.path.join("resources", "styles")
    
    def load_theme(self, theme_name: str) -> bool:
        """
        Load and apply a theme to the application
        
        Args:
            theme_name: Name of the theme file (without .qss extension)
            
        Returns:
            bool: True if theme was loaded successfully, False otherwise
        """
        theme_path = os.path.join(self.themes_dir, f"{theme_name}.qss")
        
        if not os.path.exists(theme_path):
            print(f"⚠️  Theme file not found: {theme_path}")
            return False
        
        try:
            with open(theme_path, 'r', encoding='utf-8') as file:
                stylesheet = file.read()
            
            # Apply the stylesheet to the application
            app = QApplication.instance()
            if app:
                app.setStyleSheet(stylesheet)
                self.current_theme = theme_name
                print(f"✅ Theme '{theme_name}' loaded successfully")
                return True
            else:
                print("❌ No QApplication instance found")
                return False
                
        except Exception as e:
            print(f"❌ Error loading theme '{theme_name}': {e}")
            return False
    
    def load_apple_theme(self) -> bool:
        """Load the Apple-style theme"""
        return self.load_theme("apple_theme")
    
    def get_current_theme(self) -> Optional[str]:
        """Get the name of the currently loaded theme"""
        return self.current_theme
    
    def get_available_themes(self) -> list:
        """Get list of available theme files"""
        if not os.path.exists(self.themes_dir):
            return []
        
        themes = []
        for file in os.listdir(self.themes_dir):
            if file.endswith('.qss'):
                themes.append(file[:-4])  # Remove .qss extension
        
        return themes
    
    def reset_theme(self) -> None:
        """Reset to default Qt theme"""
        app = QApplication.instance()
        if app:
            app.setStyleSheet("")
            self.current_theme = None
            print("🔄 Theme reset to default")


# Global theme loader instance
theme_loader = ThemeLoader()


def apply_apple_theme() -> bool:
    """
    Convenience function to apply Apple theme
    
    Returns:
        bool: True if theme was applied successfully
    """
    return theme_loader.load_apple_theme()


def get_theme_loader() -> ThemeLoader:
    """Get the global theme loader instance"""
    return theme_loader
