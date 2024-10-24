# gpt_analyzer.py
from openai import OpenAI
from typing import Optional, List, Dict, Any
from config import APIConfig
from template_manager import TemplateManager, TemplateConfig, TemplateCategory

class TranscriptionAnalyzer:
    """Enhanced analyzer using chat completions API with customizable templates"""

    def __init__(self, config: APIConfig, template_manager: Optional[TemplateManager] = None):
        self.client = OpenAI(api_key=config.api_key)
        self.config = config
        self.template_manager = template_manager or TemplateManager()
        self._initialize_default_templates()

    def _initialize_default_templates(self) -> None:
        """Initialize built-in analysis templates"""
        default_templates = {
            "summary": TemplateConfig(
                name="summary",
                category=TemplateCategory.ANALYSIS,
                system_prompt="You are generating a transcript summary. Focus on extracting and organizing the main points while maintaining clarity and brevity.",
                instruction="Create a concise summary of the main points discussed",
                temperature=0.3,
                description="Creates concise summaries of transcripts"
            ),
            "action_items": TemplateConfig(
                name="action_items",
                category=TemplateCategory.ANALYSIS,
                system_prompt="You are an action item extractor. Your primary focus is identifying and clearly presenting all tasks, commitments, and follow-up items.",
                instruction="Extract all action items, tasks, and commitments mentioned",
                focus_topics=["tasks", "deadlines", "assignments", "commitments"],
                temperature=0.1,
                output_format="""
# Action Items Identified
{{each item should include:
- What needs to be done
- Who is responsible (if mentioned)
- Due date/timeline (if mentioned)
- Any relevant context}}
                """,
                description="Extracts action items and tasks"
            ),
            "default": TemplateConfig(
                name="default",
                category=TemplateCategory.ANALYSIS,
                system_prompt="You are a transcript analyzer. Provide comprehensive analysis while maintaining clarity and structure.",
                instruction="Provide a detailed analysis of the transcription",
                temperature=0.7,
                description="Default comprehensive analysis"
            )
        }

        # Add default templates to template manager
        for template_name, template in default_templates.items():
            self.template_manager.templates[template_name] = template

    def analyze_transcription(self,
                              transcription: str,
                              template_name: str = "default",
                              custom_instructions: Optional[str] = None,
                              additional_context: Optional[str] = None,
                              override_focus_topics: Optional[List[str]] = None,
                              override_exclude_topics: Optional[List[str]] = None,
                              **kwargs) -> Optional[str]:
        """
        Analyzes transcription using managed templates
        """
        template = self.template_manager.get_template(template_name)
        if not template:
            print(f"Template '{template_name}' not found. Using default template.")
            template = self.template_manager.get_template("default")
            if not template:
                raise ValueError("Default template not found")

        # Create system prompt including both template and custom instructions
        system_prompt = template.system_prompt
        if template.instruction:
            system_prompt += f"\n\nPrimary task: {template.instruction}"

        if override_focus_topics:
            topics_str = ", ".join(override_focus_topics)
            system_prompt += f"\n\nPay particular attention to these topics: {topics_str}"

        if override_exclude_topics:
            topics_str = ", ".join(override_exclude_topics)
            system_prompt += f"\n\nMinimize discussion of these topics: {topics_str}"

        if custom_instructions:
            system_prompt += f"\n\nAdditional instructions: {custom_instructions}"

        if template.output_format:
            system_prompt += f"\n\nPlease format your response as follows: {template.output_format}"

        try:
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                }
            ]

            if additional_context:
                messages.append({
                    "role": "system",
                    "content": f"Additional context: {additional_context}"
                })

            messages.append({
                "role": "user",
                "content": transcription
            })

            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=template.temperature,
                max_tokens=kwargs.get('max_tokens', 1500)
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Error during GPT analysis: {e}")
            return None