"""Home page for Streamlit app."""

from typing import Any

import streamlit as st

from python_coding_test.streamlit.config import AppConfig
from python_coding_test.utils.logging_config import get_logger

logger = get_logger(__name__)


def render_home_page(config: AppConfig, sidebar_state: dict[str, Any]) -> None:
    """Render the home page.

    Parameters
    ----------
    config : AppConfig
        Application configuration
    sidebar_state : dict[str, Any]
        Current sidebar state
    """
    logger.debug("Rendering home page")

    # ヘッダー
    st.title("🏠 Welcome to Python Coding Test")
    st.markdown(
        """
        <div style='padding: 1rem; background-color: #f0f2f6;
                    border-radius: 10px; margin-bottom: 2rem;'>
            <h3 style='margin: 0; color: #1f77b4;'>
                📊 Data Analysis & Visualization Platform
            </h3>
            <p style='margin: 0.5rem 0 0 0; color: #333;'>
                Explore, analyze, and visualize your data with
                interactive tools powered by Streamlit.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 機能紹介
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            ### 📊 Data Analysis
            - CSV/JSON file upload
            - Statistical summaries
            - Data cleaning tools
            - Column analysis
            """
        )

    with col2:
        st.markdown(
            """
            ### 📈 Visualization
            - Interactive charts
            - Multiple chart types
            - Custom styling
            - Export options
            """
        )

    with col3:
        st.markdown(
            """
            ### ⚙️ Settings
            - Theme customization
            - Performance tuning
            - Export preferences
            - Advanced options
            """
        )

    st.divider()

    # クイックスタート
    st.subheader("🚀 Quick Start")

    if sidebar_state["uploaded_file"] is None:
        st.info(
            """
            👆 **Get started by uploading a file in the sidebar!**

            Supported formats: CSV, JSON

            Or try the sample data in the **Data Analysis** page.
            """
        )
    else:
        st.success(
            f"""
            ✅ **File uploaded:** {sidebar_state["uploaded_file"].name}

            Navigate to **Data Analysis** or **Visualization** to explore your data!
            """
        )

    # 最近の活動（デモ用）
    with st.expander("📈 Recent Activity (Demo)", expanded=False):
        st.markdown(
            """
            - 📁 **sample_data.csv** analyzed (2 minutes ago)
            - 📊 **Sales Report** chart created (5 minutes ago)
            - ⚙️ **Settings** updated (10 minutes ago)
            - 📈 **Performance Dashboard** exported (1 hour ago)
            """
        )

    # システム情報
    st.divider()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### ℹ️ System Info")
        st.markdown(
            f"""
            - **App Version:** 0.1.0
            - **Layout:** {config.layout.title()}
            - **Max Upload:** {config.max_upload_size_mb} MB
            - **Log Level:** {sidebar_state["log_level"]}
            """
        )

    with col2:
        st.markdown("### 🔧 Tech Stack")
        st.markdown(
            """
            - **Frontend:** Streamlit
            - **Data:** Pandas, NumPy
            - **Visualization:** Plotly, Matplotlib
            - **Quality:** Ruff, mypy, pytest
            """
        )

    # フッター
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 0.9rem;'>
            Built with ❤️ using <strong>Python</strong> and
            <strong>Streamlit</strong><br>
            Powered by <strong>Claude Code</strong> development workflow
        </div>
        """,
        unsafe_allow_html=True,
    )

    logger.debug("Home page rendered successfully")
