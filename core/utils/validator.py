import re
import os

def validate_rule_input(title, category, description, rules_list):
    """
    Validate rule input data
    
    Args:
        title (str): Rule title
        category (str): Rule category
        description (str): Rule description
        rules_list (list): List of rules
    
    Returns:
        tuple: (is_valid, error_message)
    """
    errors = []
    
    if not title or not title.strip():
        errors.append("Rule title is required")
    
    if not category or not category.strip():
        errors.append("Rule category is required")
    
    if not description or not description.strip():
        errors.append("Rule description is required")
    
    if not rules_list or not any(rule.strip() for rule in rules_list):
        errors.append("At least one rule item is required")
    
    # Check for valid filename characters in title
    if title and not is_valid_filename_part(title):
        errors.append("Rule title contains invalid characters for filename")
    
    if errors:
        return False, "\n".join(errors)
    
    return True, ""

def validate_workflow_input(title, description, steps):
    """
    Validate workflow input data
    
    Args:
        title (str): Workflow title
        description (str): Workflow description
        steps (list): List of workflow steps
    
    Returns:
        tuple: (is_valid, error_message)
    """
    errors = []
    
    if not title or not title.strip():
        errors.append("Workflow title is required")
    
    if not description or not description.strip():
        errors.append("Workflow description is required")
    
    if not steps or not any(step.strip() for step in steps):
        errors.append("At least one workflow step is required")
    
    # Check for valid filename characters in title
    if title and not is_valid_filename_part(title):
        errors.append("Workflow title contains invalid characters for filename")
    
    if errors:
        return False, "\n".join(errors)
    
    return True, ""

def is_valid_filename_part(text):
    """
    Check if text can be safely used in a filename
    
    Args:
        text (str): Text to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    invalid_chars = r'[<>:"/\\|?*]'
    return not re.search(invalid_chars, text)

def validate_directory_path(path):
    """
    Validate if a directory path is accessible
    
    Args:
        path (str): Directory path
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not path:
        return False, "Path is required"
    
    try:
        # Check if path exists or can be created
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        
        # Check if path is writable
        if not os.access(path, os.W_OK):
            return False, "Directory is not writable"
        
        return True, ""
    
    except Exception as e:
        return False, f"Invalid directory path: {str(e)}"

def validate_glob_pattern(pattern):
    """
    Basic validation for glob patterns
    
    Args:
        pattern (str): Glob pattern
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not pattern:
        return True, ""  # Empty pattern is valid
    
    # Basic check for common glob pattern characters
    valid_chars = r'[a-zA-Z0-9_\-\.\*\?\[\]\/\\]'
    if not re.match(f'^{valid_chars}+$', pattern):
        return False, "Glob pattern contains invalid characters"
    
    return True, ""

def validate_api_key(api_key):
    """
    Basic validation for API key format
    
    Args:
        api_key (str): API key to validate
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not api_key or not api_key.strip():
        return False, "API key is required"
    
    # Basic length check (Gemini API keys are typically long)
    if len(api_key.strip()) < 20:
        return False, "API key appears to be too short"
    
    # Check for valid characters (alphanumeric, hyphens, underscores)
    if not re.match(r'^[a-zA-Z0-9_-]+$', api_key.strip()):
        return False, "API key contains invalid characters"
    
    return True, ""

def validate_project_idea(idea):
    """
    Validate project idea input
    
    Args:
        idea (str): Project idea text
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not idea or not idea.strip():
        return False, "Project idea is required"
    
    if len(idea.strip()) < 10:
        return False, "Project idea should be at least 10 characters long"
    
    if len(idea.strip()) > 2000:
        return False, "Project idea is too long (max 2000 characters)"
    
    return True, ""
