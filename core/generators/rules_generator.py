from datetime import datetime
from pathlib import Path
import os

def generate_rule_md(title, category, activation, glob, description, rules_list):
    """
    Generate Markdown content for a rule file
    
    Args:
        title (str): Rule title
        category (str): Rule category
        activation (str): Activation mode
        glob (str): Glob pattern
        description (str): Rule description
        rules_list (list): List of rule items
    
    Returns:
        tuple: (filename, markdown_content)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    filename = f"{category.lower()}_{title.replace(' ', '_').replace('/', '_')}.md"
    
    content = [
        f"# {title}",
        "",
        f"**Category:** {category}",
        f"**Activation mode:** {activation}",
    ]
    
    if glob and glob.strip():
        content.append(f"**Glob pattern:** {glob}")
    
    content.extend([
        "",
        f"**Description:** {description.strip()}",
        "",
        "**Rules:**"
    ])
    
    # Add rules as bullet points
    for rule in rules_list:
        if rule.strip():
            content.append(f"- {rule.strip()}")
    
    content.extend([
        "",
        f"_Generated on {timestamp}_"
    ])
    
    return filename, "\n".join(content)

def save_rule_file(filename, content, output_folder):
    """
    Save rule content to a file
    
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
