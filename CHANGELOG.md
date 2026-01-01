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

## [1.12.0] - 2026-01-01

### Added
- **Performance Insights Logger**: New dedicated `PerformanceInsightsLogger` for better separation of performance insights logging
- **Logger Name Constant**: Added `PERFORMANCEINSIGHTS` constant to `LoggerNames` class for easier logger access

### Changed
- **Logger Organization**: Performance insights now use a dedicated logger separate from the general monitoring logger
- **Version Bump**: Updated package version to 1.12.0

### Improved
- **Logging Clarity**: Better separation of concerns with dedicated logger for performance insights
- **Developer Experience**: Easier to filter and manage performance insights logs separately from other monitoring logs

## [1.11.0] - 2026-01-01

### Added
- **GroqManager Class**: New centralized manager for Groq API client configuration and model management
- **Centralized Model Configuration**: Single source of truth for LLM model names with `DEFAULT_MODEL` and `ANALYSIS_MODEL` constants
- **Graceful Degradation**: Application now handles missing MONGO_URI and GROQ_API_KEY gracefully without crashing
- **User-Friendly Warnings**: Clear warning messages when optional services (MongoDB, Groq API) are not configured
- **Storage Module Enhancement**: Extended storage module to include both MongoDB and Groq API management

### Changed
- **MongoManager**: Enhanced to set collection attributes to None when MongoDB URI is missing, preventing AttributeError
- **Model Name Management**: Replaced hardcoded model names across codebase with centralized constants from GroqManager
- **API Client Initialization**: All Groq API calls now use centralized GroqManager instead of scattered initialization
- **Error Handling**: Improved error handling to provide graceful fallbacks when optional dependencies are unavailable
- **Code Organization**: Consolidated API configuration logic into storage module for better maintainability

### Improved
- **Developer Experience**: Clear, actionable warning messages guide users on how to configure optional services
- **Configuration Management**: Single place to update model names and API settings across entire application
- **Code Maintainability**: Eliminated duplicate API initialization code across multiple modules
- **Resilience**: Application continues to function with reduced features when optional services unavailable

### Fixed
- **MongoDB URI Missing**: Fixed AttributeError crash when MONGO_URI environment variable is not set
- **Groq API Key Missing**: Fixed crashes in code analysis and monitoring features when GROQ_API_KEY is missing
- **Warning Consistency**: Standardized warning format using Python's warnings module for both MongoDB and Groq

### Modified Files
- `src/sherlock_ai/storage/mongo_manager.py` - Added graceful handling and warnings for missing MongoDB URI
- `src/sherlock_ai/storage/groq_manager.py` - New file for centralized Groq API management
- `src/sherlock_ai/storage/__init__.py` - Export GroqManager class
- `src/sherlock_ai/monitoring/utils.py` - Use GroqManager and centralized model names
- `src/sherlock_ai/analysis/smart_check_code.py` - Use GroqManager and centralized model names
- `src/sherlock_ai/analysis/code_analyzer.py` - Use GroqManager and centralized model names

## [1.10.1] - 2025-12-25
- **API Client**: Removed SherlockAI API Functionality

## [1.10.0] - 2025-12-25

### Reverted
- **API Client Integration in Error Insights**: Reverted `@sherlock_error_handler` decorator to use MongoDB storage instead of API client
- **API Client Integration in Performance Insights**: Reverted `@sherlock_performance_insights` decorator to use MongoDB storage instead of API client
- **Storage Method**: Rolled back HTTP-based data ingestion to MongoDB-based local storage for error and performance insights

### Changed
- **Data Ingestion Method**: `@sherlock_error_handler` and `@sherlock_performance_insights` decorators now use MongoDB storage by default (reverted from v1.9.0)
- **Storage Architecture**: Restored MongoDB-based storage as the primary storage method for insights data

## [1.9.0] - 2025-10-15

### Added
- **API Client Integration**: New `ApiClient` class for HTTP-based data ingestion to centralized backend services
- **HTTP-Based Architecture**: Support for sending monitoring data via HTTP API calls instead of local storage
- **API Key Authentication**: Secure data transmission with API key authentication using `SHERLOCK_AI_API_KEY` environment variable
- **Configurable Endpoints**: Customizable API endpoints for different backend services
- **Dual Storage Support**: Ability to use both MongoDB and API client for hybrid storage solutions

### Changed
- **Data Ingestion Method**: `@sherlock_error_handler` and `@sherlock_performance_insights` decorators now use API client by default
- **Storage Architecture**: Migrated from MongoDB-only storage to HTTP-based centralized data ingestion
- **Configuration**: Added new environment variables for API client configuration
- **Dependencies**: Added `requests>=2.32.4` dependency for HTTP-based API client integration

### Improved
- **Scalability**: HTTP-based architecture enables better scalability for distributed monitoring systems
- **Centralized Management**: Monitoring data can now be sent to centralized backend services for better management
- **Flexibility**: Users can choose between MongoDB, API client, or both storage methods
- **Integration**: Seamless integration with existing decorators without code changes

### Infrastructure
- **Backend Integration**: Prepared foundation for centralized backend service integration
- **API Endpoints**: Defined standard API endpoints for error insights and performance insights ingestion
- **Environment Configuration**: Added support for configurable API base URLs and authentication

## [1.8.0] - 2025-08-30

### Added
- **Auto-Instrumentation**: Implemented Sentry-style zero-code auto-instrumentation for supported frameworks like FastAPI.
- **Framework Patcher**: Added a monkey-patching mechanism to automatically apply the full suite of monitoring decorators (`log_performance`, `monitor_memory`, `monitor_resources`, `sherlock_error_handler`) to framework routes at runtime.
- **Configuration Flag**: Introduced the `auto_instrument` boolean flag in `LoggingConfig` to easily enable or disable the auto-instrumentation feature.

