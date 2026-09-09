"""
Modular monitoring package for Sherlock AI

This package provides decorators and context managers for monitoring:
- Memory usage (Python heap, RSS, VMS)
- CPU utilization
- Disk I/O operations
- Network I/O operations
- Process resource consumption
"""

# Import all public classes and functions
from .context_managers import MemoryTracker, ResourceTracker
from .error_insights import sherlock_error_handler
from .monitoring_insights import sherlock_performance_insights
from .performance import PerformanceTimer, log_performance
from .resource_decorators import monitor_memory, monitor_resources
from .resource_monitor import ResourceMonitor
from .snapshots import MemorySnapshot, ResourceSnapshot
from .utils import log_memory_usage, log_resource_usage

# Export public API
__all__ = [
    "MemorySnapshot",
    # Context managers
    "MemoryTracker",
    "PerformanceTimer",
    # Utility classes
    "ResourceMonitor",
    # Data classes
    "ResourceSnapshot",
    "ResourceTracker",
    # Utility functions
    "log_memory_usage",
    "log_performance",
    "log_resource_usage",
    # Decorators
    "monitor_memory",
    "monitor_resources",
    "sherlock_error_handler",
    "sherlock_performance_insights",
]