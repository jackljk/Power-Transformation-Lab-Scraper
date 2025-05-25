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

### 2. Configuration Validation
```powershell
# Test configuration loading
python -c "from app.utils.config_manager import config_manager; print('Config loaded successfully')"

# Check profile syntax
python -c "import yaml; yaml.safe_load(open('app/config/profiles/your_profile.yaml'))"
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

**Solution:**
This is automatically handled in the current version. If you still encounter issues:

1. **Update Python**: Ensure you're using Python 3.11 or higher
2. **Check Windows Version**: Windows 10/11 recommended
3. **Restart Terminal**: Close and reopen your terminal session

```powershell
# Force clean environment
$env:PYTHONPATH = ""
python main.py
```

### Issue 2: Playwright Installation Issues

**Symptoms:**
```
playwright: command not found
Browser executable not found
```

**Solutions:**

1. **Reinstall Playwright:**
   ```powershell
   pip uninstall playwright
   pip install playwright
   playwright install chromium
   ```

2. **Manual browser installation:**
   ```powershell
   # Install specific browser
   playwright install chromium --force
   
   # Install all browsers
   playwright install
   ```

3. **Permission Issues:**
   ```powershell
   # Run as administrator if needed
   Start-Process powershell -Verb runAs
   playwright install chromium
   ```

### Issue 3: OpenAI API Key Issues

**Symptoms:**
```
OpenAI API key not found
Authentication failed
Rate limit exceeded
```

**Solutions:**

1. **Check secrets.yaml:**
   ```yaml
   openai:
     api_key: "sk-your-actual-api-key"
   ```

2. **Verify API key:**
   ```powershell
   # Test API key
   python -c "from openai import OpenAI; client = OpenAI(api_key='your-key'); print('API key valid')"
   ```

3. **Environment variable:**
   ```powershell
   $env:OPENAI_API_KEY = "your-api-key"
   python main.py
   ```

### Issue 4: PDF Processing Errors

**Symptoms:**
```
PDF not found
Error reading PDF
Empty extraction results
```

**Solutions:**

1. **Check file path:**
   ```powershell
   # Verify file exists
   Test-Path "data/your-document.pdf"
   
   # Check file permissions
   Get-Acl "data/your-document.pdf"
   ```

2. **PDF format issues:**
   - Ensure PDF contains text (not just images)
   - Try with a simple text-based PDF first
   - Check if PDF is password-protected

3. **Dependencies:**
   ```powershell
   pip install --upgrade pymupdf4llm
   ```

### Issue 5: Bright Data MCP Connection Issues

**Symptoms:**
```
MCP connection failed
Authentication error
Proxy timeout
```

**Solutions:**

1. **Check credentials:**
   ```yaml
   # In secrets.yaml
   bright_data:
     username: "your-username"
     password: "your-password"
   ```

2. **Test connection:**
   ```powershell
   # Verify account status
   # Check Bright Data dashboard for account status
   ```

3. **Network issues:**
   ```powershell
   # Test basic connectivity
   Test-NetConnection brightdata.com -Port 443
   ```

### Issue 6: Memory and Performance Issues

**Symptoms:**
```
Out of memory
Slow extraction
Browser hanging
```

**Solutions:**

1. **Reduce browser steps:**
   ```yaml
   # In profile configuration
   scraper:
     additional_context:
       value: "Limit to essential actions only"
   ```

2. **Enable headless mode:**
   ```yaml
   # In browser_config.yaml
   browser:
     headless: true
   ```

3. **Close other applications:**
   ```powershell
   # Check memory usage
   Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 10
   ```

### Issue 7: Network and Timeout Errors

**Symptoms:**
```
Connection timeout
Network unreachable
SSL certificate error
```

**Solutions:**

1. **Increase timeouts:**
   ```yaml
   # In browser_config.yaml
   browser:
     timeout: 60000  # 60 seconds
   ```

2. **Check network:**
   ```powershell
   # Test URL accessibility
   Invoke-WebRequest -Uri "https://target-website.com" -Method Head
   ```

3. **SSL issues:**
   ```powershell
   # Disable SSL verification (for testing only)
   $env:PYTHONHTTPSVERIFY = "0"
   ```

## Debug Mode

Enable debug mode for detailed troubleshooting:

### Method 1: Environment Variable
```powershell
$env:DEBUG_MODE = "true"
python main.py
```

### Method 2: Configuration File
```yaml
# In local.yaml
debug_mode: true
```

### Method 3: Command Line
```powershell
python main.py --debug
```

### Debug Output Includes:
- Detailed step-by-step logs
- Screenshot captures
- Network request/response details
- Memory usage information
- Timing information

## Log Analysis

### Understanding Log Levels

1. **INFO**: Normal operation messages
2. **DEBUG**: Detailed execution information
3. **WARNING**: Potential issues that don't stop execution
4. **ERROR**: Serious problems that may cause failure

### Key Log Patterns

**Successful extraction:**
```
INFO - Scraping completed successfully
INFO - Results saved to results/profile_name/timestamp/
```

**Navigation issues:**
```
ERROR - Failed to navigate to URL
WARNING - Element not found
```

**API issues:**
```
ERROR - OpenAI API call failed
ERROR - Rate limit exceeded
```

## Performance Optimization

### 1. Browser-Use Scraper Optimization

```yaml
# Optimize for speed
scraper:
  scraper_type: "browser_use"
  
  initial_actions:
    - wait: 1000  # Reduce wait times
    # Remove unnecessary actions
  
  additional_context:
    value: "Extract quickly, focus on visible content only"
