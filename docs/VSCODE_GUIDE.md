# VS Code Quick Start Guide

## Opening the Project

1. **Open in VS Code**
   ```bash
   code .
   ```
   Or: File → Open Folder → Select the project directory

2. **Install Recommended Extensions**
   - When prompted, click "Install" to add recommended extensions
   - Or: View → Extensions → Click "Install All" in the recommendations section

## First Time Setup

1. **Install Dependencies**
   - Open integrated terminal: `Ctrl+` ` (backtick) or Terminal → New Terminal
   - Run: `npm install`

2. **Copy Environment File**
   ```bash
   cp .env.example .env
   ```

3. **Build the Project**
   - Press `Ctrl+Shift+B` (Windows/Linux) or `Cmd+Shift+B` (Mac)
   - Or run: `npm run build`

## Daily Development Workflow

### Running the Development Server

**Option 1: Using Terminal**
```bash
npm run dev
```

**Option 2: Using VS Code Tasks**
- Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
- Type "Run Task"
- Select "npm: dev"

### Debugging

1. **Set Breakpoints**
   - Click in the gutter (left of line numbers) to add breakpoints

2. **Start Debugging**
   - Press `F5` or click Run → Start Debugging
   - Choose "Launch Program" configuration

3. **Debug Controls**
   - Continue: `F5`
   - Step Over: `F10`
   - Step Into: `F11`
   - Step Out: `Shift+F11`
   - Stop: `Shift+F5`

### Running Tests

**Option 1: Run All Tests**
```bash
npm test
```

**Option 2: Debug Tests**
- Press `F5` → Select "Run Tests"
- Set breakpoints in test files

**Option 3: Watch Mode**
```bash
npm run test:watch
```

### Code Quality

**Format on Save** - Already configured! Just save files with `Ctrl+S`

**Manual Formatting**
```bash
npm run format
```

**Linting**
```bash
npm run lint
npm run lint:fix  # Auto-fix issues
```

## VS Code Features Included

### IntelliSense
- Automatic code completion
- Parameter hints
- Type information
- Import suggestions

### Debugging
- Breakpoints
- Variable inspection
- Call stack navigation
- Watch expressions

### Tasks (Ctrl+Shift+B)
- Build: Compile TypeScript
- Test: Run Jest tests
- Lint: Check code quality
- Dev: Start development server

### Extensions
- **ESLint**: Real-time code quality checks
- **Prettier**: Automatic code formatting
- **TypeScript**: Enhanced TypeScript support
- **GitHub Copilot**: AI pair programming
- **Docker**: Container management (for future use)

## Keyboard Shortcuts

### General
- `Ctrl+P` / `Cmd+P`: Quick file open
- `Ctrl+Shift+P` / `Cmd+Shift+P`: Command palette
- `Ctrl+` ` : Toggle terminal
- `Ctrl+B` / `Cmd+B`: Toggle sidebar

### Editing
- `Alt+Up/Down`: Move line up/down
- `Ctrl+D` / `Cmd+D`: Select next occurrence
- `Ctrl+/` / `Cmd+/`: Toggle line comment
- `Alt+Shift+F`: Format document

### Navigation
- `F12`: Go to definition
- `Alt+F12`: Peek definition
- `Shift+F12`: Find all references
- `Ctrl+T` / `Cmd+T`: Go to symbol

## Troubleshooting

### "Cannot find module" errors
```bash
rm -rf node_modules package-lock.json
npm install
```

### TypeScript errors
```bash
npm run build
```

### Port already in use
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill
# Or change PORT in .env file
```

### ESLint not working
- Make sure ESLint extension is installed
- Reload VS Code: `Ctrl+Shift+P` → "Reload Window"

## Project Structure

```
.vscode/          # VS Code configuration
├── settings.json    # Editor settings
├── launch.json      # Debug configs
├── tasks.json       # Build tasks
└── extensions.json  # Recommended extensions

src/              # Source code
├── index.ts         # Entry point
└── types.ts         # Type definitions

tests/            # Test files
└── api.test.ts      # API tests

docs/             # Documentation
└── ARCHITECTURE.md  # Project architecture
```

## Next Steps

1. ✅ Install dependencies: `npm install`
2. ✅ Build the project: `npm run build`
3. ✅ Run tests: `npm test`
4. ✅ Start dev server: `npm run dev`
5. 📝 Start coding!

## Resources

- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Express.js Documentation](https://expressjs.com/)
- [Jest Documentation](https://jestjs.io/)
- [VS Code Tips & Tricks](https://code.visualstudio.com/docs/getstarted/tips-and-tricks)
