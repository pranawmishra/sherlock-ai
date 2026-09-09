from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field


@dataclass
class LogFileConfig:
    """Configuration for individual log files"""
    filename: str
    level: str | int = logging.INFO
    max_bytes: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    encoding: str = "utf-8"
    enabled: bool = True

@dataclass
class LoggerConfig:
    """Configuration for individual loggers"""
    name: str
    level: str | int = logging.INFO
    log_files: list[str] = field(default_factory=list)  # Which log files this logger writes to
    propagate: bool = True
    enabled: bool = True

@dataclass
class LoggingConfig:
    """Complete logging configuration"""

    auto_instrument: bool = True
    auto_trace_functions: bool = False
    auto_frameworks: list[str] = field(default_factory=lambda: ["fastapi"])
    auto_exclude_modules: list[str] = field(default_factory=lambda: ["sys", "os", "logging"])
    auto_min_duration: float = 0.0  # Only auto-log functions taking longer than this
    monitor_resources: bool = False
    monitor_memory: bool = False
    log_performance_enabled: bool = True
    performance_insights: bool = True
    
    # Directory settings
    logs_dir: str = "logs"
    
    # Format settings
    log_format: str = "%(asctime)s - %(request_id)s - %(name)s - %(levelname)s - %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    log_format_type: str = "json"
    
    # Console settings
    console_enabled: bool = True
    console_level: str | int = logging.INFO
    
    # Root logger settings
    root_level: str | int = logging.INFO
    
    # Log files configuration
    log_files: dict[str, LogFileConfig] = field(default_factory=dict)
    
    # Logger configuration
    loggers: dict[str, LoggerConfig] = field(default_factory=dict)
    
    # External library log levels
    external_loggers: dict[str, str | int] = field(default_factory=dict)

    def __post_init__(self):
        """Set up default configuration if not provided"""
        # Auto-expand log file paths for user convenience
        self._expand_log_file_paths()

        if not self.log_files:
            self.log_files = self._get_default_log_files()
        
        if not self.loggers:
            self.loggers = self._get_default_loggers()
            
        if not self.external_loggers:
            self.external_loggers = self._get_default_external_loggers()

    def _expand_log_file_paths(self):
        """Automatically expand base filenames to full paths using logs_dir and log_format_type"""
        file_extension = ".json" if self.log_format_type == "json" else ".log"
        
        for config in self.log_files.values():
            # Check if filename is just a base name (no directory separators)
            if not any(sep in config.filename for sep in ['/', '\\', os.path.sep]):
                # Expand to full path with proper extension if not already present
                config.filename = f"{self.logs_dir}/{config.filename}{file_extension}"

    def _get_default_log_files(self) -> dict[str, LogFileConfig]:
        """Default log files configuration"""

        # Choose file extension based on format type
        file_extension = ".json" if self.log_format_type == "json" else ".log"
        files = {
            "app": LogFileConfig(f"{self.logs_dir}/app{file_extension}"),
            "errors": LogFileConfig(f"{self.logs_dir}/errors{file_extension}", level=logging.ERROR),
            "performance": LogFileConfig(f"{self.logs_dir}/performance{file_extension}"),
            "error_insights": LogFileConfig(f"{self.logs_dir}/error_insights{file_extension}"),
            "performance_insights": LogFileConfig(f"{self.logs_dir}/performance_insights{file_extension}"),
        }
        # Only create monitoring file if memory or resource monitoring is enabled
        if self.monitor_memory or self.monitor_resources:
            files["monitoring"] = LogFileConfig(f"{self.logs_dir}/monitoring{file_extension}")

        return files

    def _get_default_loggers(self) -> dict[str, LoggerConfig]:
        """Default loggers configuration"""
        loggers = {
            "performance": LoggerConfig("PerformanceLogger", log_files=["performance"], propagate=False),
            "error_insights": LoggerConfig("ErrorInsightsLogger", log_files=["error_insights"], propagate=False),
            "performance_insights": LoggerConfig("PerformanceInsightsLogger", log_files=["performance_insights"], propagate=False),
        }
        # Add monitoring logger if monitoring is enabled
        if self.monitor_memory or self.monitor_resources:
            loggers["monitoring"] = LoggerConfig("MonitoringLogger", log_files=["monitoring"], propagate=False)
        
        return loggers

    def _get_default_external_loggers(self) -> dict[str, str | int]:
        """Default external library log levels"""
        return {
            "uvicorn": logging.INFO,
            "fastapi": logging.INFO,
        }