import asyncio
import time
import pytest
from unittest.mock import patch
from sherlock_ai.monitoring.performance import (
    log_performance,
    log_execution_time,
    PerformanceTimer,
)


# ── log_performance decorator ──────────────────────────────────────────────────

class TestLogPerformanceDecorator:
    def test_sync_function_returns_correct_value(self):
        @log_performance
        def add(a, b):
            return a + b

        assert add(2, 3) == 5

    def test_sync_function_preserves_name_and_docstring(self):
        @log_performance
        def my_func():
            """My docstring."""
            pass

        assert my_func.__name__ == "my_func"
        assert my_func.__doc__ == "My docstring."

    def test_sync_function_with_kwargs(self):
        @log_performance
        def greet(name="World"):
            return f"Hello, {name}!"

        assert greet(name="Alice") == "Hello, Alice!"

    def test_sync_function_reraises_exception(self):
        @log_performance
        def broken():
            raise ValueError("intentional error")

        with pytest.raises(ValueError, match="intentional error"):
            broken()

    def test_decorator_with_min_duration_still_returns_value(self):
        @log_performance(min_duration=0.0)
        def compute():
            return 42

        assert compute() == 42

    def test_decorator_with_include_args_false(self):
        @log_performance(include_args=False)
        def compute(x):
            return x * 2

        assert compute(10) == 20

    def test_decorator_with_log_level_debug(self):
        @log_performance(log_level="DEBUG")
        def compute():
            return "ok"

        assert compute() == "ok"

    def test_plain_decorator_wraps_sync(self):
        @log_performance
        def sync_fn():
            return "result"

        # Must not be a coroutine function since original is sync
        assert not asyncio.iscoroutinefunction(sync_fn)
        assert sync_fn() == "result"

    def test_async_wrapper_returned_for_async_function(self):
        @log_performance
        async def async_fn():
            return "async_result"

        assert asyncio.iscoroutinefunction(async_fn)

    def test_async_function_returns_correct_value(self):
        @log_performance
        async def async_add(a, b):
            return a + b

        result = asyncio.get_event_loop().run_until_complete(async_add(3, 4))
        assert result == 7

    def test_async_function_reraises_exception(self):
        @log_performance
        async def async_broken():
            raise RuntimeError("async error")

        with pytest.raises(RuntimeError, match="async error"):
            asyncio.get_event_loop().run_until_complete(async_broken())


# ── log_execution_time ─────────────────────────────────────────────────────────

class TestLogExecutionTime:
    def test_success_path_does_not_raise(self):
        start = time.time()
        # Should complete without error
        log_execution_time("test_op", start, success=True)

    def test_error_path_does_not_raise(self):
        start = time.time()
        log_execution_time("test_op", start, success=False, error="something failed")

    def test_calls_logger_info_on_success(self):
        start = time.time()
        with patch("sherlock_ai.monitoring.performance.logger") as mock_logger:
            log_execution_time("my_op", start, success=True)
            mock_logger.info.assert_called_once()
            call_args = mock_logger.info.call_args[0][0]
            assert "my_op" in call_args
            assert "SUCCESS" in call_args

    def test_calls_logger_error_on_failure(self):
        start = time.time()
        with patch("sherlock_ai.monitoring.performance.logger") as mock_logger:
            log_execution_time("my_op", start, success=False, error="boom")
            mock_logger.error.assert_called_once()
            call_args = mock_logger.error.call_args[0][0]
            assert "my_op" in call_args
            assert "ERROR" in call_args
            assert "boom" in call_args


# ── PerformanceTimer ───────────────────────────────────────────────────────────

class TestPerformanceTimer:
    def test_basic_usage_does_not_raise(self):
        with PerformanceTimer("test_block"):
            pass  # just verify no exception

    def test_does_not_suppress_exceptions(self):
        with pytest.raises(ZeroDivisionError):
            with PerformanceTimer("failing_block"):
                _ = 1 / 0

    def test_start_time_is_set_on_enter(self):
        timer = PerformanceTimer("op")
        assert timer.start_time is None
        with timer:
            assert timer.start_time is not None

    def test_min_duration_skips_logging_for_fast_ops(self):
        with patch("sherlock_ai.monitoring.performance.logger") as mock_logger:
            with PerformanceTimer("fast_op", min_duration=9999.0):
                pass
            mock_logger.info.assert_not_called()

    def test_logging_called_when_duration_exceeds_min(self):
        with patch("sherlock_ai.monitoring.performance.logger") as mock_logger:
            with PerformanceTimer("slow_op", min_duration=0.0):
                pass
            mock_logger.info.assert_called_once()
            call_args = mock_logger.info.call_args[0][0]
            assert "slow_op" in call_args
            assert "SUCCESS" in call_args