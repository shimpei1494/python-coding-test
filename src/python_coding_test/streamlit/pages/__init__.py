"""Pages module for Streamlit app."""

from .data_analysis import render_data_analysis_page
from .home import render_home_page
from .settings import render_settings_page
from .visualization import render_visualization_page

__all__ = [
    "render_data_analysis_page",
    "render_home_page",
    "render_settings_page",
    "render_visualization_page",
]
