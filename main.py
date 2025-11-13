import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
    QHBoxLayout, QFormLayout, QLineEdit, QTextEdit, QComboBox, 
    QPushButton, QFileDialog, QMessageBox, QTextBrowser, QLabel,
    QSplitter, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

# Import core modules
from core.generators import generate_rule_md, save_rule_file, generate_workflow_md, save_workflow_file, AI_AVAILABLE
from core.utils import validate_rule_input, validate_workflow_input, validate_directory_path
from core.utils import get_default_windsurf_paths, get_default_config
from core.config_manager import ConfigManager
# Import generator functions directly
# from core.generators.rules_generator import RulesGenerator  # Not needed - using functions from __init__.py
# from core.generators.workflows_generator import WorkflowsGenerator  # Not needed - using functions from __init__.py
from core.theme_loader import apply_apple_theme

# Import UI components
from ui.settings_dialog import SettingsDialog

# Import AI tab only if AI is available
if AI_AVAILABLE:
    from ui.ai_tab import AITab
else:
    AITab = None

class WindsurfGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.config = self.config_manager.config
        self.default_paths = self.config_manager.get('default_paths')
        self.init_ui()
        self.setup_menu()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("WindForge - AI-Powered Development Rules & Workflow Generator")
        # Get window size from config
        width = self.config_manager.get('ui_settings.window_width', 1200)
        height = self.config_manager.get('ui_settings.window_height', 800)
        self.setGeometry(100, 100, width, height)
        
        # Set application icon
        app_icon_path = os.path.join("resources", "icons", "app_icon.svg")
        if os.path.exists(app_icon_path):
            self.setWindowIcon(QIcon(app_icon_path))
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Create tabs
        self.rules_tab = self.create_rules_tab()
        self.workflow_tab = self.create_workflow_tab()
        
        # Create AI tab only if available
        if AI_AVAILABLE and AITab:
            self.ai_tab = AITab(self.config_manager)
            # Load saved API key
            self.load_saved_api_key()
        else:
            self.ai_tab = None
        
        # Add tabs to tab widget with icons
        rules_icon_path = os.path.join("resources", "icons", "rules_tab.svg")
        workflow_icon_path = os.path.join("resources", "icons", "workflow_tab.svg")
        ai_icon_path = os.path.join("resources", "icons", "ai_icon.svg")
        
        rules_icon = QIcon(rules_icon_path) if os.path.exists(rules_icon_path) else QIcon()
        workflow_icon = QIcon(workflow_icon_path) if os.path.exists(workflow_icon_path) else QIcon()
        ai_icon = QIcon(ai_icon_path) if os.path.exists(ai_icon_path) else QIcon()
        
        self.tab_widget.addTab(self.rules_tab, rules_icon, "Rules Generator")
        self.tab_widget.addTab(self.workflow_tab, workflow_icon, "Workflow Generator")
        
        # Add AI tab only if available
        if self.ai_tab:
            self.tab_widget.addTab(self.ai_tab, ai_icon, "AI Generator")
        else:
            # Show a placeholder message about AI not being available
            print("ℹ️  AI Generator tab not available - install google-generativeai to enable AI features")
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)
        central_widget.setLayout(main_layout)
        
        # Apply Apple-style theme from QSS file
        if not apply_apple_theme():
            print("⚠️  Could not load Apple theme, using default styling")
            # Fallback to basic styling if QSS file is not available
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f8f9fa;
                    color: #1d1d1f;
                }
                QPushButton {
                    background-color: #007aff;
                    color: #ffffff;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 14px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
            """)
    
    def setup_menu(self):
        """Setup application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        # Settings action
        settings_action = file_menu.addAction('Settings')
        settings_icon_path = os.path.join("resources", "icons", "settings_icon.svg")
        if os.path.exists(settings_icon_path):
            settings_action.setIcon(QIcon(settings_icon_path))
        settings_action.triggered.connect(self.open_settings)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = file_menu.addAction('Exit')
        exit_action.triggered.connect(self.close)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        # About action
        about_action = help_menu.addAction('About')
        help_icon_path = os.path.join("resources", "icons", "help_icon.svg")
        if os.path.exists(help_icon_path):
            about_action.setIcon(QIcon(help_icon_path))
        about_action.triggered.connect(self.show_about)
        
        # Icon showcase action
        showcase_action = help_menu.addAction('Icon Showcase')
        showcase_action.triggered.connect(self.show_icon_showcase)
    
    def create_rules_tab(self):
        """Create the rules generator tab"""
        tab = QWidget()
        layout = QHBoxLayout()
        
        # Left panel - Input form
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # Form group
        form_group = QGroupBox("Rule Configuration")
        form_layout = QFormLayout()
        
        # Rule title
        self.rule_title = QLineEdit()
        self.rule_title.setPlaceholderText("Enter rule title...")
        form_layout.addRow("Rule Title:", self.rule_title)
        
        # Rule category
        self.rule_category = QComboBox()
        self.rule_category.addItems(self.config_manager.get_categories())
        form_layout.addRow("Category:", self.rule_category)
        
        # Activation mode
        self.rule_activation = QComboBox()
        self.rule_activation.addItems(self.config_manager.get('activation_modes', []))
        form_layout.addRow("Activation Mode:", self.rule_activation)
        
        # Glob pattern
        self.rule_glob = QLineEdit()
        self.rule_glob.setPlaceholderText("e.g., **/*.py")
        form_layout.addRow("Glob Pattern:", self.rule_glob)
        
        # Description
        self.rule_description = QTextEdit()
        self.rule_description.setMaximumHeight(100)
        self.rule_description.setPlaceholderText("Enter rule description...")
        form_layout.addRow("Description:", self.rule_description)
        
        # Rules list
        self.rule_items = QTextEdit()
        self.rule_items.setPlaceholderText("Enter rules (one per line):\n- Rule 1\n- Rule 2\n- Rule 3")
        form_layout.addRow("Rules:", self.rule_items)
        
        form_group.setLayout(form_layout)
        left_layout.addWidget(form_group)
        
        # Output folder selection
        folder_group = QGroupBox("Output Settings")
        folder_layout = QHBoxLayout()
        
        self.rule_output_path = QLineEdit()
        self.rule_output_path.setText(self.default_paths.get('rules', '.windsurf/rules'))
        self.rule_output_path.setReadOnly(True)
        
        self.btn_browse_rules = QPushButton("Browse...")
        folder_icon_path = os.path.join("resources", "icons", "folder_icon.svg")
        if os.path.exists(folder_icon_path):
            self.btn_browse_rules.setIcon(QIcon(folder_icon_path))
        self.btn_browse_rules.clicked.connect(self.browse_rules_folder)
        
        folder_layout.addWidget(self.rule_output_path)
        folder_layout.addWidget(self.btn_browse_rules)
        folder_group.setLayout(folder_layout)
        left_layout.addWidget(folder_group)
        
        # Generate button
        self.btn_generate_rule = QPushButton("Generate Rule")
        generate_icon_path = os.path.join("resources", "icons", "generate_button.svg")
        if os.path.exists(generate_icon_path):
            self.btn_generate_rule.setIcon(QIcon(generate_icon_path))
        self.btn_generate_rule.clicked.connect(self.generate_rule)
        left_layout.addWidget(self.btn_generate_rule)
        
        left_panel.setLayout(left_layout)
        
        # Right panel - Preview
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        preview_group = QGroupBox("Markdown Preview")
        preview_layout = QVBoxLayout()
        
        # Preview toolbar
        preview_toolbar = QHBoxLayout()
        
        # Copy button
        self.btn_copy_rule = QPushButton("Copy")
        copy_icon_path = os.path.join("resources", "icons", "copy_icon.svg")
        if os.path.exists(copy_icon_path):
            self.btn_copy_rule.setIcon(QIcon(copy_icon_path))
        self.btn_copy_rule.clicked.connect(self.copy_rule_preview)
        self.btn_copy_rule.setEnabled(False)
        
        # Clear button
        self.btn_clear_rule = QPushButton("Clear")
        clear_icon_path = os.path.join("resources", "icons", "clear_icon.svg")
        if os.path.exists(clear_icon_path):
            self.btn_clear_rule.setIcon(QIcon(clear_icon_path))
        self.btn_clear_rule.clicked.connect(self.clear_rule_preview)
        self.btn_clear_rule.setEnabled(False)
        
        preview_toolbar.addWidget(self.btn_copy_rule)
        preview_toolbar.addWidget(self.btn_clear_rule)
        preview_toolbar.addStretch()
        
        preview_layout.addLayout(preview_toolbar)
        
        self.rule_preview = QTextBrowser()
        self.rule_preview.setPlaceholderText("Generated Markdown will appear here...")
        self.rule_preview.textChanged.connect(self.on_rule_preview_changed)
        preview_layout.addWidget(self.rule_preview)
        
        preview_group.setLayout(preview_layout)
        right_layout.addWidget(preview_group)
        right_panel.setLayout(right_layout)
        
        # Add panels to splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 600])
        
        layout.addWidget(splitter)
        tab.setLayout(layout)
        
        return tab
    
    def create_workflow_tab(self):
        """Create the workflow generator tab"""
        tab = QWidget()
        layout = QHBoxLayout()
        
        # Left panel - Input form
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # Form group
        form_group = QGroupBox("Workflow Configuration")
        form_layout = QFormLayout()
        
        # Workflow title
        self.workflow_title = QLineEdit()
        self.workflow_title.setPlaceholderText("Enter workflow title...")
        form_layout.addRow("Workflow Title:", self.workflow_title)
        
        # Description
        self.workflow_description = QTextEdit()
        self.workflow_description.setMaximumHeight(100)
        self.workflow_description.setPlaceholderText("Enter workflow description...")
        form_layout.addRow("Description:", self.workflow_description)
        
        # Steps
        self.workflow_steps = QTextEdit()
        self.workflow_steps.setPlaceholderText("Enter workflow steps (one per line):\nStep 1: Initialize project\nStep 2: Configure settings\nStep 3: Run tests")
        form_layout.addRow("Steps:", self.workflow_steps)
        
        form_group.setLayout(form_layout)
        left_layout.addWidget(form_group)
        
        # Output folder selection
        folder_group = QGroupBox("Output Settings")
        folder_layout = QHBoxLayout()
        
        self.workflow_output_path = QLineEdit()
        self.workflow_output_path.setText(self.default_paths.get('workflows', '.windsurf/workflows'))
        self.workflow_output_path.setReadOnly(True)
        
        self.btn_browse_workflows = QPushButton("Browse...")
        folder_icon_path = os.path.join("resources", "icons", "folder_icon.svg")
        if os.path.exists(folder_icon_path):
            self.btn_browse_workflows.setIcon(QIcon(folder_icon_path))
        self.btn_browse_workflows.clicked.connect(self.browse_workflows_folder)
        
        folder_layout.addWidget(self.workflow_output_path)
        folder_layout.addWidget(self.btn_browse_workflows)
        folder_group.setLayout(folder_layout)
        left_layout.addWidget(folder_group)
        
        # Generate button
        self.btn_generate_workflow = QPushButton("Generate Workflow")
        generate_icon_path = os.path.join("resources", "icons", "generate_button.svg")
        if os.path.exists(generate_icon_path):
            self.btn_generate_workflow.setIcon(QIcon(generate_icon_path))
        self.btn_generate_workflow.clicked.connect(self.generate_workflow)
        left_layout.addWidget(self.btn_generate_workflow)
        
        left_panel.setLayout(left_layout)
        
        # Right panel - Preview
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        preview_group = QGroupBox("Markdown Preview")
        preview_layout = QVBoxLayout()
        
        # Preview toolbar
        workflow_preview_toolbar = QHBoxLayout()
        
        # Copy button
        self.btn_copy_workflow = QPushButton("Copy")
        copy_icon_path = os.path.join("resources", "icons", "copy_icon.svg")
        if os.path.exists(copy_icon_path):
            self.btn_copy_workflow.setIcon(QIcon(copy_icon_path))
        self.btn_copy_workflow.clicked.connect(self.copy_workflow_preview)
        self.btn_copy_workflow.setEnabled(False)
        
        # Clear button
        self.btn_clear_workflow = QPushButton("Clear")
        clear_icon_path = os.path.join("resources", "icons", "clear_icon.svg")
        if os.path.exists(clear_icon_path):
            self.btn_clear_workflow.setIcon(QIcon(clear_icon_path))
        self.btn_clear_workflow.clicked.connect(self.clear_workflow_preview)
        self.btn_clear_workflow.setEnabled(False)
        
        workflow_preview_toolbar.addWidget(self.btn_copy_workflow)
        workflow_preview_toolbar.addWidget(self.btn_clear_workflow)
        workflow_preview_toolbar.addStretch()
        
        preview_layout.addLayout(workflow_preview_toolbar)
        
        self.workflow_preview = QTextBrowser()
        self.workflow_preview.setPlaceholderText("Generated Markdown will appear here...")
        self.workflow_preview.textChanged.connect(self.on_workflow_preview_changed)
        preview_layout.addWidget(self.workflow_preview)
        
        preview_group.setLayout(preview_layout)
        right_layout.addWidget(preview_group)
        right_panel.setLayout(right_layout)
        
        # Add panels to splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 600])
        
        layout.addWidget(splitter)
        tab.setLayout(layout)
        
        return tab
    
    def browse_rules_folder(self):
        """Browse for rules output folder"""
        folder = QFileDialog.getExistingDirectory(
            self, 
            "Select Rules Output Folder", 
            self.rule_output_path.text()
        )
        if folder:
            self.rule_output_path.setText(folder)
    
    def browse_workflows_folder(self):
        """Browse for workflows output folder"""
        folder = QFileDialog.getExistingDirectory(
            self, 
            "Select Workflows Output Folder", 
            self.workflow_output_path.text()
        )
        if folder:
            self.workflow_output_path.setText(folder)
    
    def generate_rule(self):
        """Generate rule markdown file"""
        try:
            # Get input values
            title = self.rule_title.text().strip()
            category = self.rule_category.currentText()
            activation = self.rule_activation.currentText()
            glob = self.rule_glob.text().strip()
            description = self.rule_description.toPlainText().strip()
            rules_list = [line.strip() for line in self.rule_items.toPlainText().splitlines()]
            output_folder = self.rule_output_path.text()
            
            # Validate input
            is_valid, error_msg = validate_rule_input(title, category, description, rules_list)
            if not is_valid:
                QMessageBox.warning(self, "Validation Error", error_msg)
                return
            
            # Validate output folder
            is_valid_path, path_error = validate_directory_path(output_folder)
            if not is_valid_path:
                QMessageBox.warning(self, "Path Error", path_error)
                return
            
            # Generate markdown
            filename, md_content = generate_rule_md(title, category, activation, glob, description, rules_list)
            
            # Update preview
            self.rule_preview.setText(md_content)
            
            # Save file
            file_path = save_rule_file(filename, md_content, output_folder)
            
            # Show success message
            QMessageBox.information(
                self, 
                "✅ Rule Generated Successfully", 
                f"Rule saved to:\n{file_path}"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate rule:\n{str(e)}")
    
    def generate_workflow(self):
        """Generate workflow markdown file"""
        try:
            # Get input values
            title = self.workflow_title.text().strip()
            description = self.workflow_description.toPlainText().strip()
            steps = [line.strip() for line in self.workflow_steps.toPlainText().splitlines()]
            output_folder = self.workflow_output_path.text()
            
            # Validate input
            is_valid, error_msg = validate_workflow_input(title, description, steps)
            if not is_valid:
                QMessageBox.warning(self, "Validation Error", error_msg)
                return
            
            # Validate output folder
            is_valid_path, path_error = validate_directory_path(output_folder)
            if not is_valid_path:
                QMessageBox.warning(self, "Path Error", path_error)
                return
            
            # Generate markdown
            filename, md_content = generate_workflow_md(title, description, steps)
            
            # Update preview
            self.workflow_preview.setText(md_content)
            
            # Save file
            file_path = save_workflow_file(filename, md_content, output_folder)
            
            # Show success message
            QMessageBox.information(
                self, 
                "✅ Workflow Generated Successfully", 
                f"Workflow saved to:\n{file_path}"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate workflow:\n{str(e)}")
    
    def copy_rule_preview(self):
        """Copy rule preview content to clipboard"""
        content = self.rule_preview.toPlainText()
        if content:
            clipboard = QApplication.clipboard()
            clipboard.setText(content)
            QMessageBox.information(self, "Copied", "Rule preview copied to clipboard!")
    
    def clear_rule_preview(self):
        """Clear rule preview content"""
        self.rule_preview.clear()
        self.btn_copy_rule.setEnabled(False)
        self.btn_clear_rule.setEnabled(False)
    
    def copy_workflow_preview(self):
        """Copy workflow preview content to clipboard"""
        content = self.workflow_preview.toPlainText()
        if content:
            clipboard = QApplication.clipboard()
            clipboard.setText(content)
            QMessageBox.information(self, "Copied", "Workflow preview copied to clipboard!")
    
    def clear_workflow_preview(self):
        """Clear workflow preview content"""
        self.workflow_preview.clear()
        self.btn_copy_workflow.setEnabled(False)
        self.btn_clear_workflow.setEnabled(False)
    
    def on_rule_preview_changed(self):
        """Enable/disable buttons based on rule preview content"""
        has_content = bool(self.rule_preview.toPlainText().strip())
        self.btn_copy_rule.setEnabled(has_content)
        self.btn_clear_rule.setEnabled(has_content)
    
    def on_workflow_preview_changed(self):
        """Enable/disable buttons based on workflow preview content"""
        has_content = bool(self.workflow_preview.toPlainText().strip())
        self.btn_copy_workflow.setEnabled(has_content)
        self.btn_clear_workflow.setEnabled(has_content)
    
    def open_settings(self):
        """Open settings dialog"""
        settings_dialog = SettingsDialog(self.config_manager, self)
        settings_dialog.settings_changed.connect(self.on_settings_changed)
        settings_dialog.exec()
    
    def on_settings_changed(self):
        """Handle settings changes"""
        # Reload config
        self.config = self.config_manager.config
        self.default_paths = self.config_manager.get('default_paths')
        
        # Update UI elements
        self.rule_output_path.setText(self.default_paths.get('rules', '.windsurf/rules'))
        self.workflow_output_path.setText(self.default_paths.get('workflows', '.windsurf/workflows'))
        
        # Update categories
        categories = self.config_manager.get_categories()
        current_rule_category = self.rule_category.currentText()
        self.rule_category.clear()
        self.rule_category.addItems(categories)
        
        # Restore selection if still available
        if current_rule_category in categories:
            self.rule_category.setCurrentText(current_rule_category)
        
        QMessageBox.information(self, "Settings Updated", "Settings have been applied successfully!")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
        <div style='font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: #1d1d1f; line-height: 1.6;'>
            <div style='text-align: center; margin-bottom: 24px;'>
                <h1 style='color: #007aff; font-size: 32px; font-weight: 700; margin: 0;'>🔥 WindForge</h1>
                <p style='color: #86868b; font-size: 16px; margin: 8px 0;'>The Ultimate AI-Powered Development Tool</p>
                <div style='background: linear-gradient(135deg, #007aff, #5856d6); color: white; padding: 6px 12px; border-radius: 16px; display: inline-block; font-size: 14px; font-weight: 600;'>
                    Version 2.0.0
                </div>
            </div>
            
            <div style='background-color: #f2f2f7; padding: 20px; border-radius: 12px; margin: 16px 0;'>
                <h3 style='color: #1d1d1f; font-size: 18px; font-weight: 600; margin: 0 0 12px 0;'>🚀 Core Features</h3>
                <ul style='margin: 0; padding-left: 20px; color: #1d1d1f;'>
                    <li style='margin: 6px 0;'>🧩 Smart Rules Generator with AI assistance</li>
                    <li style='margin: 6px 0;'>⚙️ Advanced Workflow Builder</li>
                    <li style='margin: 6px 0;'>🤖 Gemini Flash 2.5 AI Integration</li>
                    <li style='margin: 6px 0;'>🎨 Modern Apple-style UI with custom icons</li>
                    <li style='margin: 6px 0;'>📋 Live Markdown preview with copy/paste tools</li>
                    <li style='margin: 6px 0;'>💾 Comprehensive settings and configuration</li>
                </ul>
            </div>
            
            <div style='background-color: #e8f4fd; padding: 20px; border-radius: 12px; margin: 16px 0; border-left: 4px solid #007aff;'>
                <h3 style='color: #007aff; font-size: 18px; font-weight: 600; margin: 0 0 12px 0;'>🛠️ Technology Stack</h3>
                <p style='margin: 0; color: #1d1d1f;'>Built with <strong>PyQt6</strong>, <strong>Python 3.8+</strong>, and <strong>Google Gemini AI</strong></p>
                <p style='margin: 8px 0 0 0; color: #86868b; font-size: 14px;'>Designed with Apple's Human Interface Guidelines</p>
            </div>
            
            <div style='text-align: center; margin-top: 24px; padding-top: 16px; border-top: 1px solid #e5e5e7;'>
                <p style='color: #86868b; font-size: 14px; margin: 0;'>
                    © 2024 WindForge Team<br>
                    <em style='color: #007aff;'>Forging the future of development workflows</em>
                </p>
            </div>
        </div>
        """
        
        QMessageBox.about(self, "About WindForge", about_text)
    
    def show_icon_showcase(self):
        """Show icon showcase window"""
        try:
            import subprocess
            subprocess.Popen([sys.executable, "icon_showcase.py"])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not open icon showcase:\n{str(e)}")
    
    def load_saved_api_key(self):
        """Load saved API key from settings and configure AI"""
        if not self.ai_tab:
            return
        
        try:
            # Get saved API key
            api_key = self.config_manager.get('ai_settings.api_key', '')
            
            if api_key:
                # Set API key in AI tab
                self.ai_tab.api_key_input.setText(api_key)
                
                # Automatically configure AI with saved key
                success = self.ai_tab.set_api_key_from_settings(api_key)
                if success:
                    print("✅ Loaded saved API key successfully")
                else:
                    print("⚠️  Saved API key is invalid")
                    
        except Exception as e:
            print(f"Error loading saved API key: {e}")
    
    def on_settings_changed(self):
        """Handle settings changes"""
        # Reload API key if it was changed in settings
        if self.ai_tab:
            try:
                api_key = self.config_manager.get('ai_settings.api_key', '')
                current_key = self.ai_tab.api_key_input.text()
                
                # If API key changed, update it
                if api_key != current_key:
                    self.ai_tab.api_key_input.setText(api_key)
                    if api_key:
                        success = self.ai_tab.set_api_key_from_settings(api_key)
                        if success:
                            print("✅ Updated API key from settings")
                        else:
                            print("⚠️  New API key is invalid")
                    else:
                        print("ℹ️  API key removed from settings")
                        self.ai_tab.check_ai_status()
                        
            except Exception as e:
                print(f"Error updating API key from settings: {e}")

def main():
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("WindForge")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("WindForge Team")
    
    # Create and show main window
    window = WindsurfGeneratorApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
