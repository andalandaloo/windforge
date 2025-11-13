"""
AI Generator Module - Gemini Flash 2.5 Integration
Generates rules and workflows using Google's Gemini AI model
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Tuple
from pathlib import Path

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class AIGenerator:
    """AI-powered generator using Gemini Flash 2.5"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.model = None
        self.is_configured = False
        
        if GEMINI_AVAILABLE and self.api_key:
            self.configure_gemini()
    
    def configure_gemini(self):
        """Configure Gemini AI model"""
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            self.is_configured = True
        except Exception as e:
            print(f"Error configuring Gemini: {e}")
            self.is_configured = False
    
    def set_api_key(self, api_key: str) -> bool:
        """Set API key and reconfigure model"""
        self.api_key = api_key
        if GEMINI_AVAILABLE:
            self.configure_gemini()
            return self.is_configured
        return False
    
    def is_available(self) -> bool:
        """Check if AI generator is available and configured"""
        return GEMINI_AVAILABLE and self.is_configured
    
    def analyze_project(self, project_path: str) -> Dict[str, any]:
        """Analyze project structure and files"""
        project_info = {
            'path': project_path,
            'files': [],
            'structure': {},
            'languages': set(),
            'frameworks': set(),
            'file_count': 0
        }
        
        try:
            project_path = Path(project_path)
            if not project_path.exists():
                return project_info
            
            # Common file extensions and their languages
            language_map = {
                '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
                '.java': 'Java', '.cpp': 'C++', '.c': 'C', '.cs': 'C#',
                '.php': 'PHP', '.rb': 'Ruby', '.go': 'Go', '.rs': 'Rust',
                '.html': 'HTML', '.css': 'CSS', '.scss': 'SCSS',
                '.json': 'JSON', '.xml': 'XML', '.yaml': 'YAML', '.yml': 'YAML'
            }
            
            # Framework indicators
            framework_indicators = {
                'package.json': ['Node.js'],
                'requirements.txt': ['Python'],
                'Gemfile': ['Ruby'],
                'pom.xml': ['Java/Maven'],
                'build.gradle': ['Java/Gradle'],
                'Cargo.toml': ['Rust'],
                'go.mod': ['Go'],
                'composer.json': ['PHP']
            }
            
            for file_path in project_path.rglob('*'):
                if file_path.is_file() and not any(part.startswith('.') for part in file_path.parts):
                    relative_path = file_path.relative_to(project_path)
                    project_info['files'].append(str(relative_path))
                    project_info['file_count'] += 1
                    
                    # Detect language
                    suffix = file_path.suffix.lower()
                    if suffix in language_map:
                        project_info['languages'].add(language_map[suffix])
                    
                    # Detect frameworks
                    filename = file_path.name.lower()
                    if filename in framework_indicators:
                        project_info['frameworks'].update(framework_indicators[filename])
            
            project_info['languages'] = list(project_info['languages'])
            project_info['frameworks'] = list(project_info['frameworks'])
            
        except Exception as e:
            print(f"Error analyzing project: {e}")
        
        return project_info
    
    def generate_rules_prompt(self, project_idea: str, project_info: Dict) -> str:
        """Generate prompt for rules generation"""
        languages = ', '.join(project_info.get('languages', []))
        frameworks = ', '.join(project_info.get('frameworks', []))
        
        prompt = f"""
أنت خبير في تطوير البرمجيات وإنشاء قواعد التطوير. أريدك أن تولد مجموعة من القواعد (Rules) لمشروع برمجي.

معلومات المشروع:
- الفكرة: {project_idea}
- اللغات المستخدمة: {languages or 'غير محدد'}
- الأطر المستخدمة: {frameworks or 'غير محدد'}
- عدد الملفات: {project_info.get('file_count', 0)}

يرجى إنشاء قواعد تطوير شاملة تغطي:
1. قواعد الكود (Code Rules)
2. قواعد الأمان (Security Rules)
3. قواعد الأداء (Performance Rules)
4. قواعد الاختبار (Testing Rules)
5. قواعد التوثيق (Documentation Rules)

لكل قاعدة، يرجى تحديد:
- العنوان
- الفئة (UI/Database/Logic/Security/Performance/Testing/Documentation)
- وضع التفعيل (Always On/Manual/Glob)
- نمط الملفات (Glob pattern)
- الوصف
- القواعد التفصيلية

أريد الإجابة في تنسيق JSON كالتالي:
{{
  "rules": [
    {{
      "title": "عنوان القاعدة",
      "category": "الفئة",
      "activation": "وضع التفعيل",
      "glob": "نمط الملفات",
      "description": "وصف القاعدة",
      "rules": ["قاعدة 1", "قاعدة 2", "قاعدة 3"]
    }}
  ]
}}
"""
        return prompt.strip()
    
    def generate_workflows_prompt(self, project_idea: str, project_info: Dict) -> str:
        """Generate prompt for workflows generation"""
        languages = ', '.join(project_info.get('languages', []))
        frameworks = ', '.join(project_info.get('frameworks', []))
        
        prompt = f"""
أنت خبير في إدارة المشاريع البرمجية وسير العمل. أريدك أن تولد مجموعة من سير العمل (Workflows) لمشروع برمجي.

معلومات المشروع:
- الفكرة: {project_idea}
- اللغات المستخدمة: {languages or 'غير محدد'}
- الأطر المستخدمة: {frameworks or 'غير محدد'}
- عدد الملفات: {project_info.get('file_count', 0)}

يرجى إنشاء سير عمل شامل يغطي:
1. سير عمل التطوير (Development Workflow)
2. سير عمل الاختبار (Testing Workflow)
3. سير عمل النشر (Deployment Workflow)
4. سير عمل مراجعة الكود (Code Review Workflow)
5. سير عمل إدارة الأخطاء (Bug Management Workflow)

لكل سير عمل، يرجى تحديد:
- العنوان
- الوصف
- الخطوات التفصيلية

أريد الإجابة في تنسيق JSON كالتالي:
{{
  "workflows": [
    {{
      "title": "عنوان سير العمل",
      "description": "وصف سير العمل",
      "steps": ["خطوة 1", "خطوة 2", "خطوة 3"]
    }}
  ]
}}
"""
        return prompt.strip()
    
    async def generate_content_async(self, prompt: str) -> Optional[str]:
        """Generate content using Gemini AI (async)"""
        if not self.is_available():
            return None
        
        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating content: {e}")
            return None
    
    def generate_content(self, prompt: str) -> Optional[str]:
        """Generate content using Gemini AI (sync)"""
        if not self.is_available():
            return None
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating content: {e}")
            return None
    
    def parse_ai_response(self, response: str, content_type: str) -> List[Dict]:
        """Parse AI response and extract structured data"""
        try:
            # Try to find JSON in the response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response[start_idx:end_idx]
                data = json.loads(json_str)
                
                if content_type == 'rules' and 'rules' in data:
                    return data['rules']
                elif content_type == 'workflows' and 'workflows' in data:
                    return data['workflows']
        
        except json.JSONDecodeError:
            pass
        
        # Fallback: try to parse manually
        return self.manual_parse_response(response, content_type)
    
    def manual_parse_response(self, response: str, content_type: str) -> List[Dict]:
        """Manually parse AI response if JSON parsing fails"""
        items = []
        
        # This is a simplified parser - in a real implementation,
        # you might want to use more sophisticated parsing
        lines = response.split('\n')
        current_item = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith('Title:') or line.startswith('عنوان:'):
                if current_item:
                    items.append(current_item)
                current_item = {'title': line.split(':', 1)[1].strip()}
            elif line.startswith('Category:') or line.startswith('فئة:'):
                current_item['category'] = line.split(':', 1)[1].strip()
            elif line.startswith('Description:') or line.startswith('وصف:'):
                current_item['description'] = line.split(':', 1)[1].strip()
        
        if current_item:
            items.append(current_item)
        
        return items
    
    def generate_rules(self, project_idea: str, project_path: str) -> List[Dict]:
        """Generate rules for the project"""
        if not self.is_available():
            return []
        
        project_info = self.analyze_project(project_path)
        prompt = self.generate_rules_prompt(project_idea, project_info)
        
        response = self.generate_content(prompt)
        if response:
            return self.parse_ai_response(response, 'rules')
        
        return []
    
    def generate_workflows(self, project_idea: str, project_path: str) -> List[Dict]:
        """Generate workflows for the project"""
        if not self.is_available():
            return []
        
        project_info = self.analyze_project(project_path)
        prompt = self.generate_workflows_prompt(project_idea, project_info)
        
        response = self.generate_content(prompt)
        if response:
            return self.parse_ai_response(response, 'workflows')
        
        return []
    
    def get_status_message(self) -> str:
        """Get current status message"""
        if not GEMINI_AVAILABLE:
            return "Gemini library not installed. Run: pip install google-generativeai"
        elif not self.api_key:
            return "API key not configured. Please set GEMINI_API_KEY environment variable or configure in settings."
        elif not self.is_configured:
            return "Gemini model not configured properly. Please check your API key."
        else:
            return "AI Generator ready!"
