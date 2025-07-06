"""Tests for Streamlit app configuration."""

import pytest

from python_coding_test.streamlit.config import AppConfig


class TestAppConfig:
    """Test AppConfig class."""

    def test_正常系_デフォルト値で初期化される(self) -> None:
        """デフォルト値でAppConfigが作成されることを確認。"""
        config = AppConfig()

        assert config.title == "Python Coding Test - Streamlit App"
        assert config.page_title == "Python Coding Test"
        assert config.page_icon == "📊"
        assert config.layout == "wide"
        assert config.initial_sidebar_state == "expanded"
        assert config.log_level == "INFO"
        assert config.max_upload_size_mb == 200
        assert config.allowed_file_formats == ["csv", "json"]

    def test_正常系_カスタム値で初期化される(self) -> None:
        """カスタム値でAppConfigが作成されることを確認。"""
        config = AppConfig(
            title="Custom App",
            max_upload_size_mb=100,
            allowed_file_formats=["json", "xlsx"],
            layout="centered",
        )

        assert config.title == "Custom App"
        assert config.max_upload_size_mb == 100
        assert config.allowed_file_formats == ["json", "xlsx"]
        assert config.layout == "centered"

    def test_正常系_allowed_file_formatsがNoneの場合デフォルト値が設定される(
        self,
    ) -> None:
        """allowed_file_formatsがNoneの場合、デフォルト値が設定されることを確認。"""
        config = AppConfig(allowed_file_formats=None)

        assert config.allowed_file_formats == ["csv", "json"]

    def test_正常系_テーマ色が正しく設定される(self) -> None:
        """テーマ色が正しく設定されることを確認。"""
        config = AppConfig()

        assert config.theme_primary_color == "#FF6B6B"
        assert config.theme_background_color == "#FFFFFF"
        assert config.theme_secondary_background_color == "#F0F2F6"
        assert config.theme_text_color == "#262730"

    def test_正常系_カスタムテーマ色で初期化される(self) -> None:
        """カスタムテーマ色で初期化されることを確認。"""
        config = AppConfig(
            theme_primary_color="#FF0000",
            theme_background_color="#000000",
        )

        assert config.theme_primary_color == "#FF0000"
        assert config.theme_background_color == "#000000"
