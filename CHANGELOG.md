# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

### Changed
- **Publishing Workflow**: Migrated from manual PyPI uploads to automated trusted publishing
- **Release Process**: Streamlined release creation and package distribution
- **Logging Architecture**: Migrated to fully configurable logging system while maintaining backward compatibility
- **Package Organization**: Improved module structure with dedicated config package

### Fixed
- **Performance Logger Configuration**: Fixed logger name mismatch between `performance.py` and logging configuration
- **Log File Population**: Resolved issue where performance logs weren't appearing in `performance.log`

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