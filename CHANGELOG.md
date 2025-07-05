# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Future enhancements and features will be listed here

### Changed
- Future changes will be documented here

### Fixed
- Future fixes will be documented here

## [1.2.0] - 2025-01-02

### Added
- **Memory and Resource Monitoring**: Comprehensive monitoring system for tracking system resources
- **Memory Monitoring Decorator**: `@monitor_memory` decorator for tracking Python memory usage with tracemalloc integration
- **Resource Monitoring Decorator**: `@monitor_resources` decorator for tracking CPU, memory, I/O, and network usage
- **Modular Architecture**: Reorganized monitoring functionality into focused modules for better maintainability
- **Context Managers**: 
  - `MemoryTracker` for monitoring memory usage in code blocks
  - `ResourceTracker` for comprehensive resource monitoring in code blocks
- **Advanced Resource Tracking**:
  - CPU utilization monitoring
  - Memory usage (RSS, VMS) tracking
  - Disk I/O operations monitoring
  - Network I/O operations monitoring (optional)
  - Thread count and file handle tracking
- **ResourceMonitor Utility**: Comprehensive utility class for capturing and analyzing resource snapshots
- **Data Classes**: 
  - `ResourceSnapshot` for system resource snapshots
  - `MemorySnapshot` for memory usage snapshots
- **Flexible Configuration Options**:
  - Configurable minimum duration thresholds
  - Optional I/O and network monitoring
  - Tracemalloc integration for detailed memory tracking
  - Customizable log levels

### Changed
- **Modular Package Structure**: Reorganized monitoring functionality into separate focused modules:
  - `monitoring/snapshots.py` - Data classes for resource snapshots
  - `monitoring/resource_monitor.py` - Resource monitoring utilities
  - `monitoring/decorators.py` - Monitoring decorators
  - `monitoring/context_managers.py` - Context managers for code blocks
  - `monitoring/utils.py` - Logging utilities
- **Enhanced Package Dependencies**: Added `psutil>=5.8.0` for advanced system monitoring capabilities
- **Improved Logging**: Added `MonitoringLogger` for dedicated monitoring log output
- **Better API Organization**: Maintained backward compatibility while providing cleaner module structure

### Infrastructure
- **Dependency Management**: Added psutil for system-level resource monitoring
- **Type Safety**: Enhanced type hints throughout monitoring modules
- **Documentation**: Comprehensive docstrings for all monitoring functionality

## [1.1.4] - 2025-01-02

### Added
- Comprehensive testing improvements
- Enhanced package metadata for PyPI publication
- **PyPI Trusted Publishing**: Secure, token-less publishing setup using OpenID Connect (OIDC)
- **GitHub Actions Automation**: 
  - `publish.yml` workflow for automated PyPI publishing on releases
  - `release.yml` workflow for automatic GitHub release creation on version changes
- **CI/CD Pipeline**: Complete automation from version update to PyPI publication
- **Security Improvements**: Eliminated need for API token management through trusted publishing
- **Advanced Logging Configuration System**:
  - `LoggingConfig` dataclass for complete logging control
  - `LogFileConfig` class for individual log file configuration
  - `LoggerConfig` class for specific logger setup
  - Configuration presets: `minimal()`, `development()`, `production()`, `performance_only()`
  - Custom file naming and directory configuration
  - Dynamic log level and size configuration
- **Enhanced Package Structure**: 
  - `src/sherlock_ai/config/` module for configuration classes
  - Separated configuration logic from implementation
  - Clean import structure with backward compatibility
- **Configuration Presets**: Pre-built configurations for common use cases
- **Flexible Log Management**: 
  - Enable/disable individual log files
  - Custom log directories and filenames
  - Configurable rotation settings and backup counts
  - External library log level management
- **Enhanced Testing Suite**: Comprehensive tests for all configuration features
- **Logger Name Constants**: Added `LoggerNames` class for easy access to available logger names
- **Logger Discovery**: Added `list_available_loggers()` function to programmatically discover available loggers

### Changed
- **Publishing Workflow**: Migrated from manual PyPI uploads to automated trusted publishing
- **Release Process**: Streamlined release creation and package distribution
- **Logging Architecture**: Migrated to fully configurable logging system while maintaining backward compatibility
- **Package Organization**: Improved module structure with dedicated config package
- **File Organization**: Renamed `logging_config.py` to `logging_setup.py` for clearer purpose distinction
- **Logger Configuration**: Improved handler cleanup to prevent duplicate log entries during FastAPI development with reload=True

### Fixed
- **Performance Logger Configuration**: Fixed logger name mismatch between `performance.py` and logging configuration
- **Log File Population**: Resolved issue where performance logs weren't appearing in `performance.log`
- **Handler Duplication**: Fixed critical issue where FastAPI's reload feature caused duplicate log entries
- **Development Environment**: Resolved logging issues in development mode with auto-reload enabled

### Infrastructure
- Configured PyPI trusted publisher for secure authentication
- Implemented GitHub Actions workflows for continuous deployment
- Added automatic version detection and release tagging
- Enhanced security through OIDC-based authentication

## [0.1.0] - 2025-01-10

### Added
- **Performance Monitoring**: `@log_performance` decorator for tracking function execution times
- **Async/Sync Support**: Automatic detection and support for both synchronous and asynchronous functions
- **Context Manager**: `PerformanceTimer` class for monitoring code block execution
- **Logging Configuration**: `setup_logging()` function with structured log file organization
- **Request ID Tracking**: Built-in request ID support for distributed systems tracing
- **Manual Timing**: `log_execution_time()` function for manual performance tracking
- **Flexible Configuration**: 
  - Minimum duration thresholds
  - Configurable log levels
  - Optional argument logging
- **Multi-file Logging System**:
  - `app.log` - General application logs (INFO+)
  - `errors.log` - Error logs only (ERROR+)
  - `api.log` - API-related logs
  - `database.log` - Database operation logs
  - `services.log` - Service operation logs
  - `performance.log` - Performance monitoring logs
- **Zero Dependencies**: Pure Python implementation using only standard library
- **Type Hints**: Full type annotation support for better IDE integration
- **Structured Log Format**: Consistent performance log format with execution times and status
- **Helper Utilities**: Request ID management functions for context tracking
- **Comprehensive Documentation**: Detailed README with examples and API reference
- **MIT License**: Open source license for community use

### Features
- Performance decorator with customizable options (`min_duration`, `include_args`, `log_level`)
- Automatic async function detection and handling
- Context manager for timing arbitrary code blocks
- Request ID propagation through application context
- Rotating log files with size limits and backup counts
- Error handling and exception logging in performance metrics
- Clean API with sensible defaults

---

## Version History

- **1.0.0** - Initial release with core performance monitoring and logging functionality
- **1.0.1** - [Planned] Trusted publishing and automated CI/CD pipeline
- **1.1.0** - Advanced logging configuration system with dataclass-based config, presets, and flexible log management
- **1.1.4** - Enhanced logging setup with handler duplication fixes, logger name constants, and improved development experience 