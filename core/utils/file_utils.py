import os
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

def get_file_extension(filename):
    """
    Get file extension from filename
    
    Args:
        filename (str): Filename
    
    Returns:
        str: File extension (without dot)
    """
    return Path(filename).suffix.lstrip('.')

def get_file_size(file_path):
    """
    Get file size in bytes
    
    Args:
        file_path (str): Path to file
    
    Returns:
        int: File size in bytes, -1 if file doesn't exist
    """
    try:
        return os.path.getsize(file_path)
    except (OSError, FileNotFoundError):
        return -1

def create_backup_filename(original_path):
    """
    Create backup filename by adding timestamp
    
    Args:
        original_path (str): Original file path
    
    Returns:
        str: Backup file path
    """
    from datetime import datetime
    
    path = Path(original_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{path.stem}_backup_{timestamp}{path.suffix}"
    
    return str(path.parent / backup_name)
