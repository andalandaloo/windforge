import os
import json
from pathlib import Path

def ensure_directory_exists(directory_path):
    """
    Ensure that a directory exists, create it if it doesn't
    
    Args:
        directory_path (str): Path to the directory
    """
    Path(directory_path).mkdir(parents=True, exist_ok=True)

def get_default_windsurf_paths():
    """
    Get default paths for .windsurf/rules and .windsurf/workflows
    
    Returns:
        dict: Dictionary containing default paths
    """
    current_dir = os.getcwd()
    windsurf_dir = os.path.join(current_dir, ".windsurf")
    
    return {
        "rules": os.path.join(windsurf_dir, "rules"),
        "workflows": os.path.join(windsurf_dir, "workflows")
    }

def sanitize_filename(filename):
    """
    Sanitize filename by removing or replacing invalid characters
    
    Args:
        filename (str): Original filename
    
    Returns:
        str: Sanitized filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

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
