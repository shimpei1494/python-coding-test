"""Visualization page for Streamlit app."""

from typing import Any

import pandas as pd
import streamlit as st

from python_coding_test.streamlit.components.charts import (
    create_bar_chart,
    create_line_chart,
    create_scatter_plot,
    load_sample_data,
)
from python_coding_test.streamlit.config import AppConfig
from python_coding_test.streamlit.pages.data_analysis import load_uploaded_data
from python_coding_test.utils.logging_config import get_logger

logger = get_logger(__name__)


def get_chart_data(sidebar_state: dict[str, Any]) -> pd.DataFrame | None:
    """Get data for charting.

    Parameters
    ----------
    sidebar_state : dict[str, Any]
        Current sidebar state

    Returns
    -------
    pd.DataFrame | None
        Data for charting or None if no data
    """
    # まずアップロードされたファイルをチェック
    if sidebar_state["uploaded_file"] is not None:
        df = load_uploaded_data(sidebar_state["uploaded_file"])
        if df is not None:
            return df

    # セッション状態にサンプルデータがあるかチェック
    if "sample_data" in st.session_state:
        return st.session_state.sample_data

    return None


def render_chart_controls(df: pd.DataFrame) -> dict[str, Any]:
    """Render chart configuration controls.

    Parameters
    ----------
    df : pd.DataFrame
        Data for charting

    Returns
    -------
    dict[str, Any]
        Chart configuration
    """
    st.subheader("🎨 Chart Configuration")

    # チャートタイプ選択
    chart_type = st.selectbox(
        "Chart Type",
        ["Bar Chart", "Line Chart", "Scatter Plot"],
        help="Select the type of chart to create",
    )

    # 列選択
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    all_cols = df.columns.tolist()

    col1, col2 = st.columns(2)

    with col1:
        x_col = st.selectbox("X-axis Column", all_cols, help="Column for X-axis")

    with col2:
        y_col = st.selectbox(
            "Y-axis Column",
            numeric_cols if numeric_cols else all_cols,
            help="Column for Y-axis (preferably numeric)",
        )

    # オプション設定
    with st.expander("🔧 Advanced Options"):
        col1, col2 = st.columns(2)

        with col1:
            color_col = st.selectbox(
                "Color Column (Optional)",
                [None, *all_cols],
                help="Column to color-code the chart",
            )

            if chart_type == "Scatter Plot":
                size_col = st.selectbox(
                    "Size Column (Optional)",
                    [None, *numeric_cols],
                    help="Column to size points by",
                )
            else:
                size_col = None

        with col2:
            chart_title = st.text_input(
                "Chart Title", value=f"{chart_type}: {y_col} by {x_col}"
            )

            chart_height = st.slider(
                "Chart Height",
                min_value=300,
                max_value=800,
                value=500,
                step=50,
                help="Height of the chart in pixels",
            )

    return {
        "chart_type": chart_type,
        "x_col": x_col,
        "y_col": y_col,
        "color_col": color_col,
        "size_col": size_col,
        "title": chart_title,
        "height": chart_height,
    }


def render_data_filtering(df: pd.DataFrame) -> pd.DataFrame:
    """Render data filtering controls and return filtered data.

    Parameters
    ----------
    df : pd.DataFrame
        Original data

    Returns
    -------
    pd.DataFrame
        Filtered data
    """
    with st.expander("🔍 Data Filtering"):
        st.markdown("Filter your data before creating charts:")

        filtered_df = df.copy()

        # 数値列のフィルタリング
        numeric_cols = df.select_dtypes(include=["number"]).columns
        for col in numeric_cols:
            if col in df.columns:
                min_val, max_val = float(df[col].min()), float(df[col].max())
                if min_val != max_val:  # 値に幅がある場合のみ
                    selected_range = st.slider(
                        f"{col} Range",
                        min_value=min_val,
                        max_value=max_val,
                        value=(min_val, max_val),
                        step=(max_val - min_val) / 100,
                        key=f"filter_{col}",
                    )
                    filtered_df = filtered_df[
                        (filtered_df[col] >= selected_range[0])
                        & (filtered_df[col] <= selected_range[1])
                    ]

        # カテゴリカル列のフィルタリング
        categorical_cols = df.select_dtypes(include=["object", "category"]).columns
        for col in categorical_cols:
            if col in df.columns and df[col].nunique() <= 20:  # 20以下のユニーク値
                unique_values = df[col].unique().tolist()
                selected_values: list[str] = st.multiselect(
                    f"{col} Values",
                    unique_values,
                    default=unique_values,
                    key=f"filter_cat_{col}",
                )
                if selected_values:
                    filtered_df = filtered_df[filtered_df[col].isin(selected_values)]

        if len(filtered_df) != len(df):
            st.info(
                f"📊 Filtered data: {len(filtered_df):,} rows "
                f"(from {len(df):,} total)"
            )

        return filtered_df


