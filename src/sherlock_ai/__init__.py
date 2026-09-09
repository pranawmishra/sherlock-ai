"""
Sherlock AI - Your AI assistant package
"""

__version__ = "1.14.9"

# Import main components for easy access
from .analysis import CodeAnalyzer, hardcoded_value_detector
from .auto import enable_auto_instrumentation
from .config import LogFileConfig, LoggerConfig, LoggingConfig
from .logging_setup import SherlockAI, get_current_config, get_logger, get_logging_stats
from .monitoring import (
    MemoryTracker,
    PerformanceTimer,
    ResourceMonitor,
    ResourceTracker,
    log_performance,
    monitor_memory,
    monitor_resources,
)
from .utils import clear_request_id, get_request_id, set_request_id


# ✅ Logger name constants 
class LoggerNames:
    """Available logger names for use with get_logger()"""
    API = "ApiLogger"
    DATABASE = "DatabaseLogger"
    SERVICES = "ServiceLogger"
    PERFORMANCE = "PerformanceLogger"
    MONITORING = "MonitoringLogger"
    ERRORINSIGHTS = "ErrorInsightsLogger"
    PERFORMANCEINSIGHTS = "PerformanceInsightsLogger"
    AUTO_INSTRUMENTATION = "AutoInstrumentationLogger"
# ✅ Convenience function
def list_available_loggers():
    """Get list of all available logger names"""
    return [
        LoggerNames.API,
        LoggerNames.DATABASE,
        LoggerNames.SERVICES,
        LoggerNames.PERFORMANCE,
        LoggerNames.MONITORING,
        LoggerNames.ERRORINSIGHTS,
        LoggerNames.PERFORMANCEINSIGHTS,
        LoggerNames.AUTO_INSTRUMENTATION
    ]

__all__ = [
    "CodeAnalyzer",
    # "LoggingPresets",
    "LogFileConfig",
    "LoggerConfig",
    # Logger utilities
    "LoggerNames",
    "LoggingConfig",
    "MemoryTracker",
    "PerformanceTimer",
    "ResourceMonitor",
    "ResourceTracker",
    # Logging Configuration
    "SherlockAI",
    # Package info
    "__version__",
    "clear_request_id",
    # Auto-instrumentation
    "enable_auto_instrumentation",
    "get_current_config",
    # "sherlock_ai",
    "get_logger",
    "get_logging_stats",
    "get_request_id",
    # Analysis
    "hardcoded_value_detector",
    "list_available_loggers",
    # Performance Logging
    "log_performance",
    # Memory and Resource Monitoring
    "monitor_memory",
    "monitor_resources",
    # Request ID
    "set_request_id",
]