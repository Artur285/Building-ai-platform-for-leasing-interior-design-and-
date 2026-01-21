# AI Building Materials Leasing Platform

An intelligent platform for leasing building materials and equipment using AI-powered recommendations and pricing optimization.

## Features

### Core Functionality
- **Material Catalog Management**: Browse and search extensive inventory of building materials and equipment
- **Lease Management**: Create, track, and manage material leasing agreements
- **User Management**: Register users and track their leasing history

### AI-Powered Features
- **Project-Based Recommendations**: Get intelligent material suggestions based on project descriptions
- **Complementary Material Suggestions**: Discover related materials that complement your selections
- **Dynamic Pricing Optimization**: AI-driven discount calculations based on:
  - Lease duration (up to 20% discount for 3+ months)
  - Quantity (up to 15% discount for bulk orders)
  - Combined discounts (maximum 30%)
- **Smart Search**: Text-based similarity matching using TF-IDF and cosine similarity

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLAlchemy with SQLite
- **AI/ML**: scikit-learn for recommendation engine
- **API**: RESTful API with JSON responses

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

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

For development with debug mode enabled:
```bash
FLASK_DEBUG=True python main.py
```

The server will start on `http://localhost:5000`

## API Documentation

### Material Endpoints

#### Get All Materials
```
GET /api/materials
Query Parameters:
  - category: Filter by category
  - search: Search in name and description
```

#### Get Single Material
```
GET /api/materials/<material_id>
```

#### Create Material
```
POST /api/materials
Body: {
  "name": "Material Name",
  "category": "Category",
  "description": "Description",
  "unit": "piece/sqft/ton",
  "price_per_day": 10.50,
  "quantity_available": 100,
  "specifications": "Additional specs"
}
```

### AI Recommendation Endpoints

#### Get Project Recommendations
```
POST /api/recommendations/project
Body: {
  "project_description": "Building a 3-story residential complex",
  "project_type": "Residential Construction",
  "top_n": 5
}
```

#### Get Complementary Recommendations
```
POST /api/recommendations/complementary
Body: {
  "material_ids": [1, 3, 5],
  "top_n": 5
}
```

#### Optimize Pricing
```
POST /api/pricing/optimize
Body: {
  "material_id": 1,
  "lease_duration_days": 90,
  "quantity": 100
}
```

### Lease Endpoints

#### Create Lease
```
POST /api/leases
Body: {
  "user_id": 1,
  "project_name": "Downtown Office Building",
  "project_description": "5-story commercial building",
  "start_date": "2024-01-15",
  "end_date": "2024-04-15",
  "delivery_address": "123 Main St",
  "items": [
    {
      "material_id": 1,
      "quantity": 50
    }
  ]
}
```

#### Get Lease Details
```
GET /api/leases/<lease_id>
```

#### Get User Leases
```
GET /api/leases/user/<user_id>
```

#### Update Lease Status
```
PUT /api/leases/<lease_id>/status
Body: {
  "status": "active"  // pending, active, completed, cancelled
}
```

### User Endpoints

#### Create User
```
POST /api/users
Body: {
  "username": "john_doe",
  "email": "john@example.com",
  "company_name": "ABC Construction",
  "phone": "+1-555-0123"
}
```

## Sample Materials Catalog

The platform comes pre-loaded with 15 categories of building materials:
- Formwork panels
- Scaffolding systems
- Heavy equipment (cranes, excavators, forklifts)
- Power equipment (generators, tools)
- Concrete equipment
- Safety equipment
- Structural materials
- Insulation
- And more...

## AI Recommendation Engine

The platform uses a sophisticated AI engine that:

1. **Text Vectorization**: Converts material descriptions into numerical vectors using TF-IDF
2. **Similarity Matching**: Uses cosine similarity to find relevant materials
3. **Smart Discounting**: Calculates optimal pricing based on multiple factors
4. **Complementary Suggestions**: Recommends related materials from different categories

### Example Use Cases

1. **New Construction Project**
   - Submit project description: "Building a 10-story residential apartment"
   - Receive recommendations for scaffolding, formwork, cranes, safety equipment
   - Get optimized pricing for long-term lease

2. **Renovation Project**
   - Describe renovation scope
   - Get suggestions for specific materials needed
   - Discover complementary items you might have missed

3. **Bulk Equipment Rental**
   - Select multiple items
   - Receive automatic quantity discounts
   - Get recommendations for additional needed equipment

## Project Structure

```
.
├── main.py               # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── app/
│   ├── __init__.py       # App package initialization
│   ├── models.py         # Database models
│   ├── routes.py         # API endpoints
│   └── ai_engine.py      # AI recommendation engine
├── static/               # Static files (HTML, CSS, JS)
│   └── index.html        # Web interface
└── README.md            # This file
```

## Development

### Adding New Materials
Materials can be added via the API or directly through the database. Each material should include:
- Name and category
- Detailed description
- Unit of measurement
- Daily pricing
- Available quantity
- Technical specifications

### Extending the AI Engine
The recommendation engine can be enhanced by:
- Training on historical lease data
- Incorporating user preferences
- Adding seasonal pricing models
- Implementing demand forecasting

## Future Enhancements

- [ ] User authentication with JWT tokens
- [ ] Payment integration
- [ ] Real-time inventory tracking
- [ ] Mobile application
- [ ] Advanced analytics dashboard
- [ ] Machine learning model for demand prediction
- [ ] Automated maintenance scheduling
- [ ] Multi-language support

## License

MIT License

## Support

For issues, questions, or contributions, please open an issue in the repository.