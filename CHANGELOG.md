# Changelog

All notable changes to the Power Transformation Lab Scraper will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation overhaul
- Multiple scraper type support (Browser-Use, Bright Data MCP, PDF)
- Profile-based configuration system
- Local tracing and result management
- Custom task template support
- Advanced troubleshooting guide

### Changed
- Improved Windows asyncio compatibility
- Enhanced error handling and recovery
- Restructured project documentation
- Optimized PDF processing with vector search

### Fixed
- Windows event loop issues
- Resource cleanup problems
- PDF extraction reliability
- Browser automation stability

## [2.0.0] - 2025-05-25

### Added
- **Multi-Scraper Architecture**: Support for three different scraping technologies
  - Browser-Use: AI-powered browser automation
  - Bright Data MCP: Proxy-based scraping with MCP
  - PDF Scraper: Document processing with vector search
- **Profile System**: YAML-based configuration profiles for reusable scraping tasks
- **Task Templates**: Specialized templates for different extraction scenarios
- **Local Tracing**: Comprehensive logging with screenshots and execution traces
- **Advanced Output Formatting**: Custom content structure definitions
- **Enhanced Error Handling**: Robust error recovery and debugging capabilities

### Changed
- **Configuration System**: Migrated to hierarchical YAML configuration
- **Project Structure**: Reorganized codebase for better maintainability
- **Documentation**: Complete documentation overhaul with examples and guides
- **Windows Compatibility**: Improved Windows asyncio event loop handling

### Fixed
- **Event Loop Issues**: Resolved Windows-specific asyncio problems
- **Resource Management**: Fixed memory leaks and resource cleanup
- **PDF Processing**: Enhanced PDF text extraction reliability
- **Browser Stability**: Improved browser automation stability

## [1.x.x] - Previous Versions

### Legacy Features
- Basic web scraping with browser-use
- Simple configuration system
- Basic output formatting
- Initial documentation

---

## Version Guidelines

### Version Number Format
- **Major (X.0.0)**: Breaking changes, major new features
- **Minor (0.X.0)**: New features, backwards compatible
- **Patch (0.0.X)**: Bug fixes, minor improvements

### Change Categories
- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Now removed features
- **Fixed**: Bug fixes
- **Security**: Vulnerability fixes

### Release Process
1. Update version number in relevant files
2. Update CHANGELOG.md with new version
3. Test all scraper types and configurations
4. Create git tag for release
5. Update documentation if needed

### Contributing to Changelog
When making changes:
1. Add entry to [Unreleased] section
2. Use appropriate category (Added, Changed, etc.)
3. Be specific and concise
4. Include breaking change notices
5. Reference issue numbers when applicable

Example entry format:
```
### Added
- New PDF batch processing feature (#123)
- Support for custom extraction templates
- Enhanced debug mode with step-by-step screenshots

### Fixed
- Browser timeout issues on slow networks (#456)
- PDF extraction failures with complex layouts (#789)
```