### Changed
- **Initialization Logic**: The `SherlockAI.setup()` and `sherlock_ai()` functions now automatically trigger the auto-instrumentation process when the feature is enabled in the configuration.

### Improved
- **Developer Experience**: Drastically simplifies the setup for monitoring web applications by removing the need to manually add decorators to every endpoint.
- **Code Maintainability**: Reduces boilerplate code within user applications, leading to cleaner and more readable route definitions.

## [1.7.1] - 2025-08-24

### Added
- **AI-Powered Performance Insights**: New `@sherlock_performance_insights` decorator that uses an LLM to analyze performance bottlenecks and provide insights.
- **Intelligent Source Code Extraction**: The performance insights feature now intelligently extracts only user-defined function source code, excluding the monitoring decorators themselves for more accurate analysis.

### Changed
- **Performance Analysis**: Performance insights generation now uses a filtered function source to provide more relevant analysis to the user.
- **Documentation**: Updated `README.md` to include documentation for the new `@sherlock_performance_insights` decorator.

### Fixed
- **Performance Insights Bug**: Fixed a bug where `generate_performance_insights` was called with a function object instead of a function name and was being incorrectly awaited.
- **Decorator Source Code Inclusion**: Fixed an issue where the source code of the monitoring decorators was included in the performance analysis payload.

## [1.6.1] - 2025-07-27

### Added
- **Global Monitoring Decorator**: New `@global_monitor` decorator that can compose all monitoring decorators with configurable parameters
- **Convenience Monitoring Presets**: Added `@monitor_all`, `@monitor_critical`, `@monitor_performance_only`, and `@monitor_errors_only` decorators for common use cases
- **Flexible Monitoring Control**: Boolean flags to enable/disable individual monitoring types (memory, resources, performance, error_handling)
- **Global Parameter Overrides**: Global settings for `min_duration` and `log_level` that can override individual decorator settings
- **Comprehensive Configuration Options**: Per-decorator parameter configuration with intelligent defaults

### Fixed
- **Critical Variable Bug**: Fixed incorrect variable usage in `@sherlock_error_handler` decorator where `func.__name__` was used instead of `f.__name__`
- **Exception Handling Bug**: Fixed silently swallowed exceptions in error handler - exceptions are now properly re-raised after logging
- **Function Metadata Preservation**: Corrected `@functools.wraps` usage to properly preserve function metadata in error handler

### Changed
- **Monitoring Package Exports**: Updated `__init__.py` to export new global monitoring decorators and convenience functions
- **Decorator Composition**: Improved decorator composition order for optimal performance measurement accuracy
- **Error Handler Reliability**: Enhanced error handler to ensure exceptions are logged AND properly propagated to calling code

### Improved
- **User Experience**: Single decorator can now replace multiple individual monitoring decorators with fine-grained control
- **Code Maintainability**: Reduced boilerplate when applying multiple monitoring decorators to functions
- **Configuration Flexibility**: Centralized monitoring configuration with per-type customization options

## [1.6.0] - 2025-07-19

### Added
- **MongoDB Integration**: New `MongoManager` class for automatic error insights storage with MongoDB support
- **AI-Powered Error Analysis**: New `@sherlock_error_handler` decorator for automatic error analysis and insights
- **Error Insights Storage**: Automatic storage of error analysis results in MongoDB (sherlock-meta.error-insights collection)
- **Storage Module**: New `src/sherlock_ai/storage/` module for database and persistence management
- **LLM Error Analysis**: Integration with Groq API for AI-powered probable cause detection in errors
- **Async/Sync Error Handling**: Error handler decorator supports both synchronous and asynchronous functions
- **Automatic Error Logging**: Enhanced error logging with AI-generated insights and MongoDB persistence
- **Environment Configuration**: MongoDB connection via `MONGO_URI` environment variable with graceful fallback

### Changed
- **Package Structure**: Added new storage module for better organization of database-related functionality
- **Error Handling Architecture**: Enhanced error handling with AI analysis and persistent storage capabilities
- **Dependency Updates**: Added `pymongo>=4.10.1` for MongoDB integration

### Infrastructure
- **Database Architecture**: Prepared foundation for future vector database integration alongside MongoDB
- **Modular Storage Design**: Extensible storage architecture supporting multiple database backends
- **Error Insights Pipeline**: Complete pipeline from error detection to AI analysis to persistent storage

## [1.5.0] - 2025-07-17

### Added
- **Smart Code Analysis Decorator**: New `@smart_check` decorator for LLM-powered code review with suggestions for config management and type safety

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
- **1.5.0** - Smart code analysis decorator with LLM-powered code review, Groq API integration, and async/sync function support
- **1.6.0** - MongoDB integration, AI-powered error analysis with Groq API, enhanced error handling with storage capabilities
- **1.6.1** - Global monitoring decorator with composable decorators, critical bug fixes in error handler, improved decorator composition 
- **1.7.1** - AI-powered performance insights, intelligent source code extraction, and bug fixes for performance analysis. 
- **1.8.0** - Sentry style Auto-Instrumentation techniques to simplify and patch all the decoratos in background without need ing to add the decorator on each of the endpoint
- **1.9.0** - API Client Integration with HTTP-based data ingestion, centralized backend service support, and dual storage capabilities
- **1.10.0** - Reverted API Client integration in error and performance insights decorators, restored MongoDB as primary storage method
- **1.10.1** - Removed API Key functionality
- **1.11.0** - Centralized configuration management with GroqManager, graceful degradation for missing API keys, and improved error handling
- **1.12.0** - Added dedicated PerformanceInsightsLogger for better logging organization and separation of concerns