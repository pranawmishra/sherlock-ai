"""
Framework-specific auto-instrumentation patches
"""

# import functools
# import importlib
import sys
from ..monitoring import monitor_memory, monitor_resources, sherlock_error_handler, log_performance, sherlock_performance_insights

def patch_frameworks(frameworks, config):
    """Patch specified frameworks for auto-instrumentation"""
    for framework in frameworks:
        # print(f"Patching {framework}")
        if framework == "fastapi":
            patch_fastapi(config)


def patch_fastapi(config):
    """Auto-instrument FastAPI applications"""
    try:
        import fastapi
        if 'fastapi' in sys.modules:
            # print("FastAPI is installed")
            fastapi = sys.modules['fastapi']
            _patch_fastapi_app(fastapi, config)
    except ImportError:
        pass

def _patch_fastapi_app(fastapi, config):
    """Patch FastAPI route decorators"""

    # Guard: dont patch if already patched
    if getattr(fastapi.FastAPI, '_sherlock_patched', False): # type: ignore
        return
    
    original_get = fastapi.FastAPI.get
    original_post = fastapi.FastAPI.post
    original_put = fastapi.FastAPI.put
    original_delete = fastapi.FastAPI.delete
    
    def create_instrumented_method(original_method):
        def instrumented_method(self, path, **kwargs):
            def decorator(f):
                # Auto-apply sherlock monitoring
                f = sherlock_error_handler(f)
                if config.monitor_resources:
                    f = monitor_resources(f)
                if config.monitor_memory:
                    f = monitor_memory(f)
                if config.log_performance_enabled:
                    f = log_performance(f)
                if config.performance_insights:
                    f = sherlock_performance_insights(f)
                return original_method(self, path, **kwargs)(f)
            return decorator
        return instrumented_method
    
    fastapi.FastAPI.get = create_instrumented_method(original_get)
    fastapi.FastAPI.post = create_instrumented_method(original_post)
    fastapi.FastAPI.put = create_instrumented_method(original_put)
    fastapi.FastAPI.delete = create_instrumented_method(original_delete)
    fastapi.FastAPI._sherlock_patched = True # mark as patched