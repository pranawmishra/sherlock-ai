"""
Integration tests for SherlockAI setup, configuration, and logging infrastructure.
These tests exercise the full setup lifecycle including file creation and logger wiring.
"""

import logging
import pytest
# from pathlib import Path

from sherlock_ai import SherlockAI, get_logger, get_logging_stats
from sherlock_ai.config.logging import LoggingConfig, LoggingPresets, LogFileConfig#, LoggerConfig


# ── Fixtures ───────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def reset_sherlock_singleton():
    """Reset SherlockAI singleton and root logger handlers before every test
    to prevent state leakage between tests."""
    SherlockAI._instance = None
    logging.root.handlers.clear()
    yield
    # Cleanup after test
    SherlockAI._instance = None
    logging.root.handlers.clear()


@pytest.fixture
def tmp_config(tmp_path):
    """Return a LoggingConfig that writes to a pytest-managed temp directory."""
    return LoggingConfig(
        logs_dir=str(tmp_path / "logs"),
        auto_instrument=False,   # skip framework patching in unit-style integration tests
    )


@pytest.fixture
def configured_instance(tmp_config):
    """Return a fully set-up SherlockAI instance backed by tmp_path."""
    instance = SherlockAI(config=tmp_config)
    instance.setup()
    yield instance
    instance.cleanup()


# ── SherlockAI initialisation ──────────────────────────────────────────────────

class TestSherlockAIInit:
    def test_default_config_is_created_when_none_provided(self):
        instance = SherlockAI()
        assert isinstance(instance.config, LoggingConfig)

    def test_custom_config_is_stored(self, tmp_config):
        instance = SherlockAI(config=tmp_config)
        assert instance.config is tmp_config

    def test_is_configured_is_false_before_setup(self, tmp_config):
        instance = SherlockAI(config=tmp_config)
        assert instance.is_configured is False

    def test_handlers_dict_is_empty_before_setup(self, tmp_config):
        instance = SherlockAI(config=tmp_config)
        assert instance.handlers == {}


# ── SherlockAI.setup() ─────────────────────────────────────────────────────────

class TestSherlockAISetup:
    def test_setup_sets_is_configured_true(self, configured_instance):
        assert configured_instance.is_configured is True

    def test_setup_creates_logs_directory(self, tmp_config, tmp_path):
        instance = SherlockAI(config=tmp_config)
        instance.setup()
        assert (tmp_path / "logs").is_dir()
        instance.cleanup()

    def test_setup_returns_config(self, tmp_config):
        instance = SherlockAI(config=tmp_config)
        returned = instance.setup()
        assert returned is tmp_config
        instance.cleanup()

    def test_setup_creates_file_handlers_for_enabled_files(self, configured_instance):
        # All default log files are enabled — handlers should exist for each
        for key in configured_instance.config.log_files:
            if configured_instance.config.log_files[key].enabled:
                assert key in configured_instance.handlers, f"Missing handler for: {key}"

    def test_setup_creates_console_handler_when_enabled(self, configured_instance):
        assert "console" in configured_instance.handlers

    def test_setup_skips_console_handler_when_disabled(self, tmp_path):
        config = LoggingConfig(
            logs_dir=str(tmp_path / "logs"),
            console_enabled=False,
            auto_instrument=False,
        )
        instance = SherlockAI(config=config)
        instance.setup()
        assert "console" not in instance.handlers
        instance.cleanup()

    def test_setup_configures_performance_logger_no_propagation(self, configured_instance):
        perf_logger = logging.getLogger("PerformanceLogger")
        assert perf_logger.propagate is False

    def test_log_files_are_physically_created_on_disk(self, configured_instance, tmp_path):
        logs_dir = tmp_path / "logs"
        # At least the app log file should exist after setup (RotatingFileHandler creates it)
        log_files = list(logs_dir.glob("*.json"))
        assert len(log_files) > 0, "No log files were created on disk"


# ── SherlockAI.get_stats() ─────────────────────────────────────────────────────

