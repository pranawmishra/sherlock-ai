import logging
# import pytest
from sherlock_ai.config.logging import (
    LogFileConfig,
    LoggerConfig,
    LoggingConfig,
)


# ── LogFileConfig ──────────────────────────────────────────────────────────────

class TestLogFileConfig:
    def test_defaults(self):
        cfg = LogFileConfig(filename="logs/app.json")
        assert cfg.filename == "logs/app.json"
        assert cfg.level == logging.INFO
        assert cfg.max_bytes == 10 * 1024 * 1024
        assert cfg.backup_count == 5
        assert cfg.encoding == "utf-8"
        assert cfg.enabled is True

    def test_custom_values(self):
        cfg = LogFileConfig(
            filename="logs/errors.json",
            level="ERROR",
            max_bytes=5 * 1024 * 1024,
            backup_count=3,
            enabled=False,
        )
        assert cfg.level == "ERROR"
        assert cfg.max_bytes == 5 * 1024 * 1024
        assert cfg.backup_count == 3
        assert cfg.enabled is False


# ── LoggerConfig ───────────────────────────────────────────────────────────────

class TestLoggerConfig:
    def test_defaults(self):
        cfg = LoggerConfig(name="ApiLogger")
        assert cfg.name == "ApiLogger"
        assert cfg.level == logging.INFO
        assert cfg.log_files == []
        assert cfg.propagate is True
        assert cfg.enabled is True

    def test_custom_values(self):
        cfg = LoggerConfig(
            name="PerformanceLogger",
            log_files=["performance"],
            propagate=False,
        )
        assert cfg.log_files == ["performance"]
        assert cfg.propagate is False


# ── LoggingConfig ──────────────────────────────────────────────────────────────

class TestLoggingConfig:
    def test_default_log_files_are_created(self):
        cfg = LoggingConfig()
        expected = [
            "app", "errors", "performance", "monitoring",
            "error_insights", "performance_insights",
        ]
        for key in expected:
            assert key in cfg.log_files, f"Missing log file key: {key}"

    def test_default_loggers_are_created(self):
        cfg = LoggingConfig()
        expected = [
            "performance", "monitoring", "error_insights", "performance_insights",
        ]
        for key in expected:
            assert key in cfg.loggers, f"Missing logger key: {key}"

    def test_default_attributes_exist(self):
        cfg = LoggingConfig()
        assert hasattr(cfg, "logs_dir")
        assert hasattr(cfg, "console_enabled")
        assert hasattr(cfg, "console_level")
        assert hasattr(cfg, "log_format_type")

    def test_default_logs_dir(self):
        cfg = LoggingConfig()
        assert cfg.logs_dir == "logs"

    def test_json_format_expands_paths_to_json(self):
        cfg = LoggingConfig(log_format_type="json")
        for file_cfg in cfg.log_files.values():
            assert file_cfg.filename.endswith(".json"), (
                f"Expected .json extension, got: {file_cfg.filename}"
            )

    def test_non_json_format_expands_paths_to_log(self):
        cfg = LoggingConfig(log_format_type="text")
        for file_cfg in cfg.log_files.values():
            assert file_cfg.filename.endswith(".log"), (
                f"Expected .log extension, got: {file_cfg.filename}"
            )

    def test_custom_logs_dir_is_reflected_in_paths(self):
        cfg = LoggingConfig(logs_dir="custom_logs")
        for file_cfg in cfg.log_files.values():
            assert file_cfg.filename.startswith("custom_logs/"), (
                f"Expected path to start with custom_logs/, got: {file_cfg.filename}"
            )

    def test_mutating_log_file_enabled_flag(self):
        cfg = LoggingConfig()
        cfg.log_files["app"].enabled = False
        assert cfg.log_files["app"].enabled is False

    def test_mutating_console_level(self):
        cfg = LoggingConfig()
        cfg.console_level = "WARNING"
        assert cfg.console_level == "WARNING"