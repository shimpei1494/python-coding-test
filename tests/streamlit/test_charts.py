"""Tests for Streamlit chart components."""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pytest

from python_coding_test.streamlit.components.charts import (
    create_bar_chart,
    create_line_chart,
    create_scatter_plot,
    load_sample_data,
)


class TestChartComponents:
    """Test chart creation functions."""

    @pytest.fixture
    def sample_df(self) -> pd.DataFrame:
        """Create sample DataFrame for testing."""
        return pd.DataFrame(
            {
                "x": [1, 2, 3, 4, 5],
                "y": [10, 20, 15, 25, 30],
                "category": ["A", "B", "A", "B", "A"],
                "size": [5, 10, 7, 12, 8],
            }
        )

    def test_正常系_棒グラフが作成される(self, sample_df: pd.DataFrame) -> None:
        """棒グラフが正しく作成されることを確認。"""
        fig = create_bar_chart(sample_df, x_col="x", y_col="y")

        assert isinstance(fig, go.Figure)
        assert fig.data[0].type == "bar"
        assert len(fig.data[0].x) == 5
        assert len(fig.data[0].y) == 5

    def test_正常系_棒グラフが色分けされる(self, sample_df: pd.DataFrame) -> None:
        """色分けされた棒グラフが作成されることを確認。"""
        fig = create_bar_chart(
            sample_df,
            x_col="x",
            y_col="y",
            color_col="category",
            title="Test Bar Chart",
        )

        assert isinstance(fig, go.Figure)
        assert fig.layout.title.text == "Test Bar Chart"
        # 色分けがある場合、複数のトレースが作成される
        assert len(fig.data) >= 1

    def test_正常系_折れ線グラフが作成される(self, sample_df: pd.DataFrame) -> None:
        """折れ線グラフが正しく作成されることを確認。"""
        fig = create_line_chart(sample_df, x_col="x", y_col="y")

        assert isinstance(fig, go.Figure)
        assert fig.data[0].type == "scatter"
        assert fig.data[0].mode == "lines+markers"
        assert len(fig.data[0].x) == 5
        assert len(fig.data[0].y) == 5

    def test_正常系_散布図が作成される(self, sample_df: pd.DataFrame) -> None:
        """散布図が正しく作成されることを確認。"""
        fig = create_scatter_plot(sample_df, x_col="x", y_col="y")

        assert isinstance(fig, go.Figure)
        assert fig.data[0].type == "scatter"
        assert fig.data[0].mode == "markers"
        assert len(fig.data[0].x) == 5
        assert len(fig.data[0].y) == 5

    def test_正常系_散布図がサイズ指定で作成される(
        self, sample_df: pd.DataFrame
    ) -> None:
        """サイズ指定付きの散布図が作成されることを確認。"""
        fig = create_scatter_plot(
            sample_df, x_col="x", y_col="y", size_col="size", height=600
        )

        assert isinstance(fig, go.Figure)
        assert fig.layout.height == 600

    def test_異常系_存在しない列名でValueError(self, sample_df: pd.DataFrame) -> None:
        """存在しない列名を指定した場合、ValueErrorが発生することを確認。"""
        with pytest.raises(ValueError, match="Failed to create bar chart"):
            create_bar_chart(sample_df, x_col="nonexistent", y_col="y")

    def test_異常系_空のDataFrameでValueError(self) -> None:
        """空のDataFrameを渡した場合、ValueErrorが発生することを確認。"""
        empty_df = pd.DataFrame()

        with pytest.raises(ValueError, match="Failed to create line chart"):
            create_line_chart(empty_df, x_col="x", y_col="y")

    def test_正常系_チャートのレイアウトが正しく設定される(
        self, sample_df: pd.DataFrame
    ) -> None:
        """チャートのレイアウトが正しく設定されることを確認。"""
        fig = create_bar_chart(
            sample_df, x_col="x", y_col="y", title="Custom Title", height=400
        )

        assert fig.layout.title.text == "Custom Title"
        assert fig.layout.height == 400
        assert fig.layout.xaxis.title.text == "X"
        assert fig.layout.yaxis.title.text == "Y"


class TestLoadSampleData:
    """Test sample data loading."""

    def test_正常系_サンプルデータが読み込まれる(self) -> None:
        """サンプルデータが正しく読み込まれることを確認。"""
        df = load_sample_data()

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 100
        assert "date" in df.columns
        assert "sales" in df.columns
        assert "profit" in df.columns
        assert "category" in df.columns
        assert "region" in df.columns
        assert "customer_count" in df.columns
        assert "satisfaction" in df.columns

    def test_正常系_サンプルデータの型が正しい(self) -> None:
        """サンプルデータの型が正しいことを確認。"""
        df = load_sample_data()

        assert pd.api.types.is_datetime64_any_dtype(df["date"])
        assert pd.api.types.is_integer_dtype(df["sales"])
        assert pd.api.types.is_integer_dtype(df["profit"])
        assert pd.api.types.is_object_dtype(df["category"])
        assert pd.api.types.is_object_dtype(df["region"])
        assert pd.api.types.is_integer_dtype(df["customer_count"])
        assert pd.api.types.is_float_dtype(df["satisfaction"])

    def test_正常系_サンプルデータの値範囲が妥当(self) -> None:
        """サンプルデータの値範囲が妥当であることを確認。"""
        df = load_sample_data()

        # 売上は正の値
        assert (df["sales"] > 0).all()

        # 満足度は1-5の範囲
        assert (df["satisfaction"] >= 1).all()
        assert (df["satisfaction"] <= 5).all()

        # カテゴリの種類
        assert set(df["category"].unique()) == {"A", "B", "C"}
        assert set(df["region"].unique()) == {"North", "South", "East", "West"}

    def test_正常系_再現性がある(self) -> None:
        """同じシードで同じデータが生成されることを確認。"""
        df1 = load_sample_data()
        df2 = load_sample_data()

        pd.testing.assert_frame_equal(df1, df2)
