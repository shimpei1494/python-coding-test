"""Streamlit application settings."""

from dataclasses import dataclass
from typing import Literal

from python_coding_test.types import FileFormat, LogLevel
from python_coding_test.utils.logging_config import get_logger

logger = get_logger(__name__)

PageName = Literal["home", "data_analysis", "visualization", "settings"]


@dataclass
class AppConfig:
    """Streamlit application configuration."""

    title: str = "Python Coding Test - Streamlit App"
    page_title: str = "Python Coding Test"
    page_icon: str = "📊"
    layout: Literal["centered", "wide"] = "wide"
    initial_sidebar_state: Literal["auto", "expanded", "collapsed"] = "expanded"
    log_level: LogLevel = "INFO"
    max_upload_size_mb: int = 200
    allowed_file_formats: list[FileFormat] | None = None
    theme_primary_color: str = "#FF6B6B"
    theme_background_color: str = "#FFFFFF"
    theme_secondary_background_color: str = "#F0F2F6"
    theme_text_color: str = "#262730"

    def __post_init__(self) -> None:
        """Initialize default values."""
        if self.allowed_file_formats is None:
            self.allowed_file_formats = ["csv", "json"]

        logger.debug(
            "AppConfig initialized",
            title=self.title,
            layout=self.layout,
            max_upload_size_mb=self.max_upload_size_mb,
        )
