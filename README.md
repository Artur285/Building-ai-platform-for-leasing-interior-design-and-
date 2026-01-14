# AI Interior Design Platform

An AI-powered platform for leasing interior design services and solutions.

## 🚀 Quick Start

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn
- Visual Studio Code (recommended)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Building-ai-platform-for-leasing-interior-design-and-
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
```

4. Start the development server:
```bash
npm run dev
```

The server will start on `http://localhost:3000`

## 📁 Project Structure

```
.
├── .vscode/              # VS Code configuration
│   ├── settings.json     # Editor settings
│   ├── launch.json       # Debug configurations
│   ├── tasks.json        # Build tasks
│   └── extensions.json   # Recommended extensions
├── src/                  # Source files
│   ├── index.ts          # Application entry point
│   └── types.ts          # TypeScript type definitions
├── tests/                # Test files
│   └── api.test.ts       # API tests
├── docs/                 # Documentation
├── .eslintrc.js          # ESLint configuration
├── .prettierrc.json      # Prettier configuration
├── jest.config.js        # Jest configuration
├── tsconfig.json         # TypeScript configuration
└── package.json          # Project dependencies

```

## 🛠️ Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build the project for production
- `npm start` - Start the production server
- `npm test` - Run tests
- `npm run test:watch` - Run tests in watch mode
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Fix ESLint errors
- `npm run format` - Format code with Prettier

## 🔧 VS Code Setup

This project is configured to work seamlessly with Visual Studio Code.

### Recommended Extensions

When you open the project in VS Code, you'll be prompted to install recommended extensions:
- ESLint
- Prettier
- TypeScript
- Python (for AI features)
- GitHub Copilot
- Docker

### Debugging

Press `F5` or use the Debug panel to:
- Launch Program: Run the main application
- Attach to Process: Attach debugger to running process
- Run Tests: Execute tests with debugging

### Tasks

Access tasks via `Ctrl+Shift+B` (Windows/Linux) or `Cmd+Shift+B` (Mac):
- Build: Compile TypeScript
- Test: Run test suite
- Lint: Check code quality
- Dev: Start development server

## 🧪 Testing

Run tests:
```bash
npm test
```

Run tests with coverage:
```bash
npm test -- --coverage
```

## 📝 API Endpoints

- `GET /` - API information
- `GET /health` - Health check

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

ISC