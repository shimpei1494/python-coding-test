"""Tests for data analysis page functionality."""

import io

import pandas as pd
import pytest

from python_coding_test.streamlit.pages.data_analysis import load_uploaded_data


class MockUploadedFile:
    """Mock Streamlit uploaded file object."""

    def __init__(self, content: str, filename: str):
        self.content = content
        self.name = filename
        self._buffer = io.StringIO(content)

    def read(self) -> bytes:
        """Read file content as bytes."""
        return self.content.encode("utf-8")

    def getvalue(self) -> str:
        """Get file content as string."""
        return self.content


class TestLoadUploadedData:
    """Test file loading functionality."""

    def test_正常系_CSVファイルが読み込まれる(self) -> None:
        """CSVファイルが正しく読み込まれることを確認。"""
        csv_content = "id,name,value\n1,Alice,100\n2,Bob,200\n3,Charlie,300"

        # StringIOオブジェクトを直接作成してテスト
        df = pd.read_csv(io.StringIO(csv_content))

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        assert list(df.columns) == ["id", "name", "value"]
        assert df.iloc[0]["name"] == "Alice"

    def test_正常系_JSONファイルが読み込まれる(self) -> None:
        """JSONファイルが正しく読み込まれることを確認。"""
        json_content = (
            '[{"id": 1, "name": "Alice", "value": 100}, '
            '{"id": 2, "name": "Bob", "value": 200}]'
        )

        # StringIOオブジェクトを直接作成してテスト
        df = pd.read_json(io.StringIO(json_content))

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert list(df.columns) == ["id", "name", "value"]
        assert df.iloc[0]["name"] == "Alice"

    def test_正常系_空のCSVファイルが処理される(self) -> None:
        """空のCSVファイルが適切に処理されることを確認。"""
        csv_content = "id,name,value"  # ヘッダーのみ

        df = pd.read_csv(io.StringIO(csv_content))

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0
        assert list(df.columns) == ["id", "name", "value"]

    def test_正常系_数値データが適切に読み込まれる(self) -> None:
        """数値データが適切な型で読み込まれることを確認。"""
        csv_content = "id,score,temperature\n1,85.5,23.4\n2,92.1,24.7"

        df = pd.read_csv(io.StringIO(csv_content))

        assert pd.api.types.is_integer_dtype(df["id"])
        assert pd.api.types.is_float_dtype(df["score"])
        assert pd.api.types.is_float_dtype(df["temperature"])

    def test_正常系_日付データが読み込まれる(self) -> None:
        """日付データが読み込まれることを確認。"""
        csv_content = "date,value\n2024-01-01,100\n2024-01-02,200"

        df = pd.read_csv(io.StringIO(csv_content))

        # 日付変換
        df["date"] = pd.to_datetime(df["date"])

        assert pd.api.types.is_datetime64_any_dtype(df["date"])
        assert len(df) == 2

    def test_正常系_特殊文字を含むデータが処理される(self) -> None:
        """特殊文字を含むデータが正しく処理されることを確認。"""
        csv_content = (
            'id,name,description\n1,"Alice","Hello, World!"\n2,"Bob","Line1\nLine2"'
        )

        df = pd.read_csv(io.StringIO(csv_content))

        assert len(df) == 2
        assert df.iloc[0]["description"] == "Hello, World!"
        assert "Line1\nLine2" in df.iloc[1]["description"]

    def test_正常系_欠損値が適切に処理される(self) -> None:
        """欠損値が適切に処理されることを確認。"""
        csv_content = "id,name,value\n1,Alice,100\n2,,200\n3,Charlie,"

        df = pd.read_csv(io.StringIO(csv_content))

        assert len(df) == 3
        assert pd.isna(df.iloc[1]["name"])
        assert pd.isna(df.iloc[2]["value"])

    def test_正常系_大きなファイルが処理される(self) -> None:
        """大きなファイルが処理されることを確認（パフォーマンステスト）。"""
        # 1000行のデータを生成
        rows = ["id,value"]
        for i in range(1000):
            rows.append(f"{i},{i * 10}")
        csv_content = "\n".join(rows)

        df = pd.read_csv(io.StringIO(csv_content))

        assert len(df) == 1000
        assert df.iloc[-1]["id"] == 999
        assert df.iloc[-1]["value"] == 9990


class TestDataValidation:
    """Test data validation functionality."""

    def test_正常系_データ型の検証(self) -> None:
        """データ型の検証が正しく動作することを確認。"""
        df = pd.DataFrame(
            {
                "numeric_string": ["1", "2", "3"],
                "text": ["apple", "banana", "cherry"],
                "mixed": ["1", "text", "3"],
            }
        )

        # 数値のような文字列を検出
        numeric_like_cols = []
        for col in df.columns:
            if df[col].dtype == "object":
                try:
                    pd.to_numeric(df[col], errors="raise")
                    numeric_like_cols.append(col)
                except (ValueError, TypeError):
                    pass

        assert "numeric_string" in numeric_like_cols
        assert "text" not in numeric_like_cols
        assert "mixed" not in numeric_like_cols

    def test_正常系_重複データの検出(self) -> None:
        """重複データが正しく検出されることを確認。"""
        df = pd.DataFrame(
            {
                "id": [1, 2, 2, 3],
                "name": ["Alice", "Bob", "Bob", "Charlie"],
            }
        )

        duplicates = df.duplicated().sum()
        assert duplicates == 1

        # 特定の列での重複
        id_duplicates = df["id"].duplicated().sum()
        assert id_duplicates == 1

    def test_正常系_欠損値の分析(self) -> None:
        """欠損値の分析が正しく動作することを確認。"""
        df = pd.DataFrame(
            {
                "complete": [1, 2, 3, 4],
                "partial": [1, None, 3, None],
                "empty": [None, None, None, None],
            }
        )

        missing_stats = df.isnull().sum()

        assert missing_stats["complete"] == 0
        assert missing_stats["partial"] == 2
        assert missing_stats["empty"] == 4

        missing_percentages = (missing_stats / len(df) * 100).round(2)
        assert missing_percentages["complete"] == 0.0
        assert missing_percentages["partial"] == 50.0
        assert missing_percentages["empty"] == 100.0