def render_visualization_page(  # noqa: PLR0912, PLR0915
    config: AppConfig, sidebar_state: dict[str, Any]
) -> None:
    """Render the visualization page.

    Parameters
    ----------
    config : AppConfig
        Application configuration
    sidebar_state : dict[str, Any]
        Current sidebar state
    """
    logger.debug("Rendering visualization page")

    st.title("📈 Data Visualization")
    st.markdown("Create interactive charts and visualizations from your data.")

    # データソース選択
    data_source = st.radio(
        "Select Data Source", ["Upload Your Data", "Use Sample Data"], horizontal=True
    )

    df = None

    if data_source == "Upload Your Data":
        if sidebar_state["uploaded_file"] is not None:
            df = load_uploaded_data(sidebar_state["uploaded_file"])
        else:
            st.info("👆 Please upload a file using the sidebar.")

    else:  # Sample Data
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🎲 Load Sample Data", type="primary"):
                with st.spinner("Loading sample data..."):
                    df = load_sample_data()
                    st.session_state.sample_data = df
                    st.success("✅ Sample data loaded!")

        # セッション状態からサンプルデータを取得
        if "sample_data" in st.session_state:
            df = st.session_state.sample_data

    # データが利用可能な場合の可視化
    if df is not None:
        st.divider()

        # データフィルタリング
        filtered_df = render_data_filtering(df)

        if len(filtered_df) == 0:
            st.error("❌ No data remains after filtering. Please adjust your filters.")
            return

        st.divider()

        # チャート設定
        chart_config = render_chart_controls(filtered_df)

        st.divider()

        # チャート生成
        st.subheader("📊 Generated Chart")

        try:
            if chart_config["chart_type"] == "Bar Chart":
                fig = create_bar_chart(
                    filtered_df,
                    x_col=chart_config["x_col"],
                    y_col=chart_config["y_col"],
                    title=chart_config["title"],
                    color_col=chart_config["color_col"],
                    height=chart_config["height"],
                )

            elif chart_config["chart_type"] == "Line Chart":
                fig = create_line_chart(
                    filtered_df,
                    x_col=chart_config["x_col"],
                    y_col=chart_config["y_col"],
                    title=chart_config["title"],
                    color_col=chart_config["color_col"],
                    height=chart_config["height"],
                )

            else:  # Scatter Plot
                fig = create_scatter_plot(
                    filtered_df,
                    x_col=chart_config["x_col"],
                    y_col=chart_config["y_col"],
                    title=chart_config["title"],
                    color_col=chart_config["color_col"],
                    size_col=chart_config["size_col"],
                    height=chart_config["height"],
                )

            # チャートを表示
            st.plotly_chart(fig, use_container_width=True)

            # チャート情報
            with st.expander("📋 Chart Information"):
                st.markdown(f"**Chart Type:** {chart_config['chart_type']}")
                st.markdown(f"**Data Points:** {len(filtered_df):,}")
                st.markdown(f"**X-axis:** {chart_config['x_col']}")
                st.markdown(f"**Y-axis:** {chart_config['y_col']}")
                if chart_config["color_col"]:
                    st.markdown(f"**Color:** {chart_config['color_col']}")
                if chart_config.get("size_col"):
                    st.markdown(f"**Size:** {chart_config['size_col']}")

            # エクスポートオプション
            st.divider()
            st.subheader("💾 Export Chart")

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("📷 Export PNG"):
                    img_bytes = fig.to_image(format="png", width=1200, height=800)
                    st.download_button(
                        "Download PNG",
                        img_bytes,
                        (
                            "chart_"
                            + chart_config["chart_type"].lower().replace(" ", "_")
                            + ".png"
                        ),
                        "image/png",
                    )

            with col2:
                if st.button("🖼️ Export SVG"):
                    svg_bytes = fig.to_image(format="svg")
                    st.download_button(
                        "Download SVG",
                        svg_bytes,
                        (
                            "chart_"
                            + chart_config["chart_type"].lower().replace(" ", "_")
                            + ".svg"
                        ),
                        "image/svg+xml",
                    )

            with col3:
                if st.button("📄 Export HTML"):
                    html_str = fig.to_html(include_plotlyjs="cdn")
                    st.download_button(
                        "Download HTML",
                        html_str,
                        (
                            "chart_"
                            + chart_config["chart_type"].lower().replace(" ", "_")
                            + ".html"
                        ),
                        "text/html",
                    )

        except Exception as e:
            logger.error("Failed to create chart", error=str(e), exc_info=True)
            st.error(f"❌ Failed to create chart: {e}")

            # エラー詳細
            with st.expander("🔍 Error Details"):
                st.code(str(e))
                st.markdown("**Suggestions:**")
                st.markdown(
                    "- Check if selected columns contain appropriate data types"
                )
                st.markdown("- Ensure Y-axis column contains numeric data")
                st.markdown("- Try different column combinations")

    else:
        # データがない場合のヘルプ
        st.info(
            """
            📊 **Ready to create amazing visualizations!**

            To get started:
            1. Upload your data file (CSV/JSON) using the sidebar, or
            2. Click 'Load Sample Data' to try with demo data
            3. Configure your chart settings
            4. Explore interactive visualizations!

            **Supported chart types:**
            - 📊 Bar Charts - Compare categories
            - 📈 Line Charts - Show trends over time
            - 🔸 Scatter Plots - Explore relationships
            """
        )

    logger.debug("Visualization page rendered successfully")
