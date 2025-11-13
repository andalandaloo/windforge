#!/usr/bin/env python3
"""
Icon Showcase - عرض جميع أيقونات التطبيق
يعرض هذا الملف جميع الأيقونات المتاحة في التطبيق لأغراض المراجعة والاختبار
"""

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QScrollArea, QFrame, QGridLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap, QFont

class IconShowcase(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("WindForge - Icon Showcase")
        self.setGeometry(100, 100, 800, 600)
        
        # Set main app icon
        app_icon_path = os.path.join("resources", "icons", "app_icon.svg")
        if os.path.exists(app_icon_path):
            self.setWindowIcon(QIcon(app_icon_path))
        
        # Create central widget and scroll area
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("🎨 WindForge Icons Showcase")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2C5F8F; margin: 20px;")
        scroll_layout.addWidget(title_label)
        
        # Icon categories
        self.add_icon_category(scroll_layout, "📱 App Icons", [
            ("app_icon.svg", "Main App Icon (512x512)"),
            ("app_icon_64.svg", "App Icon Medium (64x64)"),
            ("app_icon_32.svg", "App Icon Small (32x32)")
        ])
        
        self.add_icon_category(scroll_layout, "🧩 Tab Icons", [
            ("rules_tab.svg", "Rules Tab"),
            ("workflow_tab.svg", "Workflow Tab"),
            ("ai_icon.svg", "AI Generator Tab")
        ])
        
        self.add_icon_category(scroll_layout, "🔧 Function Icons", [
            ("generate_button.svg", "Generate Button"),
            ("folder_icon.svg", "Folder Browser"),
            ("preview_icon.svg", "Preview"),
            ("markdown_icon.svg", "Markdown Document")
        ])
        
        self.add_icon_category(scroll_layout, "✅ Status Icons", [
            ("success_icon.svg", "Success Message"),
            ("error_icon.svg", "Error Message"),
            ("validation_icon.svg", "Validation Warning")
        ])
        
        self.add_icon_category(scroll_layout, "💾 Additional Icons", [
            ("save_icon.svg", "Save File"),
            ("settings_icon.svg", "Settings"),
            ("copy_icon.svg", "Copy to Clipboard"),
            ("clear_icon.svg", "Clear Content"),
            ("export_icon.svg", "Export Data"),
            ("import_icon.svg", "Import Data"),
            ("help_icon.svg", "Help & Information"),
            ("refresh_icon.svg", "Refresh/Reload")
        ])
        
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        central_widget.setLayout(main_layout)
        
        # Set stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QScrollArea {
                border: none;
                background-color: #ffffff;
            }
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                margin: 10px;
                padding: 15px;
            }
            QLabel {
                color: #495057;
            }
        """)
    
    def add_icon_category(self, layout, category_title, icons):
        """Add a category of icons to the layout"""
        # Category frame
        category_frame = QFrame()
        category_layout = QVBoxLayout()
        
        # Category title
        category_label = QLabel(category_title)
        category_font = QFont()
        category_font.setPointSize(14)
        category_font.setBold(True)
        category_label.setFont(category_font)
        category_label.setStyleSheet("color: #4A90E2; margin-bottom: 10px;")
        category_layout.addWidget(category_label)
        
        # Icons grid
        icons_grid = QGridLayout()
        icons_grid.setSpacing(20)
        
        for i, (icon_file, description) in enumerate(icons):
            icon_widget = self.create_icon_widget(icon_file, description)
            row = i // 3
            col = i % 3
            icons_grid.addWidget(icon_widget, row, col)
        
        category_layout.addLayout(icons_grid)
        category_frame.setLayout(category_layout)
        layout.addWidget(category_frame)
    
    def create_icon_widget(self, icon_file, description):
        """Create a widget displaying an icon with its description"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Icon display
        icon_path = os.path.join("resources", "icons", icon_file)
        icon_label = QLabel()
        
        if os.path.exists(icon_path):
            # Load and scale icon
            pixmap = QIcon(icon_path).pixmap(64, 64)
            icon_label.setPixmap(pixmap)
        else:
            icon_label.setText("❌")
            icon_label.setStyleSheet("font-size: 32px;")
        
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setFixedSize(80, 80)
        icon_label.setStyleSheet("""
            QLabel {
                border: 2px solid #e9ecef;
                border-radius: 8px;
                background-color: #f8f9fa;
            }
        """)
        
        # File name
        file_label = QLabel(icon_file)
        file_font = QFont()
        file_font.setPointSize(10)
        file_font.setBold(True)
        file_label.setFont(file_font)
        file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        file_label.setStyleSheet("color: #6c757d; margin-top: 5px;")
        
        # Description
        desc_label = QLabel(description)
        desc_font = QFont()
        desc_font.setPointSize(9)
        desc_label.setFont(desc_font)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #868e96; margin-top: 2px;")
        
        layout.addWidget(icon_label)
        layout.addWidget(file_label)
        layout.addWidget(desc_label)
        layout.setSpacing(5)
        
        widget.setLayout(layout)
        widget.setFixedWidth(120)
        
        return widget

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Icon Showcase")
    
    showcase = IconShowcase()
    showcase.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
