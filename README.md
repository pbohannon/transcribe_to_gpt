# Audio Transcription & Analysis System

A powerful system for transcribing audio files, analyzing transcripts, and generating creative interpretations of the content. Combines OpenAI's Whisper for transcription with GPT models for analysis, featuring customizable templates and musical transformations.

## Table of Contents
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Templates](#templates)
- [Advanced Features](#advanced-features)
- [Musical Summaries](#musical-summaries)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your OpenAI API key

# Basic usage
python main.py your_audio.mp3

# Generate musical summary
python main.py your_audio.mp3 --musical-style hiphop
```

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd audio-analysis-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment:
```bash
cp .env.example .env
# Edit .env and add:
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4  # Optional, defaults to gpt-4o
```

## Basic Usage

### Simple Transcription
```bash
python main.py path/to/your/audio.mp3
```

### With Analysis Template
```bash
python main.py path/to/your/audio.mp3 --template summary
```

### Adding Context
```bash
python main.py path/to/your/audio.mp3 --template summary \
    --context "Quarterly planning meeting" \
    --focus objectives deadlines
```

## Templates

### Built-in Templates
- **summary**: Concise summary of key points
- **technical_specs**: Technical analysis and specifications

### Musical Templates
- **hiphop_summary**: Hip-hop style interpretation
- **country_summary**: Country music style interpretation
- **ballad_summary**: 80s power ballad style interpretation

### Listing Templates
```bash
python main.py --list-templates
```

## Advanced Features

### Custom Instructions
```bash
python main.py meeting.mp3 --template summary \
    --instruction "Focus on action items and deadlines" \
    --focus decisions deadlines \
    --exclude small-talk
```

### Template Creation
```bash
python main.py --create-template my_template \
    --template-category custom \
    --system-prompt "You are analyzing..." \
    --instruction "Analyze the following..." \
    --temperature 0.7 \
    --description "My custom analysis template"
```

### Template Directory Structure
```
templates/
├── README.md
├── base/
│   └── musical_summary_base.json
├── analysis/
│   ├── summary.json
│   └── technical_specs.json
├── musical/
│   ├── hiphop_summary.json
│   ├── country_summary.json
│   └── ballad_summary.json
└── custom/
    └── your_custom_templates.json
```

## Musical Summaries

Transform your transcripts into various musical styles while maintaining information integrity.

### Basic Musical Summary
```bash
python main.py meeting.mp3 --musical-style hiphop
```

### With Original Summary
```bash
python main.py meeting.mp3 --musical-style country --include-original
```

### Available Styles
- Hip-hop: Complex rhyme schemes and wordplay
- Country: Narrative-driven storytelling
- Power Ballad: 80s-style emotional interpretation

## Customization

### Adding Focus Topics
```bash
python main.py meeting.mp3 --template summary \
    --focus architecture implementation timeline
```

### Modifying Temperature
```bash
python main.py meeting.mp3 --template summary --temperature 0.8
```

### Combining Features
```bash
python main.py meeting.mp3 \
    --template technical_specs \
    --instruction "Focus on architecture decisions" \
    --focus design patterns scalability \
    --context "System design review" \
    --temperature 0.4
```

## Use Cases

### Executive Summary
```bash
python main.py board_meeting.mp3 --template summary \
    --instruction "Create an executive summary" \
    --focus strategy finance metrics
```

### Technical Documentation
```bash
python main.py tech_review.mp3 --template technical_specs \
    --focus architecture security performance
```

### Creative Presentation
```bash
python main.py project_update.mp3 --musical-style hiphop \
    --focus achievements milestones \
    --context "Successful project completion"
```

## Troubleshooting

### Common Issues

1. **API Key Error**
   ```
   Error: OPENAI_API_KEY environment variable is required
   ```
   Solution: Check your .env file configuration

2. **Template Not Found**
   ```
   Template 'xyz' not found. Using default template.
   ```
   Solution: Check template name with --list-templates

3. **Transcription Failed**
   ```
   Error during transcription
   ```
   Solution: Verify audio file format and accessibility

### Best Practices

1. **Audio Quality**
   - Use clear audio recordings
   - Minimize background noise
   - Support common formats (mp3, wav, m4a)

2. **Template Selection**
   - Use appropriate templates for content type
   - Consider audience when choosing musical styles
   - Match temperature to desired creativity level

3. **System Resources**
   - Monitor API usage
   - Consider file size limitations
   - Check available disk space for templates

## Contributing

1. Fork the repository
2. Create your feature branch
3. Add your templates to appropriate directories
4. Submit a pull request

## License

[Your License Here]

## Acknowledgments

- OpenAI for Whisper and GPT APIs
- Contributors and template creators
- [Other acknowledgments]

Would you like me to expand any section or add more specific examples for certain use cases?