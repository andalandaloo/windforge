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
        self.setWindowTitle("Settings - Windsurf Generator")
        self.setModal(True)
        self.resize(600, 500)
        
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
        self.categories_tab = self.create_categories_tab()
        self.ui_tab = self.create_ui_tab()
        self.templates_tab = self.create_templates_tab()
        
        # Add tabs
        self.tab_widget.addTab(self.general_tab, "General")
        self.tab_widget.addTab(self.paths_tab, "Paths")
        self.tab_widget.addTab(self.categories_tab, "Categories")
        self.tab_widget.addTab(self.ui_tab, "Interface")
        self.tab_widget.addTab(self.templates_tab, "Templates")
        
        layout.addWidget(self.tab_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.btn_reset = QPushButton("Reset to Defaults")
        self.btn_reset.clicked.connect(self.reset_to_defaults)
        
        self.btn_export = QPushButton("Export Settings")
        export_icon_path = os.path.join("resources", "icons", "export_icon.svg")
        if os.path.exists(export_icon_path):
            self.btn_export.setIcon(QIcon(export_icon_path))
        self.btn_export.clicked.connect(self.export_settings)
        
        self.btn_import = QPushButton("Import Settings")
        import_icon_path = os.path.join("resources", "icons", "import_icon.svg")
        if os.path.exists(import_icon_path):
            self.btn_import.setIcon(QIcon(import_icon_path))
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
        
        # Save configuration
        self.config_manager.save_config()
        
        # Emit signal that settings changed
        self.settings_changed.emit()
        
        self.accept()
