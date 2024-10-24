# Audio Analysis System - Project Structure

## Directory Layout
```
transcribe_to_gpt/
├── .env                    # Environment configuration (API keys)
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
│
├── main.py               # Main application entry point
├── config.py             # Configuration management
├── whisper_transcriber.py # Audio transcription handler
├── gpt_analyzer.py       # GPT analysis implementation
├── template_manager.py   # Template management system
├── musical_templates.py  # Musical template implementations
│
└── templates/            # Template storage directory
    ├── README.md        # Template documentation
    ├── base/            # Base template definitions
    │   └── musical_summary_base.json
    ├── analysis/        # Analysis templates
    │   ├── summary.json
    │   └── technical_specs.json
    ├── musical/         # Musical style templates
    │   ├── hiphop_summary.json
    │   ├── country_summary.json
    │   └── ballad_summary.json
    └── custom/          # User-created templates
```

## Core Files Description

### Application Core
- **main.py**
  - Entry point for the application
  - Handles command-line interface
  - Orchestrates the analysis workflow
  - Manages musical feature integration

- **config.py**
  - Environment configuration management
  - API key handling
  - Configuration validation
  - Settings singleton implementation

- **whisper_transcriber.py**
  - OpenAI Whisper API integration
  - Audio file handling
  - Transcription processing
  - Error handling for audio operations

- **gpt_analyzer.py**
  - GPT integration for analysis
  - Template processing
  - Analysis customization
  - Response formatting

### Template System
- **template_manager.py**
  - Template CRUD operations
  - Template validation
  - Category management
  - Template storage handling

- **musical_templates.py**
  - Musical template definitions
  - Genre-specific configurations
  - Template installation logic
  - Musical feature integration

### Template Directory
- **templates/README.md**
  - Template format documentation
  - Usage guidelines
  - Custom template creation guide

- **templates/base/**
  - Foundation templates
  - Shared template characteristics
  - Base configurations

- **templates/analysis/**
  - Standard analysis templates
  - Technical analysis configurations
  - Summary templates

- **templates/musical/**
  - Genre-specific templates
  - Musical style configurations
  - Performance notes formats

- **templates/custom/**
  - User-created templates
  - Custom configurations
  - Local modifications

## Module Relationships

1. **Configuration Flow**
   ```
   .env → config.py → [all other modules]
   ```

2. **Analysis Pipeline**
   ```
   main.py → whisper_transcriber.py → gpt_analyzer.py
   ```

3. **Template System**
   ```
   template_manager.py ← [musical_templates.py, gpt_analyzer.py]
   ```

4. **Template Storage**
   ```
   templates/ ← [template_manager.py, musical_templates.py]
   ```

## Key Features by Module

### Main Application (main.py)
- Command-line interface
- Workflow orchestration
- Feature coordination
- Error handling
- Output formatting

### Transcription (whisper_transcriber.py)
- Audio file processing
- Whisper API integration
- Transcription management
- Error handling

### Analysis (gpt_analyzer.py)
- GPT integration
- Template processing
- Analysis customization
- Response formatting

### Template Management (template_manager.py)
- Template CRUD
- Validation
- Storage management
- Category handling

### Musical Features (musical_templates.py)
- Genre templates
- Style configurations
- Template installation
- Musical processing

## Configuration Requirements

### Environment (.env)
```
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4  # Optional
```

### Dependencies (requirements.txt)
```
openai
python-dotenv
```

This structure provides:
- Clear separation of concerns
- Modular design
- Easy extensibility
- Organized template management
- Scalable architecture

Would you like me to expand on any particular aspect of the structure?