"""Chart components for Streamlit app."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from python_coding_test.utils.logging_config import get_logger

logger = get_logger(__name__)


def create_bar_chart(  # noqa: PLR0913
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    *,
    title: str = "Bar Chart",
    color_col: str | None = None,
    height: int = 400,
) -> go.Figure:
    """Create an interactive bar chart.

    Parameters
    ----------
    data : pd.DataFrame
        Input data
    x_col : str
        Column name for x-axis
    y_col : str
        Column name for y-axis
    title : str, default="Bar Chart"
        Chart title
    color_col : str | None, default=None
        Column name for color coding
    height : int, default=400
        Chart height in pixels

    Returns
    -------
    go.Figure
        Plotly figure object
    """
    logger.debug(
        "Creating bar chart",
        x_col=x_col,
        y_col=y_col,
        color_col=color_col,
        rows=len(data),
    )

    try:
        fig = px.bar(
            data,
            x=x_col,
            y=y_col,
            color=color_col,
            title=title,
            height=height,
            template="plotly_white",
        )

        fig.update_layout(
            xaxis_title=x_col.replace("_", " ").title(),
            yaxis_title=y_col.replace("_", " ").title(),
            showlegend=color_col is not None,
        )

        logger.debug("Bar chart created successfully")
        return fig

    except Exception as e:
        logger.error("Failed to create bar chart", error=str(e), exc_info=True)
        raise ValueError(f"Failed to create bar chart: {e}") from e


def create_line_chart(  # noqa: PLR0913
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    *,
    title: str = "Line Chart",
    color_col: str | None = None,
    height: int = 400,
) -> go.Figure:
    """Create an interactive line chart.

    Parameters
    ----------
    data : pd.DataFrame
        Input data
    x_col : str
        Column name for x-axis
    y_col : str
        Column name for y-axis
    title : str, default="Line Chart"
        Chart title
    color_col : str | None, default=None
        Column name for color coding
    height : int, default=400
        Chart height in pixels

    Returns
    -------
    go.Figure
        Plotly figure object
    """
    logger.debug(
        "Creating line chart",
        x_col=x_col,
        y_col=y_col,
        color_col=color_col,
        rows=len(data),
    )

    try:
        fig = px.line(
            data,
            x=x_col,
            y=y_col,
            color=color_col,
            title=title,
            height=height,
            template="plotly_white",
        )

        fig.update_layout(
            xaxis_title=x_col.replace("_", " ").title(),
            yaxis_title=y_col.replace("_", " ").title(),
            showlegend=color_col is not None,
        )

        fig.update_traces(mode="lines+markers", line=dict(width=2), marker=dict(size=6))

        logger.debug("Line chart created successfully")
        return fig

    except Exception as e:
        logger.error("Failed to create line chart", error=str(e), exc_info=True)
        raise ValueError(f"Failed to create line chart: {e}") from e


def create_scatter_plot(  # noqa: PLR0913
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    *,
    title: str = "Scatter Plot",
    color_col: str | None = None,
    size_col: str | None = None,
    height: int = 400,
) -> go.Figure:
    """Create an interactive scatter plot.

    Parameters
    ----------
    data : pd.DataFrame
        Input data
    x_col : str
        Column name for x-axis
    y_col : str
        Column name for y-axis
    title : str, default="Scatter Plot"
        Chart title
    color_col : str | None, default=None
        Column name for color coding
    size_col : str | None, default=None
        Column name for point size
    height : int, default=400
        Chart height in pixels

    Returns
    -------
    go.Figure
        Plotly figure object
    """
    logger.debug(
        "Creating scatter plot",
        x_col=x_col,
        y_col=y_col,
        color_col=color_col,
        size_col=size_col,
        rows=len(data),
    )

    try:
        fig = px.scatter(
            data,
            x=x_col,
            y=y_col,
            color=color_col,
            size=size_col,
            title=title,
            height=height,
            template="plotly_white",
        )

        fig.update_layout(
            xaxis_title=x_col.replace("_", " ").title(),
            yaxis_title=y_col.replace("_", " ").title(),
            showlegend=color_col is not None,
        )

        fig.update_traces(marker=dict(opacity=0.7, line=dict(width=1, color="white")))

        logger.debug("Scatter plot created successfully")
        return fig

    except Exception as e:
        logger.error("Failed to create scatter plot", error=str(e), exc_info=True)
        raise ValueError(f"Failed to create scatter plot: {e}") from e


@st.cache_data  # type: ignore[misc]
def load_sample_data() -> pd.DataFrame:
    """Load sample data for demonstration.

    Returns
    -------
    pd.DataFrame
        Sample dataset
    """
    logger.debug("Loading sample data")

    import numpy as np

    # サンプルデータの生成
    np.random.seed(42)
    n_samples = 100

    data = {
        "date": pd.date_range("2024-01-01", periods=n_samples, freq="D"),
        "sales": np.random.normal(1000, 200, n_samples).astype(int),
        "profit": np.random.normal(150, 50, n_samples).astype(int),
        "category": np.random.choice(["A", "B", "C"], n_samples),
        "region": np.random.choice(["North", "South", "East", "West"], n_samples),
        "customer_count": np.random.poisson(50, n_samples),
    }

    df = pd.DataFrame(data)

    # 相関関係を作る
    df["profit"] = (df["sales"] * 0.15 + np.random.normal(0, 30, n_samples)).astype(int)
    df["satisfaction"] = np.clip(
        (df["profit"] / df["sales"] * 100 * 5 + np.random.normal(0, 0.5, n_samples)),
        1,
        5,
    ).round(1)

    logger.debug("Sample data loaded", shape=df.shape, columns=list(df.columns))
    return df
