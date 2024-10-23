# template_manager.py
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum
import json
from pathlib import Path


class TemplateCategory(Enum):
    ANALYSIS = "analysis"
    TECHNICAL = "technical"
    BUSINESS = "business"
    CUSTOM = "custom"


@dataclass
class TemplateConfig:
    name: str
    category: TemplateCategory
    system_prompt: str
    instruction: str
    temperature: float
    focus_topics: Optional[List[str]] = None
    output_format: Optional[str] = None
    description: Optional[str] = None
    version: str = "1.0"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "category": self.category.value,
            "system_prompt": self.system_prompt,
            "instruction": self.instruction,
            "temperature": self.temperature,
            "focus_topics": self.focus_topics,
            "output_format": self.output_format,
            "description": self.description,
            "version": self.version
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TemplateConfig':
        data['category'] = TemplateCategory(data['category'])
        return cls(**data)


class TemplateManager:
    """Manages analysis templates with persistent storage and validation"""

    def __init__(self, templates_dir: Optional[str] = None):
        self.templates_dir = Path(templates_dir) if templates_dir else Path.cwd() / 'templates'
        self.templates_dir.mkdir(exist_ok=True)
        self.templates: Dict[str, TemplateConfig] = {}
        self._load_default_templates()
        self._load_custom_templates()

    def _load_default_templates(self) -> None:
        """Initialize built-in templates"""
        default_templates = {
            "summary": TemplateConfig(
                name="summary",
                category=TemplateCategory.ANALYSIS,
                system_prompt="You are generating a transcript summary. Focus on extracting and organizing the main points while maintaining clarity and brevity.",
                instruction="Create a concise summary of the main points discussed",
                temperature=0.3,
                description="Creates concise summaries of transcripts"
            ),
            "technical_specs": TemplateConfig(
                name="technical_specs",
                category=TemplateCategory.TECHNICAL,
                system_prompt="You are a technical specification analyzer. Focus on technical details, requirements, and architectural decisions.",
                instruction="Extract technical specifications and architectural decisions",
                temperature=0.2,
                focus_topics=["requirements", "architecture", "technologies", "constraints"],
                output_format="""
# Technical Specifications
## Requirements
- List of functional requirements
- List of non-functional requirements

## Architecture
- Key architectural decisions
- System components
- Technical constraints

## Implementation Details
- Technologies mentioned
- Integration points
- Performance considerations
                """,
                description="Analyzes technical discussions and specifications"
            )
        }

        self.templates.update(default_templates)

    def _load_custom_templates(self) -> None:
        """Load custom templates from the templates directory"""
        for template_file in self.templates_dir.glob('*.json'):
            try:
                with open(template_file, 'r') as f:
                    template_data = json.load(f)
                    template = TemplateConfig.from_dict(template_data)
                    self.templates[template.name] = template
            except Exception as e:
                print(f"Error loading template {template_file}: {e}")

    def save_template(self, template: TemplateConfig) -> None:
        """Save a new template to persistent storage"""
        template_path = self.templates_dir / f"{template.name}.json"
        with open(template_path, 'w') as f:
            json.dump(template.to_dict(), f, indent=2)
        self.templates[template.name] = template

    def get_template(self, name: str) -> Optional[TemplateConfig]:
        """Retrieve a template by name"""
        return self.templates.get(name)

    def list_templates(self, category: Optional[TemplateCategory] = None) -> List[str]:
        """List available templates, optionally filtered by category"""
        if category:
            return [name for name, template in self.templates.items()
                    if template.category == category]
        return list(self.templates.keys())

    def validate_template(self, template: TemplateConfig) -> List[str]:
        """Validate a template configuration"""
        errors = []

        if not template.name or not template.name.isalnum():
            errors.append("Template name must be alphanumeric")

        if template.temperature < 0 or template.temperature > 1:
            errors.append("Temperature must be between 0 and 1")

        if not template.system_prompt or not template.instruction:
            errors.append("System prompt and instruction are required")

        return errors


# Modified TranscriptionAnalyzer class to use TemplateManager
class TranscriptionAnalyzer:
    """Enhanced analyzer using template manager for analysis configurations"""

    def __init__(self, config: 'APIConfig', template_manager: Optional[TemplateManager] = None):
        self.client = OpenAI(api_key=config.api_key)
        self.config = config
        self.template_manager = template_manager or TemplateManager()

    def analyze_transcription(self,
                              transcription: str,
                              template_name: str = "default",
                              custom_instructions: Optional[str] = None,
                              **kwargs) -> Optional[str]:
        """
        Analyze transcription using managed templates
        """
        template = self.template_manager.get_template(template_name)
        if not template:
            print(f"Template '{template_name}' not found. Using default template.")
            template = self.template_manager.get_template("default")
            if not template:
                raise ValueError("Default template not found")

        try:
            messages = [
                {
                    "role": "system",
                    "content": template.system_prompt
                }
            ]

            if custom_instructions:
                messages.append({
                    "role": "system",
                    "content": f"Additional instructions: {custom_instructions}"
                })

            messages.append({
                "role": "user",
                "content": f"The audio transcription is: {transcription}"
            })

            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=template.temperature,
                max_tokens=kwargs.get('max_tokens', 1500)
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Error during analysis: {e}")
            return None


# Example usage in main.py
def main():
    config = get_config()
    template_manager = TemplateManager()
    analyzer = TranscriptionAnalyzer(config, template_manager)

    # List available templates
    print("Available templates:")
    for category in TemplateCategory:
        templates = template_manager.list_templates(category)
        if templates:
            print(f"\n{category.value.title()} Templates:")
            for template_name in templates:
                template = template_manager.get_template(template_name)
                print(f"- {template_name}: {template.description}")

    # Create and save a custom template
    custom_template = TemplateConfig(
        name="meeting_minutes",
        category=TemplateCategory.BUSINESS,
        system_prompt="You are a meeting minutes generator...",
        instruction="Generate structured meeting minutes...",
        temperature=0.4,
        description="Generates formatted meeting minutes"
    )

    template_manager.save_template(custom_template)