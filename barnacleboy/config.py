from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Sets up the environment variables."""

    TEMPLATE_DIR: Path = Path(__file__).parent / "templates"
    VALID_THEMES: List[str] = ["default", "forest", "dark", "neutral", "base"]
    VALID_MERMAID_CLI_EXTENSIONS: List[str] = [".png", ".svg", ".pdf", ".md"]


@lru_cache()
def get_settings() -> Settings:
    """Cached call to the settings.

    Returns:
        Settings: An object containing the environment variables.

    """
    return Settings()
