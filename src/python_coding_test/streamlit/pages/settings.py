"""Settings page for Streamlit app."""

from typing import Any

import streamlit as st

from python_coding_test.streamlit.config import AppConfig
from python_coding_test.utils.logging_config import get_logger, set_log_level

logger = get_logger(__name__)


def render_settings_page(  # noqa: PLR0915
    config: AppConfig, sidebar_state: dict[str, Any]
) -> None:
    """Render the settings page.

    Parameters
    ----------
    config : AppConfig
        Application configuration
    sidebar_state : dict[str, Any]
        Current sidebar state
    """
    logger.debug("Rendering settings page")

    st.title("⚙️ Settings")
    st.markdown("Configure application preferences and performance settings.")

    # アプリケーション設定
    st.subheader("🎛️ Application Settings")

    col1, col2 = st.columns(2)

    with col1:
        # テーマ設定
        st.markdown("**🎨 Theme Configuration**")

        new_primary_color = st.color_picker(
            "Primary Color",
            value=sidebar_state.get("primary_color", config.theme_primary_color),
            help="Main accent color for the app",
        )

        layout_mode = st.selectbox(
            "Layout Mode",
            ["wide", "centered"],
            index=0 if config.layout == "wide" else 1,
            help="Page layout configuration",
        )

        sidebar_state_option = st.selectbox(
            "Sidebar Default State",
            ["expanded", "collapsed", "auto"],
            index=0,
            help="Default state of the sidebar",
        )

    with col2:
        # パフォーマンス設定
        st.markdown("**⚡ Performance Settings**")

        enable_caching = st.checkbox(
            "Enable Data Caching",
            value=sidebar_state.get("enable_caching", True),
            help="Cache processed data for better performance",
        )

        max_upload_size = st.number_input(
            "Max Upload Size (MB)",
            min_value=1,
            max_value=500,
            value=config.max_upload_size_mb,
            step=10,
            help="Maximum file size for uploads",
        )

        max_display_rows = st.number_input(
            "Max Display Rows",
            min_value=100,
            max_value=50000,
            value=sidebar_state.get("max_rows", 1000),
            step=100,
            help="Maximum rows to display in data tables",
        )

    st.divider()

    # ログ設定
    st.subheader("📝 Logging Configuration")

    col1, col2 = st.columns(2)

    with col1:
        current_log_level = st.selectbox(
            "Application Log Level",
            ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            index=[
                "DEBUG",
                "INFO",
                "WARNING",
                "ERROR",
                "CRITICAL",
            ].index(sidebar_state.get("log_level", "INFO")),
            help="Set the verbosity of application logging",
        )

        if st.button("Apply Log Level"):
            set_log_level(current_log_level)
            st.success(f"✅ Log level set to {current_log_level}")
            logger.info("Log level changed", new_level=current_log_level)

    with col2:
        show_debug_info = st.checkbox(
            "Show Debug Information",
            value=False,
            help="Display debug information in the UI",
        )

        if show_debug_info:
            with st.expander("🔍 Debug Information"):
                st.json(
                    {
                        "session_state_keys": list(st.session_state.keys()),
                        "sidebar_state": sidebar_state,
                        "config": {
                            "title": config.title,
                            "layout": config.layout,
                            "log_level": config.log_level,
                            "max_upload_size_mb": config.max_upload_size_mb,
                        },
                    }
                )

    st.divider()

    # データ設定
    st.subheader("📊 Data Settings")

    col1, col2 = st.columns(2)

    with col1:
        # ファイル形式設定
        st.markdown("**📁 Supported File Formats**")

        supported_formats = st.multiselect(
            "File Formats",
            ["csv", "json", "xlsx", "parquet"],
            default=config.allowed_file_formats,
            help="File formats allowed for upload",
        )

        auto_detect_types = st.checkbox(
            "Auto-detect Data Types",
            value=True,
            help="Automatically detect and convert data types",
        )

    with col2:
        # エクスポート設定
        st.markdown("**💾 Export Settings**")

        default_export_format = st.selectbox(
            "Default Export Format",
            ["csv", "json", "xlsx"],
            help="Default format for data exports",
        )

        include_index = st.checkbox(
            "Include Index in Exports",
            value=False,
            help="Include row indices in exported files",
        )

    st.divider()

    # チャート設定
    st.subheader("📈 Chart Settings")

    col1, col2 = st.columns(2)

    with col1:
        # デフォルトチャート設定
        st.markdown("**🎨 Default Chart Settings**")

        default_chart_height = st.slider(
            "Default Chart Height",
            min_value=300,
            max_value=800,
            value=500,
            step=50,
            help="Default height for charts in pixels",
        )

        chart_theme = st.selectbox(
            "Chart Theme",
            ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn"],
            index=1,  # plotly_white
            help="Default theme for charts",
        )

    with col2:
        # 相互作用設定
        st.markdown("**🖱️ Interaction Settings**")

        enable_zoom = st.checkbox(
            "Enable Chart Zoom", value=True, help="Allow zooming in charts"
        )

        enable_pan = st.checkbox(
            "Enable Chart Pan", value=True, help="Allow panning in charts"
        )

        show_toolbar = st.checkbox(
            "Show Chart Toolbar",
            value=True,
            help="Display chart toolbar with export options",
        )

    st.divider()

    # システム情報
    st.subheader("ℹ️ System Information")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**📦 Application Info**")
        st.markdown("- **Version:** 0.1.0")
        st.markdown("- **Python:** 3.12+")
        st.markdown(f"- **Streamlit:** {st.__version__}")
        st.markdown(f"- **Layout:** {config.layout}")

    with col2:
        st.markdown("**💾 Current Settings**")
        st.markdown(f"- **Log Level:** {current_log_level}")
        st.markdown(f"- **Max Upload:** {max_upload_size} MB")
        st.markdown(f"- **Max Rows:** {max_display_rows:,}")
        st.markdown(f"- **Caching:** {'Enabled' if enable_caching else 'Disabled'}")

    st.divider()

    # アクション
    st.subheader("🔧 Actions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🔄 Reset Settings", type="secondary"):
            # セッション状態をクリア
            for key in list(st.session_state.keys()):
                if isinstance(key, str) and (
                    key.startswith("filter_") or key in ["sample_data"]
                ):
                    del st.session_state[key]
            st.success("✅ Settings reset to defaults")
            st.rerun()

    with col2:
        if st.button("🗑️ Clear Cache", type="secondary"):
            st.cache_data.clear()
            st.success("✅ Cache cleared")

    with col3:
        if st.button("📥 Export Settings"):
            settings_export = {
                "theme": {
                    "primary_color": new_primary_color,
                    "layout": layout_mode,
                    "sidebar_state": sidebar_state_option,
                },
                "performance": {
                    "enable_caching": enable_caching,
                    "max_upload_size_mb": max_upload_size,
                    "max_display_rows": max_display_rows,
                },
                "logging": {
                    "log_level": current_log_level,
                    "show_debug_info": show_debug_info,
                },
                "data": {
                    "supported_formats": supported_formats,
                    "auto_detect_types": auto_detect_types,
                    "default_export_format": default_export_format,
                    "include_index": include_index,
                },
                "charts": {
                    "default_height": default_chart_height,
                    "theme": chart_theme,
                    "enable_zoom": enable_zoom,
                    "enable_pan": enable_pan,
                    "show_toolbar": show_toolbar,
                },
            }

            import json

            settings_json = json.dumps(settings_export, indent=2)

            st.download_button(
                "Download Settings",
                settings_json,
                "app_settings.json",
                "application/json",
            )

    with col4:
        uploaded_settings = st.file_uploader(
            "Import Settings",
            type=["json"],
            help="Import previously exported settings",
        )

        if uploaded_settings is not None:
            try:
                import json

                imported_settings = json.load(uploaded_settings)
                st.success("✅ Settings imported successfully!")
                with st.expander("📋 Imported Settings"):
                    st.json(imported_settings)
            except Exception as e:
                st.error(f"❌ Failed to import settings: {e}")

    # フッター
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 0.9rem;'>
            💡 <strong>Tip:</strong> Changes to most settings take effect
            immediately.<br>
            Some changes may require refreshing the page or reloading data.
        </div>
        """,
        unsafe_allow_html=True,
    )

    logger.debug("Settings page rendered successfully")
