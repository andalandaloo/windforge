"""
Generators package - Contains all content generation modules
"""

from .rules_generator import generate_rule_md, save_rule_file
from .workflows_generator import generate_workflow_md, save_workflow_file

# Try to import AIGenerator, but make it optional
try:
    from .ai_generator import AIGenerator
    AI_AVAILABLE = True
except ImportError as e:
    print(f"Warning: AI Generator not available - {e}")
    AIGenerator = None
    AI_AVAILABLE = False

__all__ = [
    'generate_rule_md',
    'save_rule_file', 
    'generate_workflow_md',
    'save_workflow_file',
    'AIGenerator',
    'AI_AVAILABLE'
]
