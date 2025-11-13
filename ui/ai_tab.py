"""
AI Tab Module - AI-powered generation interface
Provides UI for generating rules and workflows using AI
"""

import os
import json
from typing import List, Dict
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, 
    QTextEdit, QPushButton, QFileDialog, QMessageBox, QTextBrowser, 
    QLabel, QSplitter, QGroupBox, QProgressBar, QComboBox,
    QCheckBox, QSpinBox, QTabWidget
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon, QFont

from core.generators import AIGenerator, generate_rule_md, save_rule_file, generate_workflow_md, save_workflow_file

class AIGenerationWorker(QThread):
    """Worker thread for AI generation to prevent UI freezing"""
    
    progress_updated = pyqtSignal(str)
    rules_generated = pyqtSignal(list)
    workflows_generated = pyqtSignal(list)
    generation_finished = pyqtSignal(bool, str)
    
    def __init__(self, ai_generator: AIGenerator, project_idea: str, project_path: str, generate_rules: bool, generate_workflows: bool):
        super().__init__()
        self.ai_generator = ai_generator
        self.project_idea = project_idea
        self.project_path = project_path
        self.generate_rules = generate_rules
        self.generate_workflows = generate_workflows
    
    def run(self):
        """Run AI generation in background thread"""
        try:
            success = True
            message = "Generation completed successfully!"
            
            if self.generate_rules:
                self.progress_updated.emit("Analyzing project for rules generation...")
                rules = self.ai_generator.generate_rules(self.project_idea, self.project_path)
                self.rules_generated.emit(rules)
                self.progress_updated.emit(f"Generated {len(rules)} rules")
            
            if self.generate_workflows:
                self.progress_updated.emit("Analyzing project for workflow generation...")
                workflows = self.ai_generator.generate_workflows(self.project_idea, self.project_path)
                self.workflows_generated.emit(workflows)
                self.progress_updated.emit(f"Generated {len(workflows)} workflows")
            
        except Exception as e:
            success = False
            message = f"Generation failed: {str(e)}"
        
        self.generation_finished.emit(success, message)

