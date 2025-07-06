"""Integration tests for Streamlit application."""

import pandas as pd
import pytest

from python_coding_test.streamlit.components.charts import load_sample_data
from python_coding_test.streamlit.config import AppConfig


class TestStreamlitIntegration:
    """Integration tests for Streamlit components."""

    def test_正常系_設定とサンプルデータの統合(self) -> None:
        """AppConfigとサンプルデータが正しく連携することを確認。"""
        config = AppConfig()
        df = load_sample_data()

        # 設定で許可されたファイル形式を確認
        assert "csv" in config.allowed_file_formats
        assert "json" in config.allowed_file_formats

        # サンプルデータの基本検証
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert not df.empty

        # アップロードサイズ制限との整合性
        estimated_size_kb = df.memory_usage(deep=True).sum() / 1024
        assert estimated_size_kb < config.max_upload_size_mb * 1024

    def test_正常系_チャート作成とデータ処理の統合(self) -> None:
        """チャート作成とデータ処理が正しく統合されることを確認。"""
        from python_coding_test.streamlit.components.charts import (
            create_bar_chart,
            create_line_chart,
            create_scatter_plot,
        )

        df = load_sample_data()

        # 数値列の取得
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        assert len(numeric_cols) > 0

        # 各チャートタイプでの動作確認
        x_col = "date"
        y_col = numeric_cols[0]

        # 棒グラフ
        bar_fig = create_bar_chart(df, x_col=x_col, y_col=y_col)
        assert bar_fig is not None
        assert len(bar_fig.data) > 0

        # 折れ線グラフ
        line_fig = create_line_chart(df, x_col=x_col, y_col=y_col)
        assert line_fig is not None
        assert len(line_fig.data) > 0

        # 散布図
        scatter_fig = create_scatter_plot(df, x_col=x_col, y_col=y_col)
        assert scatter_fig is not None
        assert len(scatter_fig.data) > 0

    def test_正常系_データフィルタリングとチャート作成(self) -> None:
        """データフィルタリングとチャート作成の統合テスト。"""
        from python_coding_test.streamlit.components.charts import create_bar_chart

        df = load_sample_data()

        # カテゴリ別フィルタリング
        category_a_data = df[df["category"] == "A"]
        assert len(category_a_data) > 0

        # フィルタリングされたデータでチャート作成
        fig = create_bar_chart(
            category_a_data, x_col="date", y_col="sales", title="Category A Sales"
        )

        assert fig is not None
        assert fig.layout.title.text == "Category A Sales"
        assert len(fig.data[0].x) == len(category_a_data)

    def test_正常系_統計計算とデータ品質チェック(self) -> None:
        """統計計算とデータ品質チェックの統合テスト。"""
        df = load_sample_data()

        # 基本統計
        numeric_summary = df.describe()
        assert not numeric_summary.empty
        assert "sales" in numeric_summary.columns
        assert "profit" in numeric_summary.columns

        # データ品質チェック
        missing_values = df.isnull().sum()
        duplicates = df.duplicated().sum()

        # サンプルデータは完全であることを確認
        assert missing_values.sum() == 0
        assert duplicates == 0

        # データ型の確認
        expected_dtypes = {
            "sales": "int",
            "profit": "int",
            "customer_count": "int",
            "satisfaction": "float",
            "category": "object",
            "region": "object",
        }

        for col, expected_type in expected_dtypes.items():
            if expected_type == "int":
                assert pd.api.types.is_integer_dtype(df[col])
            elif expected_type == "float":
                assert pd.api.types.is_float_dtype(df[col])
            elif expected_type == "object":
                assert pd.api.types.is_object_dtype(df[col])

    def test_正常系_エクスポート機能の統合(self) -> None:
        """エクスポート機能の統合テスト。"""
        import io
        import json

        df = load_sample_data()

        # CSV エクスポート
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_content = csv_buffer.getvalue()

        assert len(csv_content) > 0
        assert "sales" in csv_content
        assert "profit" in csv_content

        # JSON エクスポート
        json_buffer = io.StringIO()
        df.to_json(json_buffer, orient="records", indent=2)
        json_content = json_buffer.getvalue()

        assert len(json_content) > 0
        parsed_json = json.loads(json_content)
        assert isinstance(parsed_json, list)
        assert len(parsed_json) == len(df)

        # サマリーエクスポート
        summary_data = {
            "overview": {
                "total_rows": len(df),
                "total_columns": len(df.columns),
                "memory_usage_kb": df.memory_usage(deep=True).sum() / 1024,
                "missing_values": df.isnull().sum().sum(),
            },
            "columns": df.dtypes.astype(str).to_dict(),
            "numeric_summary": df.describe().to_dict(),
        }

        assert summary_data["overview"]["total_rows"] == 100
        assert summary_data["overview"]["missing_values"] == 0
        assert len(summary_data["columns"]) == len(df.columns)

    def test_正常系_設定値との整合性チェック(self) -> None:
        """設定値とアプリケーション動作の整合性をチェック。"""
        config = AppConfig()
        df = load_sample_data()

        # アップロードサイズ制限の確認
        file_size_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
        assert file_size_mb < config.max_upload_size_mb

        # ファイル形式の確認
        supported_formats = config.allowed_file_formats
        assert "csv" in supported_formats
        assert "json" in supported_formats

        # レイアウト設定の確認
        assert config.layout in ["wide", "centered"]
        assert config.initial_sidebar_state in ["auto", "expanded", "collapsed"]

    def test_正常系_エラーハンドリングの統合(self) -> None:
        """エラーハンドリングの統合テスト。"""
        from python_coding_test.streamlit.components.charts import create_bar_chart

        # 空のDataFrameでのエラーハンドリング
        empty_df = pd.DataFrame()

        with pytest.raises(ValueError, match="Failed to create bar chart"):
            create_bar_chart(empty_df, x_col="nonexistent", y_col="also_nonexistent")

        # 存在しない列でのエラーハンドリング
        df = load_sample_data()

        with pytest.raises(ValueError, match="Failed to create bar chart"):
            create_bar_chart(df, x_col="nonexistent_column", y_col="sales")

    def test_正常系_パフォーマンス要件の確認(self) -> None:
        """パフォーマンス要件の確認テスト。"""
        import time

        # サンプルデータ生成のパフォーマンス
        start_time = time.time()
        df = load_sample_data()
        load_time = time.time() - start_time

        # 1秒以内でデータが生成されることを確認
        assert load_time < 1.0
        assert len(df) == 100

        # チャート作成のパフォーマンス
        from python_coding_test.streamlit.components.charts import create_bar_chart

        start_time = time.time()
        fig = create_bar_chart(df, x_col="date", y_col="sales")
        chart_time = time.time() - start_time

        # 2秒以内でチャートが作成されることを確認
        assert chart_time < 2.0
        assert fig is not None
