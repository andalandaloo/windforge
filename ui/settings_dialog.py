import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget, 
    QFormLayout, QLineEdit, QSpinBox, QCheckBox, QComboBox,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox,
    QFileDialog, QGroupBox, QTextEdit, QLabel, QSlider
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QFont

from core.config_manager import ConfigManager

class SettingsDialog(QDialog):
    """Settings dialog for the Windsurf Generator application"""
    
    settings_changed = pyqtSignal()
    
    def __init__(self, config_manager: ConfigManager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.init_ui()
        self.load_settings()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("WindForge Settings")
        self.setModal(True)
        self.resize(700, 600)
        
        # Apply Apple-style window design
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                color: #1d1d1f;
            }
            
            QTabWidget::pane {
                border: none;
                background-color: #ffffff;
                border-radius: 12px;
                margin-top: 8px;
            }
            
            QTabBar::tab {
                background-color: transparent;
                color: #86868b;
                padding: 12px 20px;
                margin-right: 4px;
                border: none;
                border-radius: 8px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                font-size: 14px;
                font-weight: 500;
                min-width: 100px;
            }
            
            QTabBar::tab:selected {
                background-color: #007aff;
                color: #ffffff;
                font-weight: 600;
            }
            
            QTabBar::tab:hover:!selected {
                background-color: #f2f2f7;
                color: #1d1d1f;
            }
            
            QGroupBox {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                font-size: 16px;
                font-weight: 600;
                color: #1d1d1f;
                border: 1px solid #e5e5e7;
                border-radius: 12px;
                margin-top: 12px;
                padding-top: 16px;
                background-color: #ffffff;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px;
                background-color: #ffffff;
            }
            
            QLineEdit, QSpinBox, QComboBox {
                border: 1px solid #d1d1d6;
                border-radius: 8px;
                padding: 8px 12px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                font-size: 14px;
                background-color: #ffffff;
                color: #1d1d1f;
                selection-background-color: #007aff;
            }
            
            QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
                border: 2px solid #007aff;
                outline: none;
            }
            
            QPushButton {
                background-color: #007aff;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                font-size: 14px;
                font-weight: 600;
                min-height: 20px;
            }
            
            QPushButton:hover {
                background-color: #0056b3;
            }
            
            QPushButton:pressed {
                background-color: #004494;
            }
            
            QLabel {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                color: #1d1d1f;
                font-size: 14px;
            }
            
            QCheckBox {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                color: #1d1d1f;
                font-size: 14px;
                spacing: 8px;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 1px solid #d1d1d6;
                background-color: #ffffff;
            }
            
            QCheckBox::indicator:checked {
                background-color: #007aff;
                border: 1px solid #007aff;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDQuNUw0LjUgOEwxMSAxIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
            }
            
            QCheckBox::indicator:hover {
                border-color: #007aff;
            }
        """)
        
        # Set settings icon
        settings_icon_path = os.path.join("resources", "icons", "settings_icon.svg")
        if os.path.exists(settings_icon_path):
            self.setWindowIcon(QIcon(settings_icon_path))
        
        layout = QVBoxLayout()
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Create tabs
        self.general_tab = self.create_general_tab()
        self.paths_tab = self.create_paths_tab()
        self.ai_tab = self.create_ai_tab()
        self.categories_tab = self.create_categories_tab()
        self.ui_tab = self.create_ui_tab()
        self.templates_tab = self.create_templates_tab()
        
        # Add tabs with icons
        general_icon = QIcon("resources/icons/general-settings.svg")
        paths_icon = QIcon("resources/icons/paths-settings.svg")
        ai_icon = QIcon("resources/icons/ai-settings.svg")
        categories_icon = QIcon("resources/icons/categories-settings.svg")
        interface_icon = QIcon("resources/icons/interface-settings.svg")
        templates_icon = QIcon("resources/icons/templates-settings.svg")
        
        self.tab_widget.addTab(self.general_tab, general_icon, "General")
        self.tab_widget.addTab(self.paths_tab, paths_icon, "Paths")
        self.tab_widget.addTab(self.ai_tab, ai_icon, "AI Settings")
        self.tab_widget.addTab(self.categories_tab, categories_icon, "Categories")
        self.tab_widget.addTab(self.ui_tab, interface_icon, "Interface")
        self.tab_widget.addTab(self.templates_tab, templates_icon, "Templates")
        
        layout.addWidget(self.tab_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.btn_reset = QPushButton("Reset to Defaults")
        self.btn_reset.setIcon(QIcon("resources/icons/reset-settings.svg"))
        self.btn_reset.clicked.connect(self.reset_to_defaults)
        
        self.btn_export = QPushButton("Export Settings")
        self.btn_export.setIcon(QIcon("resources/icons/export-settings.svg"))
        self.btn_export.clicked.connect(self.export_settings)
        
        self.btn_import = QPushButton("Import Settings")
        self.btn_import.setIcon(QIcon("resources/icons/import-settings.svg"))
        self.btn_import.clicked.connect(self.import_settings)
        
        button_layout.addWidget(self.btn_reset)
        button_layout.addWidget(self.btn_export)
        button_layout.addWidget(self.btn_import)
        button_layout.addStretch()
        
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.reject)
        
        self.btn_ok = QPushButton("OK")
        self.btn_ok.clicked.connect(self.accept_settings)
        self.btn_ok.setDefault(True)
        
        button_layout.addWidget(self.btn_cancel)
        button_layout.addWidget(self.btn_ok)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        # Apply styles
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e9ecef;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #0078d4;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
    
    def create_general_tab(self):
        """Create general settings tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # File settings group
        file_group = QGroupBox("File Settings")
        file_layout = QFormLayout()
        
        self.auto_timestamp_cb = QCheckBox()
        file_layout.addRow("Auto timestamp:", self.auto_timestamp_cb)
        
        self.backup_files_cb = QCheckBox()
        file_layout.addRow("Backup files:", self.backup_files_cb)
        
        self.encoding_combo = QComboBox()
        self.encoding_combo.addItems(["utf-8", "utf-16", "ascii"])
        file_layout.addRow("Default encoding:", self.encoding_combo)
        
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_paths_tab(self):
        """Create paths settings tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Default paths group
        paths_group = QGroupBox("Default Paths")
        paths_layout = QFormLayout()
        
        # Rules path
        rules_layout = QHBoxLayout()
        self.rules_path_edit = QLineEdit()
        self.btn_browse_rules = QPushButton("Browse")
        self.btn_browse_rules.clicked.connect(self.browse_rules_path)
        rules_layout.addWidget(self.rules_path_edit)
        rules_layout.addWidget(self.btn_browse_rules)
        paths_layout.addRow("Rules folder:", rules_layout)
        
        # Workflows path
        workflows_layout = QHBoxLayout()
        self.workflows_path_edit = QLineEdit()
        self.btn_browse_workflows = QPushButton("Browse")
        self.btn_browse_workflows.clicked.connect(self.browse_workflows_path)
        workflows_layout.addWidget(self.workflows_path_edit)
        workflows_layout.addWidget(self.btn_browse_workflows)
        paths_layout.addRow("Workflows folder:", workflows_layout)
        
        paths_group.setLayout(paths_layout)
        layout.addWidget(paths_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_ai_tab(self):
        """Create AI settings tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # AI Configuration group
        ai_config_group = QGroupBox("AI Configuration")
        ai_config_layout = QFormLayout()
        
        # Google API Key
        api_key_layout = QHBoxLayout()
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_edit.setPlaceholderText("Enter your Google Gemini API Key...")
        
        self.btn_show_api_key = QPushButton()
        self.btn_show_api_key.setIcon(QIcon("resources/icons/eye-show.svg"))
        self.btn_show_api_key.setMaximumWidth(40)
        self.btn_show_api_key.setCheckable(True)
        self.btn_show_api_key.clicked.connect(self.toggle_api_key_visibility)
        
        self.btn_test_api_key = QPushButton("Test")
        self.btn_test_api_key.setIcon(QIcon("resources/icons/test-api.svg"))
        self.btn_test_api_key.clicked.connect(self.test_api_key)
        
        api_key_layout.addWidget(self.api_key_edit)
        api_key_layout.addWidget(self.btn_show_api_key)
        api_key_layout.addWidget(self.btn_test_api_key)
        
        ai_config_layout.addRow("Google API Key:", api_key_layout)
        
        # AI Status
        self.ai_status_label = QLabel("Not configured")
        self.ai_status_label.setStyleSheet("""
            color: #86868b;
            font-style: italic;
            padding: 4px 8px;
            background-color: #f2f2f7;
            border-radius: 4px;
        """)
        ai_config_layout.addRow("AI Status:", self.ai_status_label)
        
        # AI Model Settings
        ai_model_layout = QFormLayout()
        
        # Model selection
        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "gemini-1.5-flash",
            "gemini-1.5-pro", 
            "gemini-1.0-pro"
        ])
        ai_model_layout.addRow("AI Model:", self.model_combo)
        
        # Temperature setting
        self.temperature_slider = QSlider(Qt.Orientation.Horizontal)
        self.temperature_slider.setMinimum(0)
        self.temperature_slider.setMaximum(100)
        self.temperature_slider.setValue(70)
        self.temperature_slider.valueChanged.connect(self.update_temperature_label)
        
        temp_layout = QHBoxLayout()
        self.temperature_label = QLabel("0.7")
        temp_layout.addWidget(self.temperature_slider)
        temp_layout.addWidget(self.temperature_label)
        
        ai_model_layout.addRow("Temperature:", temp_layout)
        
        # Max tokens
        self.max_tokens_spin = QSpinBox()
        self.max_tokens_spin.setMinimum(100)
        self.max_tokens_spin.setMaximum(8192)
        self.max_tokens_spin.setValue(2048)
        ai_model_layout.addRow("Max Tokens:", self.max_tokens_spin)
        
        ai_config_group.setLayout(ai_config_layout)
        layout.addWidget(ai_config_group)
        
        # AI Model Settings group
        ai_model_group = QGroupBox("Model Settings")
        ai_model_group.setLayout(ai_model_layout)
        layout.addWidget(ai_model_group)
        
        # AI Features group
        ai_features_group = QGroupBox("AI Features")
        ai_features_layout = QVBoxLayout()
        
        self.enable_ai_rules_cb = QCheckBox("Enable AI Rules Generation")
        self.enable_ai_rules_cb.setChecked(True)
        ai_features_layout.addWidget(self.enable_ai_rules_cb)
        
        self.enable_ai_workflows_cb = QCheckBox("Enable AI Workflows Generation")
        self.enable_ai_workflows_cb.setChecked(True)
        ai_features_layout.addWidget(self.enable_ai_workflows_cb)
        
        self.auto_analyze_project_cb = QCheckBox("Auto-analyze project structure")
        self.auto_analyze_project_cb.setChecked(True)
        ai_features_layout.addWidget(self.auto_analyze_project_cb)
        
        ai_features_group.setLayout(ai_features_layout)
        layout.addWidget(ai_features_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_categories_tab(self):
        """Create categories management tab"""
        tab = QWidget()
        layout = QHBoxLayout()
        
        # Categories list
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Available Categories:"))
        
        self.categories_list = QListWidget()
        left_layout.addWidget(self.categories_list)
        
        # Category management buttons
        cat_buttons_layout = QHBoxLayout()
        
        self.btn_add_category = QPushButton("Add")
        self.btn_add_category.clicked.connect(self.add_category)
        
        self.btn_remove_category = QPushButton("Remove")
        self.btn_remove_category.clicked.connect(self.remove_category)
        
        cat_buttons_layout.addWidget(self.btn_add_category)
        cat_buttons_layout.addWidget(self.btn_remove_category)
        cat_buttons_layout.addStretch()
        
        left_layout.addLayout(cat_buttons_layout)
        
        # New category input
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Add New Category:"))
        
        self.new_category_edit = QLineEdit()
        self.new_category_edit.setPlaceholderText("Enter category name...")
        self.new_category_edit.returnPressed.connect(self.add_category)
        right_layout.addWidget(self.new_category_edit)
        
        right_layout.addStretch()
        
        layout.addLayout(left_layout, 2)
        layout.addLayout(right_layout, 1)
        tab.setLayout(layout)
        return tab
    
    def create_ui_tab(self):
        """Create UI settings tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Window settings group
        window_group = QGroupBox("Window Settings")
        window_layout = QFormLayout()
        
        self.window_width_spin = QSpinBox()
        self.window_width_spin.setRange(800, 2000)
        self.window_width_spin.setSuffix(" px")
        window_layout.addRow("Window width:", self.window_width_spin)
        
        self.window_height_spin = QSpinBox()
        self.window_height_spin.setRange(600, 1500)
        self.window_height_spin.setSuffix(" px")
        window_layout.addRow("Window height:", self.window_height_spin)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["light", "dark", "auto"])
        window_layout.addRow("Theme:", self.theme_combo)
        
        window_group.setLayout(window_layout)
        layout.addWidget(window_group)
        
        # Editor settings group
        editor_group = QGroupBox("Editor Settings")
        editor_layout = QFormLayout()
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 24)
        self.font_size_spin.setSuffix(" pt")
        editor_layout.addRow("Font size:", self.font_size_spin)
        
        self.word_wrap_cb = QCheckBox()
        editor_layout.addRow("Word wrap:", self.word_wrap_cb)
        
        self.line_numbers_cb = QCheckBox()
        editor_layout.addRow("Show line numbers:", self.line_numbers_cb)
        
        self.auto_save_preview_cb = QCheckBox()
        editor_layout.addRow("Auto-save preview:", self.auto_save_preview_cb)
        
        editor_group.setLayout(editor_layout)
        layout.addWidget(editor_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_templates_tab(self):
        """Create templates settings tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Template selection
        template_layout = QHBoxLayout()
        template_layout.addWidget(QLabel("Template:"))
        
        self.template_combo = QComboBox()
        self.template_combo.addItems(["Rule Template", "Workflow Template"])
        self.template_combo.currentTextChanged.connect(self.load_template)
        template_layout.addWidget(self.template_combo)
        template_layout.addStretch()
        
        layout.addLayout(template_layout)
        
        # Template editor
        self.template_edit = QTextEdit()
        self.template_edit.setPlaceholderText("Template content will appear here...")
        layout.addWidget(self.template_edit)
        
        # Template buttons
        template_buttons = QHBoxLayout()
        
        self.btn_reset_template = QPushButton("Reset Template")
        self.btn_reset_template.clicked.connect(self.reset_template)
        
        template_buttons.addWidget(self.btn_reset_template)
        template_buttons.addStretch()
        
        layout.addLayout(template_buttons)
        
        tab.setLayout(layout)
        return tab
    
    def load_settings(self):
        """Load settings from config manager"""
        # General tab
        self.auto_timestamp_cb.setChecked(self.config_manager.get('file_settings.auto_timestamp', True))
        self.backup_files_cb.setChecked(self.config_manager.get('file_settings.backup_files', False))
        encoding = self.config_manager.get('file_settings.default_encoding', 'utf-8')
        self.encoding_combo.setCurrentText(encoding)
        
        # Paths tab
        self.rules_path_edit.setText(self.config_manager.get('default_paths.rules', '.windsurf/rules'))
        self.workflows_path_edit.setText(self.config_manager.get('default_paths.workflows', '.windsurf/workflows'))
        
        # Categories tab
        self.load_categories()
        
        # UI tab
        self.window_width_spin.setValue(self.config_manager.get('ui_settings.window_width', 1200))
        self.window_height_spin.setValue(self.config_manager.get('ui_settings.window_height', 800))
        theme = self.config_manager.get('ui_settings.theme', 'light')
        self.theme_combo.setCurrentText(theme)
        self.font_size_spin.setValue(self.config_manager.get('ui_settings.font_size', 10))
        self.word_wrap_cb.setChecked(self.config_manager.get('ui_settings.word_wrap', True))
        self.line_numbers_cb.setChecked(self.config_manager.get('ui_settings.show_line_numbers', False))
        self.auto_save_preview_cb.setChecked(self.config_manager.get('ui_settings.auto_save_preview', True))
        
        # Templates tab
        self.load_template()
        
        # AI tab
        self.load_ai_settings()
    
    def load_categories(self):
        """Load categories into the list widget"""
        self.categories_list.clear()
        categories = self.config_manager.get_categories()
        for category in categories:
            self.categories_list.addItem(category)
    
    def load_template(self):
        """Load selected template"""
        template_name = self.template_combo.currentText()
        if template_name == "Rule Template":
            template = self.config_manager.get('templates.rule_template', {})
        else:
            template = self.config_manager.get('templates.workflow_template', {})
        
        # Convert template dict to text
        template_text = ""
        for key, value in template.items():
            template_text += f"{key}: {value}\n"
        
        self.template_edit.setPlainText(template_text)
    
    def add_category(self):
        """Add new category"""
        category = self.new_category_edit.text().strip()
        if category:
            if self.config_manager.add_category(category):
                self.load_categories()
                self.new_category_edit.clear()
                QMessageBox.information(self, "Success", f"Category '{category}' added successfully!")
            else:
                QMessageBox.warning(self, "Warning", f"Category '{category}' already exists!")
    
    def remove_category(self):
        """Remove selected category"""
        current_item = self.categories_list.currentItem()
        if current_item:
            category = current_item.text()
            reply = QMessageBox.question(
                self, "Confirm", 
                f"Are you sure you want to remove category '{category}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                if self.config_manager.remove_category(category):
                    self.load_categories()
                    QMessageBox.information(self, "Success", f"Category '{category}' removed successfully!")
    
    def browse_rules_path(self):
        """Browse for rules folder"""
        folder = QFileDialog.getExistingDirectory(self, "Select Rules Folder", self.rules_path_edit.text())
        if folder:
            self.rules_path_edit.setText(folder)
    
    def browse_workflows_path(self):
        """Browse for workflows folder"""
        folder = QFileDialog.getExistingDirectory(self, "Select Workflows Folder", self.workflows_path_edit.text())
        if folder:
            self.workflows_path_edit.setText(folder)
    
    def reset_template(self):
        """Reset current template to default"""
        reply = QMessageBox.question(
            self, "Confirm", 
            "Are you sure you want to reset this template to default?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.load_template()
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        reply = QMessageBox.question(
            self, "Confirm", 
            "Are you sure you want to reset all settings to defaults?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.config_manager.reset_to_defaults()
            self.load_settings()
            QMessageBox.information(self, "Success", "Settings reset to defaults!")
    
    def export_settings(self):
        """Export settings to file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Settings", "windsurf_settings.json", 
            "JSON Files (*.json);;All Files (*)"
        )
        if file_path:
            if self.config_manager.export_config(file_path):
                QMessageBox.information(self, "Success", f"Settings exported to {file_path}")
            else:
                QMessageBox.critical(self, "Error", "Failed to export settings!")
    
    def import_settings(self):
        """Import settings from file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Settings", "", 
            "JSON Files (*.json);;All Files (*)"
        )
        if file_path:
            if self.config_manager.import_config(file_path):
                self.load_settings()
                QMessageBox.information(self, "Success", f"Settings imported from {file_path}")
            else:
                QMessageBox.critical(self, "Error", "Failed to import settings!")
    
    def accept_settings(self):
        """Save settings and close dialog"""
        # Save general settings
        self.config_manager.set('file_settings.auto_timestamp', self.auto_timestamp_cb.isChecked())
        self.config_manager.set('file_settings.backup_files', self.backup_files_cb.isChecked())
        self.config_manager.set('file_settings.default_encoding', self.encoding_combo.currentText())
        
        # Save paths
        self.config_manager.set('default_paths.rules', self.rules_path_edit.text())
        self.config_manager.set('default_paths.workflows', self.workflows_path_edit.text())
        
        # Save UI settings
        self.config_manager.set('ui_settings.window_width', self.window_width_spin.value())
        self.config_manager.set('ui_settings.window_height', self.window_height_spin.value())
        self.config_manager.set('ui_settings.theme', self.theme_combo.currentText())
        self.config_manager.set('ui_settings.font_size', self.font_size_spin.value())
        self.config_manager.set('ui_settings.word_wrap', self.word_wrap_cb.isChecked())
        self.config_manager.set('ui_settings.show_line_numbers', self.line_numbers_cb.isChecked())
        self.config_manager.set('ui_settings.auto_save_preview', self.auto_save_preview_cb.isChecked())
        
        # Save AI settings
        self.config_manager.set('ai_settings.api_key', self.api_key_edit.text())
        self.config_manager.set('ai_settings.model', self.model_combo.currentText())
        self.config_manager.set('ai_settings.temperature', self.temperature_slider.value() / 100.0)
        self.config_manager.set('ai_settings.max_tokens', self.max_tokens_spin.value())
        self.config_manager.set('ai_settings.enable_rules', self.enable_ai_rules_cb.isChecked())
        self.config_manager.set('ai_settings.enable_workflows', self.enable_ai_workflows_cb.isChecked())
        self.config_manager.set('ai_settings.auto_analyze', self.auto_analyze_project_cb.isChecked())
        
        # Save configuration
        self.config_manager.save_config()
        
        # Emit signal that settings changed
        self.settings_changed.emit()
        
        self.accept()
    
    def toggle_api_key_visibility(self):
        """Toggle API key visibility"""
        if self.btn_show_api_key.isChecked():
            self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.btn_show_api_key.setIcon(QIcon("resources/icons/eye-hide.svg"))
        else:
            self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.btn_show_api_key.setIcon(QIcon("resources/icons/eye-show.svg"))
    
    def update_temperature_label(self, value):
        """Update temperature label"""
        temp = value / 100.0
        self.temperature_label.setText(f"{temp:.1f}")
    
    def test_api_key(self):
        """Test the API key"""
        api_key = self.api_key_edit.text().strip()
        if not api_key:
            QMessageBox.warning(self, "Warning", "Please enter an API key first.")
            return
        
        try:
            # Import AI generator to test
            from core.generators import AI_AVAILABLE
            if not AI_AVAILABLE:
                QMessageBox.warning(self, "AI Not Available", 
                    "AI features are not available. Please check your installation.")
                return
            
            from core.generators.ai_generator import AIGenerator
            ai_generator = AIGenerator()
            
            # Test the API key
            success = ai_generator.set_api_key(api_key)
            if success:
                self.ai_status_label.setText("✅ API key is valid")
                self.ai_status_label.setStyleSheet("""
                    color: #30d158;
                    font-weight: 600;
                    padding: 4px 8px;
                    background-color: #f0fff4;
                    border-radius: 4px;
                """)
                QMessageBox.information(self, "Success", 
                    "✅ API key is valid and working!")
            else:
                self.ai_status_label.setText("❌ Invalid API key")
                self.ai_status_label.setStyleSheet("""
                    color: #ff3b30;
                    font-weight: 600;
                    padding: 4px 8px;
                    background-color: #fff5f5;
                    border-radius: 4px;
                """)
                QMessageBox.warning(self, "Invalid API Key", 
                    "❌ The API key is invalid or there's a connection issue.")
                
        except Exception as e:
            self.ai_status_label.setText("⚠️ Test failed")
            self.ai_status_label.setStyleSheet("""
                color: #ff9500;
                font-weight: 600;
                padding: 4px 8px;
                background-color: #fff8f0;
                border-radius: 4px;
            """)
            QMessageBox.critical(self, "Test Failed", 
                f"❌ Failed to test API key:\n\n{str(e)}")
    
    def load_ai_settings(self):
        """Load AI settings from config"""
        try:
            # Load API key
            api_key = self.config_manager.get('ai_settings.api_key', '')
            self.api_key_edit.setText(api_key)
            
            # Load model
            model = self.config_manager.get('ai_settings.model', 'gemini-1.5-flash')
            index = self.model_combo.findText(model)
            if index >= 0:
                self.model_combo.setCurrentIndex(index)
            
            # Load temperature
            temperature = self.config_manager.get('ai_settings.temperature', 0.7)
            self.temperature_slider.setValue(int(temperature * 100))
            
            # Load max tokens
            max_tokens = self.config_manager.get('ai_settings.max_tokens', 2048)
            self.max_tokens_spin.setValue(max_tokens)
            
            # Load feature flags
            self.enable_ai_rules_cb.setChecked(
                self.config_manager.get('ai_settings.enable_rules', True))
            self.enable_ai_workflows_cb.setChecked(
                self.config_manager.get('ai_settings.enable_workflows', True))
            self.auto_analyze_project_cb.setChecked(
                self.config_manager.get('ai_settings.auto_analyze', True))
            
            # Update status based on API key
            if api_key:
                self.ai_status_label.setText("🔑 API key configured")
                self.ai_status_label.setStyleSheet("""
                    color: #007aff;
                    font-weight: 600;
                    padding: 4px 8px;
                    background-color: #f0f8ff;
                    border-radius: 4px;
                """)
            else:
                self.ai_status_label.setText("Not configured")
                self.ai_status_label.setStyleSheet("""
                    color: #86868b;
                    font-style: italic;
                    padding: 4px 8px;
                    background-color: #f2f2f7;
                    border-radius: 4px;
                """)
                
        except Exception as e:
            print(f"Error loading AI settings: {e}")
