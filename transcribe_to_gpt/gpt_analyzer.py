# gpt_analyzer.py
from openai import OpenAI
from typing import Optional, List, Dict, Any
from config import APIConfig


class TranscriptionAnalyzer:
    """Enhanced analyzer using chat completions API with customizable templates"""

    def __init__(self, config: APIConfig):
        self.client = OpenAI(api_key=config.api_key)
        self.config = config
        self._initialize_templates()

    def _initialize_templates(self) -> None:
        """Initialize built-in analysis templates"""
        self.templates = {
            "summary": {
                "system_prompt": "You are generating a transcript summary. Focus on extracting and organizing the main points while maintaining clarity and brevity.",
                "instruction": "Create a concise summary of the main points discussed",
                "temperature": 0.3
            },
            "action_items": {
                "system_prompt": "You are an action item extractor. Your primary focus is identifying and clearly presenting all tasks, commitments, and follow-up items.",
                "instruction": "Extract all action items, tasks, and commitments mentioned",
                "focus_topics": ["tasks", "deadlines", "assignments", "commitments"],
                "temperature": 0.1,
                "output_format": """
# Action Items Identified
{{each item should include:
- What needs to be done
- Who is responsible (if mentioned)
- Due date/timeline (if mentioned)
- Any relevant context}}
                """
            },
            "sentiment": {
                "system_prompt": "You are a sentiment and tone analyzer. Focus on understanding and explaining the emotional undertones and attitudes expressed.",
                "instruction": "Analyze the overall tone and sentiment of the discussion",
                "focus_topics": ["emotions", "attitudes", "reactions"],
                "temperature": 0.4
            },
            "qa": {
                "system_prompt": "You are a Q&A extractor. Your role is to identify and pair questions with their corresponding answers.",
                "instruction": "Extract questions asked and their answers if provided",
                "focus_topics": ["questions", "answers", "clarifications"],
                "temperature": 0.2
            },
            "default": {
                "system_prompt": "You are a transcript analyzer. Provide comprehensive analysis while maintaining clarity and structure.",
                "instruction": "Provide a detailed analysis of the transcription",
                "temperature": 0.7
            }
        }

    def create_system_prompt(self,
                             base_prompt: str,
                             instruction: Optional[str] = None,
                             focus_topics: Optional[List[str]] = None,
                             exclude_topics: Optional[List[str]] = None,
                             custom_instructions: Optional[str] = None,
                             output_format: Optional[str] = None) -> str:
        """
        Creates the system message with both template and custom instructions.

        Args:
            base_prompt: The template's base system prompt
            instruction: Primary analysis instruction
            focus_topics: Topics to focus on
            exclude_topics: Topics to exclude
            custom_instructions: Additional custom instructions
            output_format: Specific output format requirements
        """
        system_parts = [base_prompt]

        if instruction:
            system_parts.append(f"Primary task: {instruction}")

        if focus_topics:
            topics_str = ", ".join(focus_topics)
            system_parts.append(f"Pay particular attention to these topics: {topics_str}")

        if exclude_topics:
            topics_str = ", ".join(exclude_topics)
            system_parts.append(f"Minimize discussion of these topics: {topics_str}")

        if custom_instructions:
            system_parts.append(f"Additional instructions: {custom_instructions}")

        if output_format:
            system_parts.append(f"Please format your response as follows: {output_format}")

        system_parts.append("Respond in Markdown format.")

        return " ".join(system_parts)

    def analyze_transcription_with_template(self,
                                            transcription: str,
                                            template: str = "default",
                                            custom_instructions: Optional[str] = None,
                                            additional_context: Optional[str] = None,
                                            override_focus_topics: Optional[List[str]] = None,
                                            override_exclude_topics: Optional[List[str]] = None,
                                            **kwargs) -> Optional[str]:
        """
        Analyzes transcription using predefined templates with custom modifications.

        Args:
            transcription: The text to analyze
            template: Template name ("summary", "action_items", "sentiment", etc.)
            custom_instructions: Additional instructions to modify/enhance the template
            additional_context: Any relevant context about the transcription
            override_focus_topics: Replace template's default focus topics
            override_exclude_topics: Add topics to exclude
            **kwargs: Additional template-specific parameters to override
        """
        # Get template configuration
        template_config = self.templates.get(template, self.templates["default"]).copy()

        # Update template config with any overrides
        template_config.update(kwargs)

        # Handle focus topics
        focus_topics = override_focus_topics if override_focus_topics is not None else template_config.get(
            'focus_topics')

        # Create system prompt including both template and custom instructions
        system_prompt = self.create_system_prompt(
            base_prompt=template_config['system_prompt'],
            instruction=template_config.get('instruction'),
            focus_topics=focus_topics,
            exclude_topics=override_exclude_topics,
            custom_instructions=custom_instructions,
            output_format=template_config.get('output_format')
        )

        try:
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                }
            ]

            # Add context if provided
            if additional_context:
                messages.append({
                    "role": "system",
                    "content": f"Additional context: {additional_context}"
                })

            # Add the transcription
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"The audio transcription is: {transcription}"
                    }
                ]
            })

            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=template_config.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 1500)
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Error during GPT analysis: {e}")
            return None