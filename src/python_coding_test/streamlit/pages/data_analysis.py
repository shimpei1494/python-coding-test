"""Data analysis page for Streamlit app."""

import io
from typing import Any

import pandas as pd
import streamlit as st

from python_coding_test.streamlit.components.charts import load_sample_data
from python_coding_test.streamlit.config import AppConfig
from python_coding_test.utils.logging_config import get_logger

logger = get_logger(__name__)


def load_uploaded_data(uploaded_file: Any) -> pd.DataFrame | None:
    """Load data from uploaded file.

    Parameters
    ----------
    uploaded_file : Any
        Streamlit uploaded file object

    Returns
    -------
    pd.DataFrame | None
        Loaded data or None if error
    """
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            logger.info("CSV file loaded", shape=df.shape, filename=uploaded_file.name)
        elif uploaded_file.name.endswith(".json"):
            df = pd.read_json(uploaded_file)
            logger.info("JSON file loaded", shape=df.shape, filename=uploaded_file.name)
        else:
            st.error(f"Unsupported file format: {uploaded_file.name}")
            return None

        return df

    except Exception as e:
        logger.error("Failed to load file", error=str(e), filename=uploaded_file.name)
        st.error(f"Error loading file: {e}")
        return None


def render_data_overview(df: pd.DataFrame) -> None:
    """Render data overview section.

    Parameters
    ----------
    df : pd.DataFrame
        Data to analyze
    """
    st.subheader("📋 Data Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Rows", f"{len(df):,}")

    with col2:
        st.metric("Total Columns", f"{len(df.columns):,}")

    with col3:
        st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")

    with col4:
        missing_values = df.isnull().sum().sum()
        st.metric("Missing Values", f"{missing_values:,}")

    # データ型情報
    with st.expander("📊 Column Information"):
        col_info = pd.DataFrame(
            {
                "Column": df.columns,
                "Type": df.dtypes.astype(str),
                "Non-Null Count": df.count(),
                "Null Count": df.isnull().sum(),
                "Unique Values": df.nunique(),
            }
        )
        st.dataframe(col_info, use_container_width=True)


def render_data_preview(df: pd.DataFrame, max_rows: int) -> None:
    """Render data preview section.

    Parameters
    ----------
    df : pd.DataFrame
        Data to preview
    max_rows : int
        Maximum rows to display
    """
    st.subheader("👀 Data Preview")

    # 表示オプション
    col1, col2 = st.columns([3, 1])

    with col1:
        preview_mode = st.selectbox(
            "Preview Mode",
            ["Head", "Tail", "Sample", "All"],
            help="Choose how to preview the data",
        )

    with col2:
        if preview_mode != "All":
            n_rows = st.number_input(
                "Rows",
                min_value=1,
                max_value=min(max_rows, len(df)),
                value=min(10, len(df)),
                step=1,
            )
        else:
            n_rows = len(df)

    # データ表示
    if preview_mode == "Head":
        preview_df = df.head(n_rows)
    elif preview_mode == "Tail":
        preview_df = df.tail(n_rows)
    elif preview_mode == "Sample":
        preview_df = df.sample(min(n_rows, len(df)))
    else:  # All
        preview_df = df.head(max_rows)

    st.dataframe(preview_df, use_container_width=True, height=400)

    if len(df) > max_rows and preview_mode == "All":
        st.warning(f"Showing first {max_rows:,} rows. Total rows: {len(df):,}")


def render_statistical_summary(df: pd.DataFrame) -> None:
    """Render statistical summary section.

    Parameters
    ----------
    df : pd.DataFrame
        Data to analyze
    """
    st.subheader("📊 Statistical Summary")

    # 数値列の統計
    numeric_cols = df.select_dtypes(include=["number"]).columns
    if len(numeric_cols) > 0:
        st.markdown("**Numeric Columns:**")
        st.dataframe(df[numeric_cols].describe(), use_container_width=True)

    # カテゴリカル列の統計
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns
    if len(categorical_cols) > 0:
        st.markdown("**Categorical Columns:**")
        cat_summary = pd.DataFrame(
            {
                "Column": categorical_cols,
                "Unique Values": [df[col].nunique() for col in categorical_cols],
                "Most Frequent": [
                    df[col].mode().iloc[0] if len(df[col].mode()) > 0 else "N/A"
                    for col in categorical_cols
                ],
                "Frequency": [
                    df[col].value_counts().iloc[0] if len(df[col]) > 0 else 0
                    for col in categorical_cols
                ],
            }
        )
        st.dataframe(cat_summary, use_container_width=True)


