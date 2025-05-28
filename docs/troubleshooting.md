# Troubleshooting Guide

This guide helps you diagnose and resolve common issues with the Power Transformation Lab Scraper.

## Quick Diagnostics

### 1. Environment Check
```powershell
# Check Python version (should be 3.11+)
python --version

# Check installed packages
pip list | findstr "browser-use\|playwright\|openai"

# Verify Playwright installation
playwright --version
```

## Common Issues and Solutions

### Issue 1: `NotImplementedError` on Windows

**Symptoms:**
```
TypeError: an integer is required
NotImplementedError
Error during shutdown: ...
```

**Cause:** Windows asyncio event loop compatibility issues

**CURRENTLY A KNOWN BUG** but does not affect the scraper, just the resource cleaning at the end of the scraping job


## Getting Additional Help

### 1. Check Documentation
- [`README.md`](../README.md): Main documentation
- [`docs/profile-configuration.md`](profile-configuration.md): Profile setup
- [`docs/custom-templates.md`](custom-templates.md): Template creation

### 2. Examine Results
- Check `results/` directory for trace files
- Review screenshots for navigation issues
- Analyze extracted data for accuracy

### 3. Test with Simple Cases
- Start with a simple, known website
- Use basic extraction prompts


This troubleshooting guide should help you resolve most common issues. For persistent problems, enable debug mode and examine the detailed logs for specific error patterns.
