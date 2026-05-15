import logging
# import pytest
from sherlock_ai.config.logging import (
    LogFileConfig,
    LoggerConfig,
    LoggingConfig,
    LoggingPresets,
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
            "app", "errors", "api", "database",
            "services", "performance", "monitoring",
            "error_insights", "performance_insights", "auto_instrumentation",
        ]
        for key in expected:
            assert key in cfg.log_files, f"Missing log file key: {key}"

    def test_default_loggers_are_created(self):
        cfg = LoggingConfig()
        expected = [
            "api", "database", "services", "performance",
            "monitoring", "error_insights", "performance_insights",
            "auto_instrumentation",
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
        cfg.log_files["api"].enabled = False
        assert cfg.log_files["api"].enabled is False

    def test_mutating_console_level(self):
        cfg = LoggingConfig()
        cfg.console_level = "WARNING"
        assert cfg.console_level == "WARNING"


# ── LoggingPresets ─────────────────────────────────────────────────────────────

class TestLoggingPresets:
    def test_all_presets_return_logging_config(self):
        assert isinstance(LoggingPresets.minimal(), LoggingConfig)
        assert isinstance(LoggingPresets.development(), LoggingConfig)
        assert isinstance(LoggingPresets.production(), LoggingConfig)
        assert isinstance(LoggingPresets.performance_only(), LoggingConfig)
        assert isinstance(LoggingPresets.auto_instrument_all(), LoggingConfig)
        assert isinstance(LoggingPresets.auto_frameworks_only(), LoggingConfig)

    def test_minimal_has_only_app_log(self):
        cfg = LoggingPresets.minimal()
        assert list(cfg.log_files.keys()) == ["app"]
        assert cfg.loggers == {}

    def test_development_sets_debug_level(self):
        cfg = LoggingPresets.development()
        assert cfg.console_level == logging.DEBUG
        assert cfg.root_level == logging.DEBUG
        for file_cfg in cfg.log_files.values():
            assert file_cfg.level == logging.DEBUG

    def test_production_sets_warning_console_level(self):
        cfg = LoggingPresets.production()
        assert cfg.console_level == logging.WARNING

    def test_production_disables_api_and_services(self):
        cfg = LoggingPresets.production()
        assert cfg.log_files["api"].enabled is False
        assert cfg.log_files["services"].enabled is False

    def test_performance_only_has_single_log_file(self):
        cfg = LoggingPresets.performance_only()
        assert list(cfg.log_files.keys()) == ["performance"]
        assert list(cfg.loggers.keys()) == ["performance"]

    def test_custom_files_updates_filenames(self):
        cfg = LoggingPresets.custom_files({
            "app": "my_logs/application.log",
            "performance": "my_logs/perf.log",
        })
        assert cfg.log_files["app"].filename == "my_logs/application.log"
        assert cfg.log_files["performance"].filename == "my_logs/perf.log"

    def test_custom_files_ignores_unknown_keys(self):
        # Should not raise even if key doesn't exist in defaults
        cfg = LoggingPresets.custom_files({"nonexistent_key": "some/path.log"})
        assert isinstance(cfg, LoggingConfig)

    def test_auto_instrument_all_enables_tracing(self):
        cfg = LoggingPresets.auto_instrument_all()
        assert cfg.auto_instrument is True
        assert cfg.auto_trace_functions is True
        assert cfg.auto_min_duration > 0

    def test_auto_frameworks_only_disables_function_tracing(self):
        cfg = LoggingPresets.auto_frameworks_only()
        assert cfg.auto_instrument is True
        assert cfg.auto_trace_functions is False