from datetime import datetime
from pathlib import Path
import os

def generate_workflow_md(title, description, steps):
    """
    Generate Markdown content for a workflow file
    
    Args:
        title (str): Workflow title
        description (str): Workflow description
        steps (list): List of workflow steps
    
    Returns:
        tuple: (filename, markdown_content)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    filename = f"{title.replace(' ', '_').replace('/', '_').lower()}_workflow.md"
    
    content = [
        f"# {title}",
        "",
        f"**Description:** {description.strip()}",
        "",
        "**Steps:**"
    ]
    
    # Add steps as numbered list
    for i, step in enumerate(steps):
        if step.strip():
            content.append(f"{i+1}. {step.strip()}")
    
    content.extend([
        "",
        f"_Generated on {timestamp}_"
    ])
    
    return filename, "\n".join(content)

def save_workflow_file(filename, content, output_folder):
    """
    Save workflow content to a file
    
    Args:
        filename (str): Name of the file
        content (str): Markdown content
        output_folder (str): Output directory path
    
    Returns:
        str: Full path of the saved file
    """
    # Ensure the output folder exists
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    file_path = os.path.join(output_folder, filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return file_path
