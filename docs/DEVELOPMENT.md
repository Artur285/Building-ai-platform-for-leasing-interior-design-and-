# Development Guide

## Setting Up Development Environment

### Prerequisites

Ensure you have the following installed:
- Python 3.8 or higher
- Node.js 16 or higher
- PostgreSQL 12 or higher
- Git

### Initial Setup

1. Clone the repository:
```bash
git clone https://github.com/Artur285/Building-ai-platform-for-leasing-interior-design-and-.git
cd Building-ai-platform-for-leasing-interior-design-and-
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Install Node.js dependencies:
```bash
npm install
```

5. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

6. Initialize the database:
```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

## Running the Application

### Development Mode

Start the Flask backend:
```bash
python app.py
```

In a separate terminal, start the frontend (if applicable):
```bash
npm run dev
```

The API will be available at `http://localhost:3000`

### Running Tests

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src tests/
```

Run specific test file:
```bash
pytest tests/test_validators.py
```

### Code Quality

Format code with Black:
```bash
black src/ tests/
```

Lint code with Flake8:
```bash
flake8 src/ tests/
```

## Project Structure

```
├── app.py              # Application entry point
├── requirements.txt    # Python dependencies
├── package.json        # Node.js dependencies
├── .env.example        # Example environment variables
├── src/                # Source code
│   ├── api/           # API routes
│   ├── ml/            # Machine learning models
│   ├── services/      # Business logic
│   └── utils/         # Utility functions
├── tests/             # Test files
├── docs/              # Documentation
├── config/            # Configuration files
└── data/              # Data files
```

## Development Workflow

1. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and commit:
```bash
git add .
git commit -m "Description of changes"
```

3. Run tests:
```bash
pytest
```

4. Push and create a pull request:
```bash
git push origin feature/your-feature-name
```

## Debugging

### Python Debugging

Use Python debugger (pdb):
```python
import pdb; pdb.set_trace()
```

Or use VS Code debugger with launch.json configuration.

### API Testing

Use curl or Postman to test API endpoints:
```bash
curl -X POST http://localhost:3000/api/design/recommendations \
  -H "Content-Type: application/json" \
  -d '{"space_type": "living_room", "style_preference": "modern", "budget": 5000, "dimensions": {"length": 20, "width": 15, "height": 10}}'
```

## Common Issues

### Database Connection Error
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env file
- Verify database credentials

### Import Errors
- Activate virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

### Port Already in Use
- Change PORT in .env file
- Or stop the process using the port

## Contributing

Please read [CONTRIBUTING.md](../CONTRIBUTING.md) for details on our development process and how to submit pull requests.