```

### 2. PDF Scraper Optimization

```yaml
# For large PDFs
scraper:
  scraper_type: "pdf_scraper"
  
  additional_context:
    value: "Focus on first 10 pages only for initial extraction"
```

### 3. Bright Data MCP Optimization

```yaml
# For high-volume scraping
scraper:
  scraper_type: "bright_data_mcp"
  
  additional_context:
    value: "Use fastest available proxy endpoints"
```

## Error Recovery

### Automatic Retry Logic

The scraper includes automatic retry for transient failures:

1. **Network timeouts**: Automatic retry with exponential backoff
2. **API rate limits**: Automatic waiting and retry
3. **Browser crashes**: Automatic browser restart

### Manual Recovery Steps

1. **Clean restart:**
   ```powershell
   # Kill any hanging processes
   Get-Process | Where-Object {$_.ProcessName -eq "chromium"} | Stop-Process -Force
   
   # Clear temporary files
   Remove-Item -Path "temp/*" -Recurse -Force
   
   # Restart scraper
   python main.py
   ```

2. **Reset configuration:**
   ```powershell
   # Backup current config
   Copy-Item "app/config/local.yaml" "app/config/local.yaml.backup"
   
   # Reset to defaults
   Copy-Item "app/config/local.yaml.example" "app/config/local.yaml"
   ```

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
- Gradually increase complexity

### 4. Community Support
- Create detailed issue reports
- Include log files and configuration
- Provide minimal reproduction cases

## Preventive Measures

### 1. Regular Maintenance
```powershell
# Update dependencies monthly
pip list --outdated
pip install --upgrade package-name

# Update Playwright browsers
playwright install --upgrade
```

### 2. Configuration Validation
```powershell
# Test configurations before production use
python -c "from app.utils.config.local import load_profile_config; load_profile_config()"
```

### 3. Monitoring
- Track extraction success rates
- Monitor for website changes
- Review error logs regularly

### 4. Backup
```powershell
# Backup important configurations
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
Copy-Item -Path "app/config" -Destination "backups/config_$timestamp" -Recurse
```

This troubleshooting guide should help you resolve most common issues. For persistent problems, enable debug mode and examine the detailed logs for specific error patterns.
