# VS Code & Chrome Integration Guide

This guide explains how to use the AI Building Materials Leasing Platform with VS Code and Chrome browser integrations.

## VS Code Integration

### Getting Started

1. **Open in VS Code**
   ```bash
   code materials-leasing.code-workspace
   ```
   Or simply open the folder in VS Code.

2. **Install Recommended Extensions**
   When you open the project, VS Code will prompt you to install recommended extensions:
   - **Python** - Python language support
   - **Pylance** - Fast, feature-rich language support for Python
   - **REST Client** - Test REST APIs directly in VS Code
   - **Auto Close Tag** - Automatically close HTML/XML tags
   - **Auto Rename Tag** - Automatically rename paired HTML/XML tags
   - **Prettier** - Code formatter
   - **Black Formatter** - Python code formatter

3. **Set Up Virtual Environment**
   - Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
   - Type "Python: Create Environment"
   - Select "Venv"
   - Choose Python interpreter

### Debugging

#### Run/Debug the Flask Application

1. **Using Debug Panel**:
   - Open the Debug panel (`Ctrl+Shift+D` or `Cmd+Shift+D`)
   - Select "Python: Flask" from the dropdown
   - Press F5 or click the green play button

2. **Using Tasks**:
   - Press `Ctrl+Shift+P` / `Cmd+Shift+P`
   - Type "Tasks: Run Task"
   - Select "Start Flask Server"

#### Available Debug Configurations

- **Python: Flask** - Run the Flask server with debugging enabled
- **Python: Current File** - Debug the currently open Python file
- **Python: Run Tests** - Run the test suite
- **Python: Run Examples** - Execute the examples script

#### Breakpoints

1. Click in the gutter (left of line numbers) to set breakpoints
2. Run the Flask debugger
3. Make API requests using the REST Client or browser
4. Debugger will pause at breakpoints

### REST API Testing

The `api-tests.http` file contains pre-configured API requests.

#### Using REST Client Extension

1. Open `api-tests.http`
2. Click "Send Request" above any request
3. View response in a new panel

#### Example Requests Available

- **Health Check**: Test if the API is running
- **Materials CRUD**: Get, create, update materials
- **AI Recommendations**: Test project-based recommendations
- **Pricing Optimization**: Calculate optimized pricing
- **User & Lease Management**: Create users and leases

#### Customize Base URL

Change the `@baseUrl` variable at the top of `api-tests.http`:
```http
@baseUrl = http://localhost:5000
# or for production
@baseUrl = https://your-production-url.com
```

### Tasks

Press `Ctrl+Shift+P` / `Cmd+Shift+P` and type "Tasks: Run Task" to access:

- **Start Flask Server** - Run the application
- **Start Flask Server (Debug Mode)** - Run with FLASK_DEBUG=True
- **Run Tests** - Execute test suite
- **Run Examples** - Run example API calls
- **Install Dependencies** - Install packages from requirements.txt
- **Create Virtual Environment** - Set up new venv

### Code Formatting

Files are automatically formatted on save using:
- **Python**: Black formatter (88 char line length)
- **JavaScript/HTML**: Prettier

To manually format:
- `Shift+Alt+F` (Windows/Linux)
- `Shift+Option+F` (Mac)

### Integrated Terminal

- Open with `Ctrl+` ` (Windows/Linux) or `Cmd+` ` (Mac)
- Virtual environment activates automatically
- Run commands directly:
  ```bash
  python main.py
  python test_api.py
  python examples.py
  ```

## Chrome Integration

### Progressive Web App (PWA)

The platform can be installed as a desktop/mobile app in Chrome.

#### Installing the PWA

1. **Desktop (Chrome)**:
   - Visit `http://localhost:5000`
   - Look for the install icon (⊕) in the address bar
   - Click it and select "Install"
   - The app will open in its own window

2. **Mobile (Chrome/Android)**:
   - Visit the site in Chrome
   - Tap the menu (⋮) 
   - Select "Add to Home screen"
   - Confirm installation

3. **Alternative Method**:
   - Click the three-dot menu in Chrome
   - More tools → Create shortcut
   - Check "Open as window"

#### PWA Features

