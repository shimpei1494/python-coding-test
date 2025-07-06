"""Sidebar component for Streamlit app."""

from typing import Any

import streamlit as st

from python_coding_test.streamlit.config import AppConfig
from python_coding_test.utils.logging_config import get_logger

logger = get_logger(__name__)


def render_sidebar(config: AppConfig) -> dict[str, Any]:
    """Render the sidebar with navigation and settings.

    Parameters
    ----------
    config : AppConfig
        Application configuration

    Returns
    -------
    dict[str, Any]
        Sidebar state and user selections
    """
    logger.debug("Rendering sidebar")

    with st.sidebar:
        st.title("🎛️ Control Panel")

        # ページナビゲーション
        st.subheader("📄 Navigation")
        selected_page = st.selectbox(
            "Select Page",
            options=["home", "data_analysis", "visualization", "settings"],
            format_func=lambda x: {
                "home": "🏠 Home",
                "data_analysis": "📊 Data Analysis",
                "visualization": "📈 Visualization",
                "settings": "⚙️ Settings",
            }[x],
            key="page_selection",
        )

        st.divider()

        # データアップロード
        st.subheader("📤 Data Upload")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=config.allowed_file_formats,
            help=f"Supported formats: {', '.join(config.allowed_file_formats or [])}",
        )

        # ファイル情報表示
        if uploaded_file is not None:
            st.success(f"📁 File: {uploaded_file.name}")
            st.info(f"📏 Size: {uploaded_file.size / 1024:.1f} KB")

        st.divider()

        # 設定パネル
        st.subheader("⚙️ Settings")

        # ログレベル
        log_level = st.selectbox(
            "Log Level",
            options=["DEBUG", "INFO", "WARNING", "ERROR"],
            index=1,  # INFO
            help="Set logging verbosity",
        )

        # テーマ設定
        with st.expander("🎨 Theme Settings"):
            primary_color = st.color_picker(
                "Primary Color",
                value=config.theme_primary_color,
                help="Main accent color",
            )

            show_advanced = st.checkbox("Show Advanced Options")

            if show_advanced:
                max_rows = st.number_input(
                    "Max Rows to Display",
                    min_value=10,
                    max_value=10000,
                    value=1000,
                    step=100,
                )

                enable_caching = st.checkbox(
                    "Enable Data Caching",
                    value=True,
                    help="Cache processed data for better performance",
                )
            else:
                max_rows = 1000
                enable_caching = True

        st.divider()

        # 情報表示
        with st.expander("ℹ️ App Info"):
            st.write(f"**Title:** {config.title}")
            st.write(f"**Layout:** {config.layout}")
            st.write(f"**Max Upload:** {config.max_upload_size_mb} MB")
            st.write("**Built with:** 🐍 Python + Streamlit")

    sidebar_state = {
        "selected_page": selected_page,
        "uploaded_file": uploaded_file,
        "log_level": log_level,
        "primary_color": primary_color,
        "max_rows": max_rows,
        "enable_caching": enable_caching,
    }

    logger.debug(
        "Sidebar rendered",
        selected_page=selected_page,
        has_file=uploaded_file is not None,
        log_level=log_level,
    )

    return sidebar_state
