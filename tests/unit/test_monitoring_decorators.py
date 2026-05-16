import asyncio
import pytest
from sherlock_ai.monitoring.resource_decorators import monitor_memory, monitor_resources


# ── monitor_memory ─────────────────────────────────────────────────────────────

class TestMonitorMemory:
    def test_sync_returns_correct_value(self):
        @monitor_memory
        def compute():
            return 99

        assert compute() == 99

    def test_sync_preserves_function_name(self):
        @monitor_memory
        def my_function():
            """Docstring."""
            pass

        assert my_function.__name__ == "my_function"
        assert my_function.__doc__ == "Docstring."

    def test_sync_reraises_exception(self):
        @monitor_memory
        def broken():
            raise ValueError("memory test error")

        with pytest.raises(ValueError, match="memory test error"):
            broken()

    def test_sync_with_arguments(self):
        @monitor_memory
        def add(a, b):
            return a + b

        assert add(3, 7) == 10

    def test_async_wrapper_returned_for_async_function(self):
        @monitor_memory
        async def async_fn():
            return "async"

        assert asyncio.iscoroutinefunction(async_fn)

    def test_async_returns_correct_value(self):
        @monitor_memory
        async def async_compute():
            return 42

        result = asyncio.get_event_loop().run_until_complete(async_compute())
        assert result == 42

    def test_async_reraises_exception(self):
        @monitor_memory
        async def async_broken():
            raise RuntimeError("async memory error")

        with pytest.raises(RuntimeError, match="async memory error"):
            asyncio.get_event_loop().run_until_complete(async_broken())

    def test_with_options_does_not_suppress_return_value(self):
        @monitor_memory(trace_malloc=False, min_duration=0.0)
        def fn():
            return "value"

        assert fn() == "value"


# ── monitor_resources ──────────────────────────────────────────────────────────

class TestMonitorResources:
    def test_sync_returns_correct_value(self):
        @monitor_resources
        def compute():
            return "resource_result"

        assert compute() == "resource_result"

    def test_sync_preserves_function_name(self):
        @monitor_resources
        def tracked_function():
            """Resource docstring."""
            pass

        assert tracked_function.__name__ == "tracked_function"
        assert tracked_function.__doc__ == "Resource docstring."

    def test_sync_reraises_exception(self):
        @monitor_resources
        def broken():
            raise TypeError("resource test error")

        with pytest.raises(TypeError, match="resource test error"):
            broken()

    def test_sync_with_arguments(self):
        @monitor_resources
        def multiply(a, b):
            return a * b

        assert multiply(4, 5) == 20

    def test_async_wrapper_returned_for_async_function(self):
        @monitor_resources
        async def async_fn():
            return "async"

        assert asyncio.iscoroutinefunction(async_fn)

    def test_async_returns_correct_value(self):
        @monitor_resources
        async def async_compute():
            return "async_resource"

        result = asyncio.get_event_loop().run_until_complete(async_compute())
        assert result == "async_resource"

    def test_async_reraises_exception(self):
        @monitor_resources
        async def async_broken():
            raise ValueError("async resource error")

        with pytest.raises(ValueError, match="async resource error"):
            asyncio.get_event_loop().run_until_complete(async_broken())

    def test_with_include_io_and_network_options(self):
        @monitor_resources(include_io=True, include_network=True)
        def fn():
            return "with_io_network"

        assert fn() == "with_io_network"

    def test_with_min_duration_still_returns_value(self):
        @monitor_resources(min_duration=0.0)
        def fn():
            return "min_duration_result"

        assert fn() == "min_duration_result"