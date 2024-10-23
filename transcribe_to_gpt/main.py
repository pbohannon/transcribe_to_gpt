# main.py
from typing import Optional, List
import argparse
from config import get_config
from whisper_transcriber import WhisperTranscriber
from gpt_analyzer import TranscriptionAnalyzer


def main(
        audio_file_path: str,
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

        # Initialize services
        transcriber = WhisperTranscriber(config)
        analyzer = TranscriptionAnalyzer(config)

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
            "template": template
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

        gpt_response = analyzer.analyze_transcription_with_template(**analysis_params)

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
        description='Transcribe and analyze audio with custom instructions.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Basic usage:
    python main.py audio.mp3

  Use specific template:
    python main.py audio.mp3 --template action_items

  Add custom instructions:
    python main.py audio.mp3 --instruction "Focus on technical decisions"

  Specify focus topics:
    python main.py audio.mp3 --focus "budget" "timeline" "risks"

  Template with custom instruction:
    python main.py audio.mp3 --template summary --instruction "Highlight key decisions"

Available templates:
  - summary: Create a concise summary
  - action_items: Extract tasks and commitments
  - sentiment: Analyze tone and emotions
  - qa: Extract questions and answers
  - default: General analysis
        """
    )

    parser.add_argument('audio_file',
                        help='Path to the audio file')

    parser.add_argument('--template',
                        choices=['summary', 'action_items', 'sentiment', 'qa', 'default'],
                        default='default',
                        help='Analysis template to use')

    parser.add_argument('--instruction',
                        help='Custom instructions for the analysis')

    parser.add_argument('--focus',
                        nargs='+',
                        help='Topics to focus on')

    parser.add_argument('--exclude',
                        nargs='+',
                        help='Topics to exclude')

    parser.add_argument('--context',
                        help='Additional context for the analysis')

    parser.add_argument('--temperature',
                        type=float,
                        help='Temperature for GPT analysis (0.0 to 1.0)')

    args = parser.parse_args()

    main(
        audio_file_path=args.audio_file,
        template=args.template,
        instruction=args.instruction,
        focus_topics=args.focus,
        exclude_topics=args.exclude,
        context=args.context,
        temperature=args.temperature
    )