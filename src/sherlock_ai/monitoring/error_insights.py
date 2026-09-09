from __future__ import annotations

import asyncio
import functools
import logging
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, ClassVar, TypeVar

from ..storage import MongoManager
from .utils import generate_error_insights

# Type variable for better type hints
F = TypeVar("F", bound=Callable[..., Any])

logger = logging.getLogger("ErrorInsightsLogger")

mongo_manager = MongoManager()

# C-4 FIX: Shared bounded executor for fire-and-forget background tasks.
# Avoids creating a new ThreadPoolExecutor on every error (H-8).
_bg_executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="sherlock_err")


def _run_analysis_and_save(func_name: str, error_message: str, stack: str) -> None:
    """
    Blocking helper: calls LLM and saves to MongoDB.
    Designed to be run in a background thread so it never blocks the caller.
    """
    probable_cause = generate_error_insights(error_message, stack)
    log_entry = {
        "function_name": func_name,
        "error_message": error_message,
        "stack_trace": stack,
        "probable_cause": probable_cause,
    }
    # add time.sleep to delay for debugging
    mongo_manager.save(log_entry, "error-insights")
    logger.info(probable_cause)


def sherlock_error_handler(func: F = None) -> F | Callable[[F], F]:
    def decorator(f: F) -> F:
        @functools.wraps(f)
        async def async_wrapper(*args, **kwargs):
            try:
                return await f(*args, **kwargs)

            except Exception as e:
                # Pre-register so SherlockErrorCaptureHandler doesn't double-capture this
                SherlockErrorCaptureHandler._captured_ids.add(id(e))

                error_message = str(e)
                stack = traceback.format_exc()

                # This logs at ERROR level → root logger → writes to errors.json automatically
                logging.getLogger().exception(
                    f"Unhandled exception in {f.__name__}: {error_message}"
                )

                # C-4 FIX: Run the blocking LLM call + MongoDB save in a thread pool
                # so the async event loop is never frozen.
                asyncio.get_event_loop().run_in_executor(
                    _bg_executor,
                    _run_analysis_and_save,
                    f.__name__,
                    error_message,
                    stack,
                )

        @functools.wraps(f)
        def sync_wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:

                # Pre-register so SherlockErrorCaptureHandler doesn't double-capture this
                SherlockErrorCaptureHandler._captured_ids.add(id(e))

                error_message = str(e)
                stack = traceback.format_exc()

                # This logs at ERROR level → root logger → writes to errors.json automatically
                logging.getLogger().exception(
                    f"Unhandled exception in {f.__name__}: {error_message}"
                )

                # C-4 FIX: Fire-and-forget the LLM + MongoDB work to background thread.
                # Sync callers don't block waiting for LLM response.
                _bg_executor.submit(
                    _run_analysis_and_save,
                    f.__name__,
                    error_message,
                    stack,
                )

        return async_wrapper if asyncio.iscoroutinefunction(f) else sync_wrapper

    return decorator(func) if func else decorator

class SherlockErrorCaptureHandler(logging.Handler):
    """
    Intercept ERROR-level log records and capture the active exception
    from sys.exc_info() - works even when the user doesn't re-raise
    """
    _captured_ids: ClassVar[set] = set()

    def __init__(self, level=logging.ERROR):
        super().__init__(level)

    def emit(self, record):
        if record.levelno < logging.ERROR:
            return

        exc_type, exc_value, exc_tb = sys.exc_info()
        if exc_type is None:
            return # no active exception in context, nothing to capture

        exc_id = id(exc_value)
        if exc_id in self._captured_ids:
            return # already captured this exception, nothing to do

        self._captured_ids.add(exc_id)

        error_message = str(exc_value)
        stack = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        func_name = record.funcName

        # C-4 FIX: emit() can be triggered from any async context (e.g. FastAPI
        # request handlers). Running the LLM + MongoDB work synchronously here
        # would block that context for 1-5s. Fire-and-forget to the bg executor.
        _bg_executor.submit(
            _run_analysis_and_save,
            func_name,
            error_message,
            stack,
        )