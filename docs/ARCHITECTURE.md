# AI Interior Design Platform - Architecture

## Overview

This platform provides AI-powered interior design leasing services, connecting clients with design solutions.

## Core Features

### 1. Design Management
- Browse available interior design templates
- AI-powered design recommendations
- Custom design generation

### 2. Leasing System
- Flexible leasing periods
- Automated pricing calculation
- Contract management

### 3. User Management
- Client accounts
- Designer portfolios
- Admin dashboard

## Technology Stack

- **Backend**: Node.js + TypeScript + Express
- **Testing**: Jest + Supertest
- **Code Quality**: ESLint + Prettier
- **Development**: VS Code with recommended extensions

## API Design

### REST Endpoints

```
GET  /               - API information
GET  /health         - Health check
GET  /api/designs    - List available designs
POST /api/designs    - Create new design (designer/admin)
GET  /api/designs/:id - Get design details
POST /api/leases     - Create lease
GET  /api/leases/:id - Get lease details
```

## Development Workflow

1. Open project in VS Code
2. Install recommended extensions
3. Run `npm install`
4. Start development server with `npm run dev`
5. Write code with auto-formatting on save
6. Debug using F5 in VS Code
7. Run tests before committing

## VS Code Features

- **IntelliSense**: Full TypeScript support
- **Debugging**: Breakpoints and step-through debugging
- **Tasks**: Quick access to build, test, and lint
- **Extensions**: Auto-formatting, linting, and GitHub Copilot

## Future Enhancements

- Database integration (PostgreSQL/MongoDB)
- AI model integration for design generation
- Real-time collaboration features
- Payment processing
- Mobile app development
