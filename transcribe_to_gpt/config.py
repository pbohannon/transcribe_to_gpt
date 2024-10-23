# config.py
import os
from dataclasses import dataclass
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv


@dataclass
class APIConfig:
    """Configuration class to hold API-related settings"""
    api_key: str
    model: str = "gpt-4o"

    @classmethod
    def from_env(cls, env_file: Optional[str] = None) -> 'APIConfig':
        """
        Create configuration from environment variables.
        Will attempt to load from .env file if present.

        Args:
            env_file: Optional path to .env file. If None, will search in default locations.
        """
        # Try to load .env file if it exists
        if env_file:
            load_dotenv(env_file)
        else:
            # Look for .env in current and parent directories
            current_dir = Path.cwd()
            possible_paths = [
                current_dir / '.env',
                current_dir.parent / '.env'
            ]

            for path in possible_paths:
                if path.exists():
                    load_dotenv(path)
                    break

        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required. "
                "Please set it in your .env file or environment."
            )

        model = os.getenv('OPENAI_MODEL', cls.model)

        return cls(api_key=api_key, model=model)

    def validate(self) -> None:
        """Validate configuration settings"""
        if not self.api_key:
            raise ValueError("API key cannot be empty")
        if not self.model:
            raise ValueError("Model name cannot be empty")
        if not self.api_key.startswith('sk-'):
            raise ValueError("API key appears to be invalid (should start with 'sk-')")


_config_instance: Optional[APIConfig] = None


def get_config(env_file: Optional[str] = None) -> APIConfig:
    """
    Get configuration singleton.
    Creates new configuration only on first call.

    Args:
        env_file: Optional path to .env file
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = APIConfig.from_env(env_file)
        _config_instance.validate()
    return _config_instance