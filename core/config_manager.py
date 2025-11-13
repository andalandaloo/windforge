import json
import os
from pathlib import Path
from typing import Dict, Any, List

class ConfigManager:
    """
    Configuration manager for the Windsurf Generator application
    Handles loading, saving, and managing application settings
    """
    
    def __init__(self, config_path: str = "config/settings.json"):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from JSON file
        
        Returns:
            dict: Configuration dictionary
        """
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Create default config if file doesn't exist
                default_config = self.get_default_config()
                self.save_config(default_config)
                return default_config
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.get_default_config()
    
    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """
        Save configuration to JSON file
        
        Args:
            config (dict): Configuration to save (uses self.config if None)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if config is None:
                config = self.config
            
            # Ensure config directory exists
            Path(self.config_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get_default_config(self) -> Dict[str, Any]:
        """
        Get default configuration
        
        Returns:
            dict: Default configuration
        """
        return {
            "default_paths": {
                "rules": ".windsurf/rules",
                "workflows": ".windsurf/workflows"
            },
            "categories": [
                "UI",
                "Database",
                "Logic",
                "Security",
                "Performance",
                "Testing",
                "Documentation",
                "API",
                "Configuration",
                "Deployment",
                "Validation",
                "Error Handling",
                "Logging",
                "Authentication",
                "Authorization"
            ],
            "activation_modes": [
                "Always On",
                "Manual",
                "Glob",
                "Conditional"
            ],
            "ui_settings": {
                "window_width": 1200,
                "window_height": 800,
                "theme": "light",
                "font_size": 10,
                "auto_save_preview": True,
                "show_line_numbers": False,
                "word_wrap": True
            },
            "file_settings": {
                "auto_timestamp": True,
                "backup_files": False,
                "default_encoding": "utf-8",
                "line_ending": "auto"
            },
            "templates": {
                "rule_template": {
                    "header": "# {title}\n\n**Category:** {category}\n**Activation mode:** {activation}\n",
                    "glob_line": "**Glob pattern:** {glob}\n",
                    "description": "**Description:** {description}\n\n",
                    "rules_header": "**Rules:**\n",
                    "rule_item": "- {rule}\n",
                    "footer": "\n_Generated on {timestamp}_"
                },
                "workflow_template": {
                    "header": "# {title}\n\n**Description:** {description}\n\n",
                    "steps_header": "**Steps:**\n",
                    "step_item": "{number}. {step}\n",
                    "footer": "\n_Generated on {timestamp}_"
                }
            },
            "recent_files": [],
            "shortcuts": {
                "generate_rule": "Ctrl+R",
                "generate_workflow": "Ctrl+W",
                "copy_preview": "Ctrl+C",
                "clear_preview": "Ctrl+L",
                "browse_folder": "Ctrl+O"
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key (supports dot notation)
        
        Args:
            key (str): Configuration key (e.g., 'ui_settings.theme')
            default: Default value if key not found
        
        Returns:
            Any: Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> bool:
        """
        Set configuration value by key (supports dot notation)
        
        Args:
            key (str): Configuration key (e.g., 'ui_settings.theme')
            value: Value to set
        
        Returns:
            bool: True if successful, False otherwise
        """
        keys = key.split('.')
        config = self.config
        
        try:
            # Navigate to the parent of the target key
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]
            
            # Set the value
            config[keys[-1]] = value
            return True
        except Exception as e:
            print(f"Error setting config key '{key}': {e}")
            return False
    
    def add_recent_file(self, file_path: str, max_recent: int = 10):
        """
        Add file to recent files list
        
        Args:
            file_path (str): Path to the file
            max_recent (int): Maximum number of recent files to keep
        """
        recent = self.get('recent_files', [])
        
        # Remove if already exists
        if file_path in recent:
            recent.remove(file_path)
        
        # Add to beginning
        recent.insert(0, file_path)
        
        # Limit to max_recent
        recent = recent[:max_recent]
        
        self.set('recent_files', recent)
        self.save_config()
    
    def get_categories(self) -> List[str]:
        """Get list of available categories"""
        return self.get('categories', [])
    
    def add_category(self, category: str) -> bool:
        """
        Add new category
        
        Args:
            category (str): Category name
        
        Returns:
            bool: True if added, False if already exists
        """
        categories = self.get_categories()
        if category not in categories:
            categories.append(category)
            self.set('categories', categories)
            self.save_config()
            return True
        return False
    
    def remove_category(self, category: str) -> bool:
        """
        Remove category
        
        Args:
            category (str): Category name
        
        Returns:
            bool: True if removed, False if not found
        """
        categories = self.get_categories()
        if category in categories:
            categories.remove(category)
            self.set('categories', categories)
            self.save_config()
            return True
        return False
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.config = self.get_default_config()
        self.save_config()
    
    def export_config(self, export_path: str) -> bool:
        """
        Export configuration to file
        
        Args:
            export_path (str): Path to export file
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error exporting config: {e}")
            return False
    
    def import_config(self, import_path: str) -> bool:
        """
        Import configuration from file
        
        Args:
            import_path (str): Path to import file
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
            
            # Validate imported config has required keys
            default_config = self.get_default_config()
            for key in default_config:
                if key not in imported_config:
                    imported_config[key] = default_config[key]
            
            self.config = imported_config
            self.save_config()
            return True
        except Exception as e:
            print(f"Error importing config: {e}")
            return False
