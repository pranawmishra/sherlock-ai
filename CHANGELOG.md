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

## [1.4.1] - 2025-07-16

### Added
- **Simplified LogFileConfig**: Automatic path expansion for user convenience - specify base filenames instead of full paths
- **Smart Path Construction**: Auto-generates full paths using `logs_dir` and `log_format_type` from parent `LoggingConfig`
- **Flexible Configuration**: Support for both simplified base names and full custom paths when needed

### Changed
- **LogFileConfig Behavior**: Now automatically expands base filenames (e.g., `"app"`) to full paths (e.g., `"logs/app.json"`) when no directory separators are present
- **User Experience**: Significantly reduced configuration boilerplate by leveraging existing `logs_dir` and `log_format_type` settings
- **API Enhancement**: Enhanced `LoggingConfig.__post_init__()` to include automatic path expansion before default setup

### Fixed
- **Critical Bug**: Removed `format_type` parameter from `SherlockAI.setup()` method that was incorrectly overriding user's `LoggingConfig.log_format_type` setting
- **Configuration Override Issue**: Fixed bug where custom `LogFileConfig` settings were being ignored due to method parameter precedence
- **User Configuration Respect**: Ensured that user-provided configuration is the single source of truth without method parameter interference

### Improved
- **Developer Experience**: Users can now write `LogFileConfig("app")` instead of `LogFileConfig("logs/app.json")` 
- **DRY Principle**: Eliminated repetition of directory paths and file extensions in log configuration
- **Backward Compatibility**: Full custom paths still work unchanged for users who need complete control
- **Documentation**: Updated README.md with comprehensive examples showing both simplified and full path approaches

## [1.4.0] - 2025-07-16

### Added
- **JSON Format Logging**: New structured JSON output option for better log parsing and analysis
- **Format Type Parameter**: Added `format_type` parameter to `sherlock_ai()` function and `SherlockAI.setup()` method
- **JSONFormatter Class**: New formatter class for structured JSON log output with comprehensive metadata
- **NDJSON Support**: Newline-delimited JSON format for efficient log processing and streaming
- **Enhanced Log Metadata**: JSON logs include additional fields like module, function, line number, thread info, and process ID
- **Flexible File Extensions**: Automatic file extension selection (.log or .json) based on chosen format type
- **Code Analysis and Refactoring**: New automatic code analysis capabilities for detecting and refactoring hardcoded values
- **Hardcoded Value Detector**: `@hardcoded_value_detector` decorator for automatic detection and refactoring of hardcoded strings, numbers, and URLs
- **CodeAnalyzer Class**: Comprehensive code analysis class with AST parsing and LLM-powered constant naming
- **AST-Based Detection**: Uses Python's AST parser for accurate hardcoded value detection
- **Smart Constant Naming**: LLM-powered constant naming with heuristic fallback using Groq API
- **Automatic Constants Management**: Automatically creates and manages constants.py file with detected values

### Changed
- **Backward Compatibility**: Default behavior remains unchanged (standard .log format)
- **File Organization**: Log files now use appropriate extensions based on format type selection
- **Console Output**: Console logging always uses standard format for readability regardless of file format choice

### Improved
- **Log Processing**: JSON format enables better programmatic log analysis and integration with log processing tools
- **Debugging Information**: JSON logs provide richer context with function-level metadata
- **Tool Integration**: Better compatibility with modern log analysis tools and pipelines that expect structured data

## [1.3.0] - 2025-07-12

### Added
- **Class-Based Architecture**: New `SherlockAI` class for advanced logging management with instance-based configuration
- **Runtime Reconfiguration**: Ability to change logging settings without application restart using `reconfigure()` method
- **Context Manager Support**: Use `with SherlockAI()` syntax for automatic resource cleanup and temporary configurations
- **Singleton Pattern**: `SherlockAI.get_instance()` for shared application-wide logging instances
- **Logging Introspection**: New `get_logging_stats()` function to query current logging configuration and status
- **Enhanced Configuration Access**: New `get_current_config()` function to retrieve active logging configuration
- **Resource Management**: Proper cleanup of handlers and loggers with `cleanup()` method
<!-- - **Handler Information**: `get_handler_info()` method to inspect current logging handlers -->
<!-- - **Logger Information**: `get_logger_info()` method to inspect configured loggers -->
- **Framework Foundation**: Prepared architecture for future multi-tenant and database storage features
- **Instance Management**: Class-level instance tracking for future multi-tenant support

### Changed
- **Backward Compatibility**: All existing `sherlock_ai()` function calls continue to work unchanged
- **Function Implementation**: `sherlock_ai()` function now acts as a wrapper around the new class-based system
- **Configuration Storage**: Improved configuration storage and retrieval mechanism
- **Resource Cleanup**: Enhanced resource management with proper handler cleanup
- **API Consistency**: Maintained all existing APIs while adding new class-based functionality

### Improved
- **FastAPI Integration**: Better decorator order handling for FastAPI middleware
- **Memory Management**: Improved memory usage through better resource cleanup
- **Error Handling**: Enhanced error handling in configuration and setup processes
- **Performance**: Optimized initialization and configuration processes
- **Documentation**: Added comprehensive examples for both function and class usage patterns

### Fixed
- **Handler Duplication**: Improved prevention of duplicate log handlers during reconfiguration
- **Resource Leaks**: Fixed potential resource leaks through proper cleanup mechanisms
- **Configuration Persistence**: Fixed issues with configuration state management

### Infrastructure
- **Preparation for Multi-Tenant**: Laid groundwork for future multi-tenant logging support
- **Database Ready**: Prepared architecture for future database storage integration
- **Extensible Design**: Created extensible class structure for future framework features

## [1.2.0] - 2025-07-02

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

## [1.1.4] - 2025-07-02

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

## [0.1.0] - 2025-06-28

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

- **0.1.0** - Initial release with core performance monitoring and logging functionality
- **1.0.0** - First stable release with comprehensive performance monitoring
- **1.0.1** - [Planned] Trusted publishing and automated CI/CD pipeline
- **1.1.0** - Advanced logging configuration system with dataclass-based config, presets, and flexible log management
- **1.1.4** - Enhanced logging setup with handler duplication fixes, logger name constants, and improved development experience
- **1.2.0** - Memory and resource monitoring with comprehensive system tracking, modular architecture, and psutil integration
- **1.3.0** - Class-based architecture with SherlockAI class, runtime reconfiguration, and context manager support
- **1.4.0** - JSON format logging, code analysis and refactoring, hardcoded value detection with LLM-powered constant naming
- **1.4.1** - Simplified LogFileConfig with automatic path expansion, critical bug fixes for configuration override issues 