- **Offline Support**: Service worker caches key resources
- **Standalone Mode**: Runs in its own window without browser UI
- **Fast Loading**: Cached resources load instantly
- **Add to Home Screen**: Quick access from desktop/mobile
- **App-like Experience**: Feels like a native application

#### Service Worker

The service worker (`service-worker.js`) provides:
- **Caching Strategy**: Cache-first for static resources, network-first for API
- **Offline Fallback**: Access cached materials when offline
- **Background Sync**: Future support for background updates

### Chrome DevTools for Development

#### Network Tab
- Monitor API requests and responses
- Check service worker caching behavior
- View request/response headers

#### Application Tab
- **Manifest**: View PWA manifest details
- **Service Workers**: 
  - See registration status
  - Update or unregister service worker
  - Test offline mode with "Offline" checkbox
- **Storage**:
  - View cached resources
  - Clear cache storage
  - Inspect local/session storage

#### Console
- View service worker logs
- Debug JavaScript errors
- Test API calls with fetch()

### Testing PWA Features

1. **Test Installation**:
   ```javascript
   // In Chrome DevTools Console
   window.addEventListener('beforeinstallprompt', (e) => {
     console.log('Install prompt available');
   });
   ```

2. **Test Service Worker**:
   - Open Application → Service Workers
   - Check "Offline" to test offline functionality
   - Click "Update" to force service worker update

3. **Test Caching**:
   - Load the page
   - Open Network tab
   - Check "Disable cache"
   - Reload and observe which resources come from cache

### Browser Shortcuts

With the PWA installed:
- **Windows/Linux**: Find in Start Menu or Desktop
- **Mac**: Find in Applications folder
- **Mobile**: Icon on home screen

### Lighthouse Audit

Run a PWA audit in Chrome:
1. Open DevTools (F12)
2. Go to Lighthouse tab
3. Select "Progressive Web App"
4. Click "Analyze page load"
5. Review PWA score and recommendations

## Troubleshooting

### VS Code Issues

**Extensions not installing**:
- Open Extensions panel (`Ctrl+Shift+X`)
- Manually search and install each extension

**Python interpreter not found**:
- Press `Ctrl+Shift+P`
- Type "Python: Select Interpreter"
- Choose your virtual environment or system Python

**Debugger not starting**:
- Check virtual environment is activated
- Verify requirements are installed: `pip install -r requirements.txt`
- Check port 5000 is not in use

### Chrome/PWA Issues

**Install button not showing**:
- Ensure you're using HTTPS (or localhost)
- Check manifest.json is accessible
- Verify service worker registered successfully

**Service worker not updating**:
- Open Application → Service Workers
- Click "Update" or "Unregister"
- Hard refresh with `Ctrl+Shift+R` / `Cmd+Shift+R`

**Offline mode not working**:
- Check service worker is active
- Verify resources are cached in Application → Cache Storage
- Clear cache and reload if needed

## Best Practices

### VS Code Development

1. **Use Virtual Environment**: Always work within venv
2. **Enable Format on Save**: Keeps code consistent
3. **Use Breakpoints**: More efficient than print statements
4. **REST Client**: Test APIs without leaving VS Code
5. **Git Integration**: Use built-in source control panel

### Chrome Development

1. **DevTools Open**: Keep Application tab open during PWA development
2. **Clear Cache**: When testing service worker updates
3. **Lighthouse**: Run periodic audits
4. **Mobile Testing**: Use device emulation for responsive design
5. **Network Throttling**: Test under slow connections

## Additional Resources

### VS Code
- [Python in VS Code](https://code.visualstudio.com/docs/python/python-tutorial)
- [Debugging](https://code.visualstudio.com/docs/editor/debugging)
- [REST Client Extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)

### PWA
- [PWA Documentation](https://web.dev/progressive-web-apps/)
- [Service Workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [Web App Manifest](https://developer.mozilla.org/en-US/docs/Web/Manifest)

### Chrome DevTools
- [DevTools Overview](https://developer.chrome.com/docs/devtools/)
- [Application Panel](https://developer.chrome.com/docs/devtools/progressive-web-apps/)
- [Lighthouse](https://developer.chrome.com/docs/lighthouse/)