def render_data_quality_check(df: pd.DataFrame) -> None:
    """Render data quality check section.

    Parameters
    ----------
    df : pd.DataFrame
        Data to check
    """
    st.subheader("🔍 Data Quality Check")

    # 欠損値分析
    missing_data = df.isnull().sum()
    if missing_data.sum() > 0:
        st.markdown("**Missing Values by Column:**")
        missing_df = pd.DataFrame(
            {
                "Column": missing_data.index,
                "Missing Count": missing_data.values,
                "Missing %": (missing_data.values / len(df) * 100).round(2),
            }
        )
        missing_df = missing_df[missing_df["Missing Count"] > 0]
        st.dataframe(missing_df, use_container_width=True)
    else:
        st.success("✅ No missing values found!")

    # 重複行チェック
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        st.warning(f"⚠️ Found {duplicates:,} duplicate rows")
    else:
        st.success("✅ No duplicate rows found!")

    # データ型の整合性チェック
    with st.expander("🔧 Data Type Analysis"):
        type_issues = []

        for col in df.columns:
            if df[col].dtype == "object":
                # 数値のような文字列をチェック
                try:
                    pd.to_numeric(df[col], errors="raise")
                    type_issues.append(
                        f"Column '{col}' contains numeric data but is stored "
                        f"as text"
                    )
                except (ValueError, TypeError):
                    pass

        if type_issues:
            for issue in type_issues:
                st.info(f"💡 {issue}")
        else:
            st.success("✅ Data types look good!")


def render_data_analysis_page(config: AppConfig, sidebar_state: dict[str, Any]) -> None:
    """Render the data analysis page.

    Parameters
    ----------
    config : AppConfig
        Application configuration
    sidebar_state : dict[str, Any]
        Current sidebar state
    """
    logger.debug("Rendering data analysis page")

    st.title("📊 Data Analysis")
    st.markdown(
        "Explore and analyze your data with comprehensive statistics and " "insights."
    )

    # データソース選択
    data_source = st.radio(
        "Select Data Source",
        ["Upload Your Data", "Use Sample Data"],
        horizontal=True,
    )

    df = None

    if data_source == "Upload Your Data":
        if sidebar_state["uploaded_file"] is not None:
            df = load_uploaded_data(sidebar_state["uploaded_file"])
        else:
            st.info("👆 Please upload a file using the sidebar.")

    elif st.button("🎲 Load Sample Data", type="primary"):
        with st.spinner("Loading sample data..."):
            df = load_sample_data()
            st.success("✅ Sample data loaded successfully!")

    # データ分析の実行
    if df is not None:
        st.divider()

        # データ概要
        render_data_overview(df)

        st.divider()

        # データプレビュー
        render_data_preview(df, sidebar_state["max_rows"])

        st.divider()

        # 統計サマリー
        render_statistical_summary(df)

        st.divider()

        # データ品質チェック
        render_data_quality_check(df)

        st.divider()

        # エクスポートオプション
        st.subheader("💾 Export Options")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📄 Export CSV"):
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                st.download_button(
                    "Download CSV",
                    csv_buffer.getvalue(),
                    "analyzed_data.csv",
                    "text/csv",
                )

        with col2:
            if st.button("📋 Export JSON"):
                json_buffer = io.StringIO()
                df.to_json(json_buffer, orient="records", indent=2)
                st.download_button(
                    "Download JSON",
                    json_buffer.getvalue(),
                    "analyzed_data.json",
                    "application/json",
                )

        with col3:
            if st.button("📊 Export Summary"):
                summary_data = {
                    "overview": {
                        "total_rows": len(df),
                        "total_columns": len(df.columns),
                        "memory_usage_kb": df.memory_usage(deep=True).sum() / 1024,
                        "missing_values": df.isnull().sum().sum(),
                    },
                    "columns": df.dtypes.astype(str).to_dict(),
                    "missing_values": df.isnull().sum().to_dict(),
                    "numeric_summary": (
                        df.describe().to_dict()
                        if len(df.select_dtypes(include=["number"]).columns) > 0
                        else {}
                    ),
                }

                summary_json = io.StringIO()
                import json

                json.dump(summary_data, summary_json, indent=2)

                st.download_button(
                    "Download Summary",
                    summary_json.getvalue(),
                    "data_summary.json",
                    "application/json",
                )

    logger.debug("Data analysis page rendered successfully")
