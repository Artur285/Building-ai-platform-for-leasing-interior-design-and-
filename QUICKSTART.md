# Quick Start Guide

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd Building-ai-platform-for-leasing-interior-design-and-
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python main.py
```

The server will start on `http://localhost:5000`

## Using the Web Interface

Visit `http://localhost:5000` in your browser to access the interactive web interface.

### Features:

1. **Browse Materials** - View all available building materials and equipment
2. **AI Recommendations** - Get intelligent suggestions based on your project description
3. **Pricing Calculator** - Calculate optimized pricing with automatic discounts
4. **Material Search** - Find materials by name, category, or description

## Using the API

### Get Health Status
```bash
curl http://localhost:5000/api/health
```

### Browse All Materials
```bash
curl http://localhost:5000/api/materials
```

### Search Materials by Category
```bash
curl "http://localhost:5000/api/materials?category=Scaffolding"
```

### Get AI Recommendations
```bash
curl -X POST http://localhost:5000/api/recommendations/project \
  -H "Content-Type: application/json" \
  -d '{
    "project_description": "Building a 5-story residential complex",
    "project_type": "Residential Construction",
    "top_n": 5
  }'
```

### Calculate Optimized Pricing
```bash
curl -X POST http://localhost:5000/api/pricing/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "material_id": 1,
    "lease_duration_days": 90,
    "quantity": 100
  }'
```

### Create a User
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "company_name": "Construction Co.",
    "phone": "+1-555-0123"
  }'
```

### Create a Lease
```bash
curl -X POST http://localhost:5000/api/leases \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "project_name": "Office Building",
    "project_description": "5-story commercial building",
    "start_date": "2024-02-01",
    "end_date": "2024-05-01",
    "delivery_address": "123 Main St",
    "items": [
      {"material_id": 1, "quantity": 50},
      {"material_id": 2, "quantity": 25}
    ]
  }'
```

## Running Examples

We provide a comprehensive examples script:

```bash
python examples.py
```

This will demonstrate all major features of the platform.

## Discount Structure

The AI automatically calculates discounts based on:

### Duration Discounts
- 7+ days: 5% discount
- 30+ days: 10% discount
- 90+ days: 20% discount

### Quantity Discounts
- 20+ units: 5% discount
- 50+ units: 10% discount
- 100+ units: 15% discount

**Maximum combined discount: 30%**

## Material Categories

- Formwork
- Scaffolding
- Heavy Equipment
- Power Equipment
- Concrete Equipment
- Access Equipment
- Safety Equipment
- Power Tools
- Lighting Equipment
- Structural Materials
- Insulation
- Site Security
- Interior Finish
- Material Handling

## Testing

Run the test suite:
```bash
python test_api.py
```

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify `main.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Use different port
```

### Database Issues
Delete the database and restart:
```bash
rm materials_leasing.db
python main.py
```

## Support

For issues or questions, please open an issue in the repository.
