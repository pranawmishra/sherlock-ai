import functools
# import weakref
import sys
import traceback
# import inspect
from typing import Callable, TypeVar, Any
from typing import Union
from .utils import generate_error_insights
import logging
import asyncio
from ..storage import MongoManager#, api_client

# Type variable for better type hints
F = TypeVar("F", bound=Callable[..., Any])

logger = logging.getLogger("ErrorInsightsLogger")

mongo_manager = MongoManager()

def sherlock_error_handler(func: F = None) -> Union[F, Callable[[F], F]]:
    def decorator(f: F) -> F:
        @functools.wraps(f)
        async def async_wrapper(*args, **kwargs):
            try:
                return await f(*args, **kwargs)

            except Exception as e:
                error_message = str(e)
                stack = traceback.format_exc()

                # Call LLM to analyze the error:
                probable_cause = generate_error_insights(error_message, stack)

                # Prepare log entry:
                log_entry = {
                    "function_name": f.__name__,
                    "error_message": error_message,
                    "stack_trace": stack,
                    "probable_cause": probable_cause
                }

                # Save to MongoDB:
                mongo_manager.save(log_entry, "error-insights")
                # api_client.post_error_insights(log_entry)

                logger.info(probable_cause)
                # Re-raise or handle as needed
                # raise e

        @functools.wraps(f)
        def sync_wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                error_message = str(e)
                stack = traceback.format_exc()

                # Call LLM to analyze the error:
                probable_cause = generate_error_insights(error_message, stack)

                # Prepare log entry:
                log_entry = {
                    "function_name": f.__name__,
                    "error_message": error_message,
                    "stack_trace": stack,
                    "probable_cause": probable_cause
                }

                # Save to MongoDB:
                mongo_manager.save(log_entry, "error-insights")
                # api_client.post_error_insights(log_entry)
                logger.info(probable_cause)
                # Re-raise or handle as needed
                # raise e

        return async_wrapper if asyncio.iscoroutinefunction(f) else sync_wrapper

    return decorator(func) if func else decorator

class SherlockErrorCaptureHandler(logging.Handler):
    """
    Intercept ERROR-level log records and capture the active exception
    from sys.exc_info() - works even when the user doesn't re-raise
    """
    _captured_ids : set = set()

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
        probable_cause = generate_error_insights(error_message, stack)

        log_entry = {
            "function_name": record.funcName,
            "error_message": error_message,
            "stack_trace": stack,
            "probable_cause": probable_cause
        }

        mongo_manager.save(log_entry, "error-insights")
        logger.info(probable_cause)