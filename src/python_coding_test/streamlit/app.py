"""Main Streamlit application."""

from typing import Any

import streamlit as st

from python_coding_test.streamlit.components.sidebar import render_sidebar
from python_coding_test.streamlit.config import AppConfig
from python_coding_test.streamlit.pages import (
    render_data_analysis_page,
    render_home_page,
    render_settings_page,
    render_visualization_page,
)
from python_coding_test.utils.logging_config import get_logger, setup_logging

logger = get_logger(__name__)


def configure_page(config: AppConfig) -> None:
    """Configure Streamlit page settings.

    Parameters
    ----------
    config : AppConfig
        Application configuration
    """
    st.set_page_config(
        page_title=config.page_title,
        page_icon=config.page_icon,
        layout=config.layout,
        initial_sidebar_state=config.initial_sidebar_state,
    )

    # カスタムCSS
    st.markdown(
        f"""
        <style>
        .main .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}

        .stSelectbox > div > div > div {{
            background-color: white;
        }}

        /* カスタムカラー */
        .stButton > button:first-child {{
            background-color: {config.theme_primary_color};
            color: white;
            border: none;
        }}

        .stButton > button:first-child:hover {{
            background-color: {config.theme_primary_color}dd;
            color: white;
        }}

        /* メトリクス表示の改善 */
        .metric-container {{
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid {config.theme_primary_color};
        }}

        /* エラーメッセージのスタイル */
        .stAlert > div {{
            border-radius: 0.5rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def route_to_page(
    page_name: str, config: AppConfig, sidebar_state: dict[str, Any]
) -> None:
    """Route to the appropriate page based on selection.

    Parameters
    ----------
    page_name : str
        Name of the page to render
    config : AppConfig
        Application configuration
    sidebar_state : dict[str, Any]
        Current sidebar state
    """
    logger.debug("Routing to page", page_name=page_name)

    try:
        if page_name == "home":
            render_home_page(config, sidebar_state)
        elif page_name == "data_analysis":
            render_data_analysis_page(config, sidebar_state)
        elif page_name == "visualization":
            render_visualization_page(config, sidebar_state)
        elif page_name == "settings":
            render_settings_page(config, sidebar_state)
        else:
            st.error(f"❌ Unknown page: {page_name}")
            logger.error("Unknown page requested", page_name=page_name)

    except Exception as e:
        logger.error(
            "Page rendering failed",
            page_name=page_name,
            error=str(e),
            exc_info=True,
        )
        st.error(f"❌ Failed to load page: {e}")

        with st.expander("🔍 Error Details"):
            st.code(str(e))
            st.markdown(
                "Please try refreshing the page or contact support if the "
                "issue persists."
            )


def main() -> None:
    """Main application entry point."""
    # ロギング設定
    setup_logging(level="INFO", format="console")
    logger.info("Starting Streamlit application")

    try:
        # アプリケーション設定
        config = AppConfig()

        # ページ設定
        configure_page(config)

        # サイドバーをレンダリング
        sidebar_state = render_sidebar(config)

        # 選択されたページをレンダリング
        route_to_page(sidebar_state["selected_page"], config, sidebar_state)

        logger.debug("Application rendered successfully")

    except Exception as e:
        logger.error("Application startup failed", error=str(e), exc_info=True)
        st.error("❌ Application failed to start. Please check the logs for details.")

        # 緊急時のベーシックページ
        st.title("🚨 Error")
        st.markdown("The application encountered an error during startup.")

        with st.expander("🔍 Error Details"):
            st.code(str(e))
            st.markdown(
                """
                **Possible solutions:**
                1. Refresh the page
                2. Clear browser cache
                3. Check application logs
                4. Contact technical support
                """
            )


if __name__ == "__main__":
    main()
