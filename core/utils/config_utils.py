import json
import os
from .file_utils import get_default_windsurf_paths

def load_config(config_path="config/settings.json"):
    """
    Load configuration from JSON file
    
    Args:
        config_path (str): Path to config file
    
    Returns:
        dict: Configuration dictionary
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return get_default_config()

def get_default_config():
    """
    Get default configuration
    
    Returns:
        dict: Default configuration
    """
    return {
        "default_paths": get_default_windsurf_paths(),
        "categories": [
            "UI",
            "Database", 
            "Logic",
            "Security",
            "Performance",
            "Testing",
            "Documentation"
        ],
        "activation_modes": [
            "Always On",
            "Manual",
            "Glob"
        ]
    }

def save_config(config, config_path="config/settings.json"):
    """
    Save configuration to JSON file
    
    Args:
        config (dict): Configuration to save
        config_path (str): Path to config file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False
