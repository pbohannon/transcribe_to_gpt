# main.py
from typing import Optional, List
import argparse
from config import get_config
from whisper_transcriber import WhisperTranscriber
from gpt_analyzer import TranscriptionAnalyzer
from template_manager import TemplateManager, TemplateCategory, TemplateConfig


def handle_template_management(template_manager: TemplateManager, args) -> None:
    """Handle template listing and management operations"""
    if args.list_templates:
        print("\nAvailable Templates:")
        for category in TemplateCategory:
            templates = template_manager.list_templates(category)
            if templates:
                print(f"\n{category.value.title()} Templates:")
                for template_name in templates:
                    template = template_manager.get_template(template_name)
                    if template and template.description:
                        print(f"- {template_name}: {template.description}")
                    else:
                        print(f"- {template_name}")
        return True

    if args.create_template:
        try:
            template = TemplateConfig(
                name=args.create_template,
                category=TemplateCategory(args.template_category),
                system_prompt=args.system_prompt,
                instruction=args.instruction,
                temperature=args.temperature,
                description=args.description
            )
            errors = template_manager.validate_template(template)
            if errors:
                print("\nTemplate validation errors:")
                for error in errors:
                    print(f"- {error}")
                return True

            template_manager.save_template(template)
            print(f"\nSuccessfully created template: {args.create_template}")
            return True
        except Exception as e:
            print(f"\nError creating template: {e}")
            return True

    return False


def main(
        audio_file_path: Optional[str] = None,
        template: str = "default",
        instruction: Optional[str] = None,
        focus_topics: Optional[List[str]] = None,
        exclude_topics: Optional[List[str]] = None,
        context: Optional[str] = None,
        temperature: Optional[float] = None,
) -> None:
    """
    Main function to orchestrate transcription and analysis
    """
    try:
        # Get configuration
        config = get_config()

        # Initialize template manager
        template_manager = TemplateManager()

        # Initialize services
        transcriber = WhisperTranscriber(config)
        analyzer = TranscriptionAnalyzer(config, template_manager)

        if not audio_file_path:
            return

        # Step 1: Transcribe audio
        print(f"Transcribing audio: {audio_file_path}")
        transcription = transcriber.transcribe_audio(audio_file_path)

        if not transcription:
            print("Failed to transcribe audio.")
            return

        print("Transcription complete!")

        # Step 2: Analyze transcription
        print(f"Analyzing transcription using '{template}' template...")

        # Prepare analysis parameters
        analysis_params = {
            "transcription": transcription,
            "template_name": template
        }

        # Add optional parameters if provided
        if instruction:
            analysis_params["custom_instructions"] = instruction
        if focus_topics:
            analysis_params["override_focus_topics"] = focus_topics
        if exclude_topics:
            analysis_params["override_exclude_topics"] = exclude_topics
        if context:
            analysis_params["additional_context"] = context
        if temperature is not None:
            analysis_params["temperature"] = temperature

        gpt_response = analyzer.analyze_transcription(**analysis_params)

        if not gpt_response:
            print("Failed to get analysis response.")
            return

        print("\nAnalysis Results:")
        print("=" * 50)
        print(gpt_response)
        print("=" * 50)

    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Transcribe and analyze audio with custom templates.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Template management arguments
    template_group = parser.add_argument_group('Template Management')
    template_group.add_argument('--list-templates',
                                action='store_true',
                                help='List available templates')

    template_group.add_argument('--create-template',
                                metavar='NAME',
                                help='Create a new template')

    template_group.add_argument('--template-category',
                                choices=[cat.value for cat in TemplateCategory],
                                help='Category for new template')

    template_group.add_argument('--system-prompt',
                                help='System prompt for new template')

    template_group.add_argument('--instruction',
                                help='Instruction for new template')

    template_group.add_argument('--temperature',
                                type=float,
                                help='Temperature for new template (0.0 to 1.0)')

    template_group.add_argument('--description',
                                help='Description for new template')

    # Analysis arguments
    analysis_group = parser.add_argument_group('Analysis')
    analysis_group.add_argument('audio_file',
                                nargs='?',
                                help='Path to the audio file')

    analysis_group.add_argument('--template',
                                help='Analysis template to use')

    analysis_group.add_argument('--focus',
                                nargs='+',
                                help='Topics to focus on')

    analysis_group.add_argument('--exclude',
                                nargs='+',
                                help='Topics to exclude')

    analysis_group.add_argument('--context',
                                help='Additional context for the analysis')

    args = parser.parse_args()

    # Handle template management operations first
    template_manager = TemplateManager()
    if handle_template_management(template_manager, args):
        exit(0)

    if not args.audio_file:
        parser.print_help()
        exit(1)

    main(
        audio_file_path=args.audio_file,
        template=args.template,
        instruction=args.instruction,
        focus_topics=args.focus,
        exclude_topics=args.exclude,
        context=args.context,
        temperature=args.temperature
    )