class AITab(QWidget):
    """AI-powered generation tab"""
    
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.ai_generator = AIGenerator()
        self.generated_rules = []
        self.generated_workflows = []
        self.generation_worker = None
        
        self.init_ui()
        self.check_ai_status()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QHBoxLayout()
        
        # Left panel - Input and controls
        left_panel = self.create_input_panel()
        
        # Right panel - Results and preview
        right_panel = self.create_results_panel()
        
        # Add panels to splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 600])
        
        layout.addWidget(splitter)
        self.setLayout(layout)
    
    def create_input_panel(self):
        """Create input panel with project settings"""
        panel = QWidget()
        layout = QVBoxLayout()
        
        # AI Status group
        status_group = QGroupBox("AI Status")
        status_layout = QVBoxLayout()
        
        self.status_label = QLabel("Checking AI status...")
        self.status_label.setWordWrap(True)
        status_layout.addWidget(self.status_label)
        
        
        # Keep API key input hidden but accessible for loading saved keys
        self.api_key_input = QLineEdit()
        self.api_key_input.setVisible(False)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # Project Configuration group
        project_group = QGroupBox("Project Configuration")
        project_layout = QFormLayout()
        
        # Project idea
        self.project_idea = QTextEdit()
        self.project_idea.setMaximumHeight(100)
        self.project_idea.setPlaceholderText("Describe your project idea in detail...")
        project_layout.addRow("Project Idea:", self.project_idea)
        
        # Project path
        project_path_layout = QHBoxLayout()
        self.project_path = QLineEdit()
        self.project_path.setPlaceholderText("Select project folder...")
        self.project_path.setReadOnly(True)
        
        self.btn_browse_project = QPushButton("Browse")
        folder_icon_path = os.path.join("resources", "icons", "folder_icon.svg")
        if os.path.exists(folder_icon_path):
            self.btn_browse_project.setIcon(QIcon(folder_icon_path))
        self.btn_browse_project.clicked.connect(self.browse_project_folder)
        
        project_path_layout.addWidget(self.project_path)
        project_path_layout.addWidget(self.btn_browse_project)
        project_layout.addRow("Project Path:", project_path_layout)
        
        project_group.setLayout(project_layout)
        layout.addWidget(project_group)
        
        # Generation Options group
        options_group = QGroupBox("Generation Options")
        options_layout = QFormLayout()
        
        self.generate_rules_cb = QCheckBox("Generate Rules")
        self.generate_rules_cb.setChecked(True)
        options_layout.addRow("", self.generate_rules_cb)
        
        self.generate_workflows_cb = QCheckBox("Generate Workflows")
        self.generate_workflows_cb.setChecked(True)
        options_layout.addRow("", self.generate_workflows_cb)
        
        self.max_rules_spin = QSpinBox()
        self.max_rules_spin.setRange(1, 20)
        self.max_rules_spin.setValue(5)
        options_layout.addRow("Max Rules:", self.max_rules_spin)
        
        self.max_workflows_spin = QSpinBox()
        self.max_workflows_spin.setRange(1, 10)
        self.max_workflows_spin.setValue(3)
        options_layout.addRow("Max Workflows:", self.max_workflows_spin)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Output Settings group
        output_group = QGroupBox("Output Settings")
        output_layout = QFormLayout()
        
        # Rules output path
        rules_output_layout = QHBoxLayout()
        self.rules_output_path = QLineEdit()
        default_rules_path = self.config_manager.get('default_paths.rules', '.windsurf/rules')
        self.rules_output_path.setText(default_rules_path)
        
        self.btn_browse_rules_output = QPushButton("Browse")
        if os.path.exists(folder_icon_path):
            self.btn_browse_rules_output.setIcon(QIcon(folder_icon_path))
        self.btn_browse_rules_output.clicked.connect(self.browse_rules_output)
        
        rules_output_layout.addWidget(self.rules_output_path)
        rules_output_layout.addWidget(self.btn_browse_rules_output)
        output_layout.addRow("Rules Output:", rules_output_layout)
        
        # Workflows output path
        workflows_output_layout = QHBoxLayout()
        self.workflows_output_path = QLineEdit()
        default_workflows_path = self.config_manager.get('default_paths.workflows', '.windsurf/workflows')
        self.workflows_output_path.setText(default_workflows_path)
        
        self.btn_browse_workflows_output = QPushButton("Browse")
        if os.path.exists(folder_icon_path):
            self.btn_browse_workflows_output.setIcon(QIcon(folder_icon_path))
        self.btn_browse_workflows_output.clicked.connect(self.browse_workflows_output)
        
        workflows_output_layout.addWidget(self.workflows_output_path)
        workflows_output_layout.addWidget(self.btn_browse_workflows_output)
        output_layout.addRow("Workflows Output:", workflows_output_layout)
        
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)
        
        # Generation button
        self.btn_generate = QPushButton("🤖 Generate with AI")
        generate_icon_path = os.path.join("resources", "icons", "generate_button.svg")
        if os.path.exists(generate_icon_path):
            self.btn_generate.setIcon(QIcon(generate_icon_path))
        self.btn_generate.clicked.connect(self.start_generation)
        self.btn_generate.setEnabled(False)
        layout.addWidget(self.btn_generate)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Progress label
        self.progress_label = QLabel("")
        self.progress_label.setVisible(False)
        layout.addWidget(self.progress_label)
        
        layout.addStretch()
        panel.setLayout(layout)
        return panel
    
    def create_results_panel(self):
        """Create results panel with generated content"""
        panel = QWidget()
        layout = QVBoxLayout()
        
        # Results tabs
        self.results_tabs = QTabWidget()
        
        # Rules tab
        self.rules_results_tab = self.create_rules_results_tab()
        self.results_tabs.addTab(self.rules_results_tab, "Generated Rules")
        
        # Workflows tab
        self.workflows_results_tab = self.create_workflows_results_tab()
        self.results_tabs.addTab(self.workflows_results_tab, "Generated Workflows")
        
        layout.addWidget(self.results_tabs)
        panel.setLayout(layout)
        return panel
    
    def create_rules_results_tab(self):
        """Create rules results tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        self.btn_save_all_rules = QPushButton("Save All Rules")
        save_icon_path = os.path.join("resources", "icons", "save_icon.svg")
        if os.path.exists(save_icon_path):
            self.btn_save_all_rules.setIcon(QIcon(save_icon_path))
        self.btn_save_all_rules.clicked.connect(self.save_all_rules)
        self.btn_save_all_rules.setEnabled(False)
        
        self.btn_clear_rules = QPushButton("Clear")
        clear_icon_path = os.path.join("resources", "icons", "clear_icon.svg")
        if os.path.exists(clear_icon_path):
            self.btn_clear_rules.setIcon(QIcon(clear_icon_path))
        self.btn_clear_rules.clicked.connect(self.clear_rules_results)
        self.btn_clear_rules.setEnabled(False)
        
        toolbar.addWidget(self.btn_save_all_rules)
        toolbar.addWidget(self.btn_clear_rules)
        toolbar.addStretch()
        
        layout.addLayout(toolbar)
        
        # Results display
        self.rules_results = QTextBrowser()
        self.rules_results.setPlaceholderText("Generated rules will appear here...")
        layout.addWidget(self.rules_results)
        
        tab.setLayout(layout)
        return tab
    
    def create_workflows_results_tab(self):
        """Create workflows results tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        self.btn_save_all_workflows = QPushButton("Save All Workflows")
        save_icon_path = os.path.join("resources", "icons", "save_icon.svg")
        if os.path.exists(save_icon_path):
            self.btn_save_all_workflows.setIcon(QIcon(save_icon_path))
        self.btn_save_all_workflows.clicked.connect(self.save_all_workflows)
        self.btn_save_all_workflows.setEnabled(False)
        
        self.btn_clear_workflows = QPushButton("Clear")
        clear_icon_path = os.path.join("resources", "icons", "clear_icon.svg")
        if os.path.exists(clear_icon_path):
            self.btn_clear_workflows.setIcon(QIcon(clear_icon_path))
        self.btn_clear_workflows.clicked.connect(self.clear_workflows_results)
        self.btn_clear_workflows.setEnabled(False)
        
        toolbar.addWidget(self.btn_save_all_workflows)
        toolbar.addWidget(self.btn_clear_workflows)
        toolbar.addStretch()
        
        layout.addLayout(toolbar)
        
        # Results display
        self.workflows_results = QTextBrowser()
        self.workflows_results.setPlaceholderText("Generated workflows will appear here...")
        layout.addWidget(self.workflows_results)
        
        tab.setLayout(layout)
        return tab
    
    def check_ai_status(self):
        """Check AI generator status"""
        status_message = self.ai_generator.get_status_message()
        self.status_label.setText(status_message)
        
        # Change status label color based on status - Apple style
        if "✅" in status_message:
            self.status_label.setStyleSheet("""
                color: #30d158;
                font-weight: 600;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background-color: #f0fff4;
                padding: 8px 12px;
                border-radius: 8px;
                border: 1px solid #c6f6d5;
            """)
        elif "⚠️" in status_message:
            self.status_label.setStyleSheet("""
                color: #ff9500;
                font-weight: 600;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background-color: #fff8f0;
                padding: 8px 12px;
                border-radius: 8px;
                border: 1px solid #fed7aa;
            """)
        elif "❌" in status_message:
            self.status_label.setStyleSheet("""
                color: #ff3b30;
                font-weight: 600;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background-color: #fff5f5;
                padding: 8px 12px;
                border-radius: 8px;
                border: 1px solid #fecaca;
            """)
        else:
            self.status_label.setStyleSheet("""
                color: #1d1d1f;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                padding: 8px 12px;
                border-radius: 8px;
                background-color: #f2f2f7;
            """)
        
        # Enable/disable generate button based on status
        try:
            can_generate = (
                self.ai_generator.is_available() and
                bool(self.project_idea.toPlainText().strip()) and
                bool(self.project_path.text().strip()) and
                (self.generate_rules_cb.isChecked() or self.generate_workflows_cb.isChecked())
            )
            self.btn_generate.setEnabled(bool(can_generate))
        except Exception as e:
            print(f"Error updating generate button: {e}")
            self.btn_generate.setEnabled(False)
        
    
    def open_settings(self):
        """Open settings dialog"""
        try:
            # Get parent window to open settings
            parent_window = self.window()
            if hasattr(parent_window, 'open_settings'):
                parent_window.open_settings()
            else:
                QMessageBox.information(self, "Settings", 
                    "Please use Help → Settings from the main menu to configure AI settings.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not open settings: {e}")
    
    def set_api_key_from_settings(self, api_key):
        """Set API key from settings (called by main window)"""
        if not api_key:
            return False
            
        try:
            # Check if AI generator is available at all
            if not hasattr(self.ai_generator, 'set_api_key'):
                return False
            
            success = self.ai_generator.set_api_key(api_key)
            if success:
                self.check_ai_status()
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Error setting API key from settings: {e}")
            return False
    
    def browse_project_folder(self):
        """Browse for project folder"""
        folder = QFileDialog.getExistingDirectory(self, "Select Project Folder")
        if folder:
            self.project_path.setText(folder)
            try:
                self.check_ai_status()
            except Exception as e:
                print(f"Error checking AI status after folder selection: {e}")
    
    def browse_rules_output(self):
        """Browse for rules output folder"""
        folder = QFileDialog.getExistingDirectory(
            self, "Select Rules Output Folder", 
            self.rules_output_path.text()
        )
        if folder:
            self.rules_output_path.setText(folder)
    
    def browse_workflows_output(self):
        """Browse for workflows output folder"""
        folder = QFileDialog.getExistingDirectory(
            self, "Select Workflows Output Folder", 
            self.workflows_output_path.text()
        )
        if folder:
            self.workflows_output_path.setText(folder)
    
    def start_generation(self):
        """Start AI generation process"""
        if not self.ai_generator.is_available():
            QMessageBox.warning(self, "AI Not Available", self.ai_generator.get_status_message())
            return
        
        project_idea = self.project_idea.toPlainText().strip()
        project_path = self.project_path.text().strip()
        
        if not project_idea:
            QMessageBox.warning(self, "Missing Information", "Please enter a project idea.")
            return
        
        if not project_path:
            QMessageBox.warning(self, "Missing Information", "Please select a project folder.")
            return
        
        if not os.path.exists(project_path):
            QMessageBox.warning(self, "Invalid Path", "The selected project folder does not exist.")
            return
        
        generate_rules = self.generate_rules_cb.isChecked()
        generate_workflows = self.generate_workflows_cb.isChecked()
        
        if not generate_rules and not generate_workflows:
            QMessageBox.warning(self, "No Options Selected", "Please select at least one generation option.")
            return
        
        # Start generation in background thread
        self.generation_worker = AIGenerationWorker(
            self.ai_generator, project_idea, project_path, 
            generate_rules, generate_workflows
        )
        
        # Connect signals
        self.generation_worker.progress_updated.connect(self.update_progress)
        self.generation_worker.rules_generated.connect(self.display_rules)
        self.generation_worker.workflows_generated.connect(self.display_workflows)
        self.generation_worker.generation_finished.connect(self.generation_completed)
        
        # Update UI for generation state
        self.btn_generate.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.progress_label.setVisible(True)
        self.progress_label.setText("Starting AI generation...")
        
        # Start the worker
        self.generation_worker.start()
    
    def update_progress(self, message: str):
        """Update progress message"""
        self.progress_label.setText(message)
    
    def display_rules(self, rules: List[Dict]):
        """Display generated rules"""
        self.generated_rules = rules
        
        if not rules:
            self.rules_results.setText("No rules were generated.")
            return
        
        content = f"# Generated Rules ({len(rules)} rules)\n\n"
        
        for i, rule in enumerate(rules, 1):
            content += f"## Rule {i}: {rule.get('title', 'Untitled')}\n\n"
            content += f"**Category:** {rule.get('category', 'General')}\n"
            content += f"**Activation:** {rule.get('activation', 'Manual')}\n"
            
            if rule.get('glob'):
                content += f"**Glob Pattern:** {rule.get('glob')}\n"
            
            content += f"**Description:** {rule.get('description', 'No description')}\n\n"
            
            if rule.get('rules'):
                content += "**Rules:**\n"
                for rule_item in rule['rules']:
                    content += f"- {rule_item}\n"
            
            content += "\n---\n\n"
        
        self.rules_results.setText(content)
        self.btn_save_all_rules.setEnabled(True)
        self.btn_clear_rules.setEnabled(True)
    
    def display_workflows(self, workflows: List[Dict]):
        """Display generated workflows"""
        self.generated_workflows = workflows
        
        if not workflows:
            self.workflows_results.setText("No workflows were generated.")
            return
        
        content = f"# Generated Workflows ({len(workflows)} workflows)\n\n"
        
        for i, workflow in enumerate(workflows, 1):
            content += f"## Workflow {i}: {workflow.get('title', 'Untitled')}\n\n"
            content += f"**Description:** {workflow.get('description', 'No description')}\n\n"
            
            if workflow.get('steps'):
                content += "**Steps:**\n"
                for j, step in enumerate(workflow['steps'], 1):
                    content += f"{j}. {step}\n"
            
            content += "\n---\n\n"
        
        self.workflows_results.setText(content)
        self.btn_save_all_workflows.setEnabled(True)
        self.btn_clear_workflows.setEnabled(True)
    
    def generation_completed(self, success: bool, message: str):
        """Handle generation completion"""
        # Update UI
        self.btn_generate.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        
        # Show result message
        if success:
            QMessageBox.information(self, "Generation Complete", message)
        else:
            QMessageBox.critical(self, "Generation Failed", message)
        
        # Clean up worker
        if self.generation_worker:
            self.generation_worker.deleteLater()
            self.generation_worker = None
    
    def save_all_rules(self):
        """Save all generated rules"""
        if not self.generated_rules:
            QMessageBox.warning(self, "No Rules", "No rules to save.")
            return
        
        output_folder = self.rules_output_path.text()
        if not output_folder:
            QMessageBox.warning(self, "No Output Folder", "Please select an output folder for rules.")
            return
        
        saved_count = 0
        failed_count = 0
        
        for rule in self.generated_rules:
            try:
                filename, md_content = generate_rule_md(
                    rule.get('title', 'Untitled'),
                    rule.get('category', 'General'),
                    rule.get('activation', 'Manual'),
                    rule.get('glob', ''),
                    rule.get('description', ''),
                    rule.get('rules', [])
                )
                
                save_rule_file(filename, md_content, output_folder)
                saved_count += 1
                
            except Exception as e:
                print(f"Error saving rule: {e}")
                failed_count += 1
        
        message = f"Saved {saved_count} rules successfully."
        if failed_count > 0:
            message += f" {failed_count} rules failed to save."
        
        QMessageBox.information(self, "Save Complete", message)
    
    def save_all_workflows(self):
        """Save all generated workflows"""
        if not self.generated_workflows:
            QMessageBox.warning(self, "No Workflows", "No workflows to save.")
            return
        
        output_folder = self.workflows_output_path.text()
        if not output_folder:
            QMessageBox.warning(self, "No Output Folder", "Please select an output folder for workflows.")
            return
        
        saved_count = 0
        failed_count = 0
        
        for workflow in self.generated_workflows:
            try:
                filename, md_content = generate_workflow_md(
                    workflow.get('title', 'Untitled'),
                    workflow.get('description', ''),
                    workflow.get('steps', [])
                )
                
                save_workflow_file(filename, md_content, output_folder)
                saved_count += 1
                
            except Exception as e:
                print(f"Error saving workflow: {e}")
                failed_count += 1
        
        message = f"Saved {saved_count} workflows successfully."
        if failed_count > 0:
            message += f" {failed_count} workflows failed to save."
        
        QMessageBox.information(self, "Save Complete", message)
    
    def clear_rules_results(self):
        """Clear rules results"""
        self.rules_results.clear()
        self.generated_rules = []
        self.btn_save_all_rules.setEnabled(False)
        self.btn_clear_rules.setEnabled(False)
    
    def clear_workflows_results(self):
        """Clear workflows results"""
        self.workflows_results.clear()
        self.generated_workflows = []
        self.btn_save_all_workflows.setEnabled(False)
        self.btn_clear_workflows.setEnabled(False)