class TestSherlockAIGetStats:
    def test_stats_contains_expected_keys(self, configured_instance):
        stats = configured_instance.get_stats()
        for key in ["is_configured", "handlers", "log_files", "logs_dir", "console_enabled", "format_type"]:
            assert key in stats, f"Missing stats key: {key}"

    def test_stats_is_configured_true_after_setup(self, configured_instance):
        assert configured_instance.get_stats()["is_configured"] is True

    def test_stats_handlers_list_is_not_empty(self, configured_instance):
        assert len(configured_instance.get_stats()["handlers"]) > 0

    def test_stats_log_files_matches_config(self, configured_instance):
        stats = configured_instance.get_stats()
        assert set(stats["log_files"]) == set(configured_instance.config.log_files.keys())

    def test_stats_logs_dir_matches_config(self, configured_instance, tmp_path):
        stats = configured_instance.get_stats()
        assert stats["logs_dir"] == str(tmp_path / "logs")


# ── SherlockAI.cleanup() ───────────────────────────────────────────────────────

class TestSherlockAICleanup:
    def test_cleanup_sets_is_configured_false(self, configured_instance):
        configured_instance.cleanup()
        assert configured_instance.is_configured is False

    def test_cleanup_empties_handlers_dict(self, configured_instance):
        configured_instance.cleanup()
        assert configured_instance.handlers == {}

    def test_cleanup_clears_root_handlers(self, configured_instance):
        configured_instance.cleanup()
        assert logging.root.handlers == []

    def test_cleanup_is_safe_to_call_twice(self, configured_instance):
        configured_instance.cleanup()
        configured_instance.cleanup()  # must not raise


# ── SherlockAI.reconfigure() ──────────────────────────────────────────────────

class TestSherlockAIReconfigure:
    def test_reconfigure_applies_new_config(self, configured_instance, tmp_path):
        new_config = LoggingConfig(
            logs_dir=str(tmp_path / "new_logs"),
            auto_instrument=False,
        )
        configured_instance.reconfigure(new_config)
        assert configured_instance.config is new_config
        assert configured_instance.is_configured is True
        configured_instance.cleanup()

    def test_reconfigure_creates_new_logs_directory(self, configured_instance, tmp_path):
        new_config = LoggingConfig(
            logs_dir=str(tmp_path / "reconfigured_logs"),
            auto_instrument=False,
        )
        configured_instance.reconfigure(new_config)
        assert (tmp_path / "reconfigured_logs").is_dir()
        configured_instance.cleanup()


# ── SherlockAI.get_instance() singleton ───────────────────────────────────────

class TestSherlockAISingleton:
    def test_get_instance_returns_sherlock_ai(self):
        instance = SherlockAI.get_instance()
        assert isinstance(instance, SherlockAI)

    def test_get_instance_returns_same_object_on_repeated_calls(self):
        a = SherlockAI.get_instance()
        b = SherlockAI.get_instance()
        assert a is b


# ── get_logger() helper ────────────────────────────────────────────────────────

class TestGetLogger:
    def test_returns_logger_instance(self):
        logger = get_logger("TestLogger")
        assert isinstance(logger, logging.Logger)

    def test_returns_logger_with_correct_name(self):
        logger = get_logger("MyService")
        assert logger.name == "MyService"

    def test_same_name_returns_same_logger(self):
        a = get_logger("SharedLogger")
        b = get_logger("SharedLogger")
        assert a is b


# ── get_logging_stats() helper ────────────────────────────────────────────────

class TestGetLoggingStats:
    def test_returns_dict(self):
        stats = get_logging_stats()
        assert isinstance(stats, dict)

    def test_contains_is_configured_key(self):
        stats = get_logging_stats()
        assert "is_configured" in stats


# ── Preset integration with setup ─────────────────────────────────────────────

class TestPresetIntegrationWithSetup:
    def test_minimal_preset_sets_up_without_error(self, tmp_path):
        config = LoggingPresets.minimal()
        config.logs_dir = str(tmp_path / "logs")
        config.auto_instrument = False
        instance = SherlockAI(config=config)
        instance.setup()
        assert instance.is_configured is True
        instance.cleanup()

    def test_performance_only_preset_sets_up_without_error(self, tmp_path):
        config = LoggingPresets.performance_only()
        config.logs_dir = str(tmp_path / "logs")
        config.auto_instrument = False
        instance = SherlockAI(config=config)
        instance.setup()
        assert instance.is_configured is True
        instance.cleanup()

    def test_custom_single_log_file_sets_up_without_error(self, tmp_path):
        config = LoggingConfig(
            logs_dir=str(tmp_path / "logs"),
            log_files={"app": LogFileConfig(f"{tmp_path}/logs/app.log")},
            loggers={},
            auto_instrument=False,
        )
        instance = SherlockAI(config=config)
        instance.setup()
        assert "app" in instance.handlers
        instance.cleanup()