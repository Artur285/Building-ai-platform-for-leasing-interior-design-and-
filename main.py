"""Main Flask application for AI Building Materials Leasing Platform."""
from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from app.models import db
from app.routes import api, _update_recommender


def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__, static_folder='static')
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(api, url_prefix='/api')
    
    # Route for serving the web interface
    @app.route('/')
    def index():
        return send_from_directory('static', 'index.html')
    
    # Create database tables and initialize data
    with app.app_context():
        db.create_all()
        _initialize_sample_data()
        _update_recommender()
    
    return app


def _initialize_sample_data():
    """Initialize the database with sample materials if empty."""
    from app.models import Material, User
    
    # Check if data already exists
    if Material.query.first():
        return
    
    # Sample building materials
    sample_materials = [
        {
            'name': 'Concrete Formwork Panels',
            'category': 'Formwork',
            'description': 'High-quality plywood formwork panels for concrete casting. Reusable and durable.',
            'unit': 'sqft',
            'price_per_day': 2.50,
            'quantity_available': 5000,
            'specifications': 'Size: 4x8 ft, Thickness: 18mm, Material: Marine plywood'
        },
        {
            'name': 'Steel Scaffolding System',
            'category': 'Scaffolding',
            'description': 'Modular steel scaffolding system for construction sites. Easy assembly.',
            'unit': 'set',
            'price_per_day': 15.00,
            'quantity_available': 200,
            'specifications': 'Height: up to 50ft, Load capacity: 2000 lbs, Material: Galvanized steel'
        },
        {
            'name': 'Construction Crane (Mobile)',
            'category': 'Heavy Equipment',
            'description': 'Mobile construction crane for lifting heavy materials and equipment.',
            'unit': 'unit',
            'price_per_day': 500.00,
            'quantity_available': 5,
            'specifications': 'Capacity: 20 tons, Reach: 100ft, Operator included'
        },
        {
            'name': 'Portable Generator',
            'category': 'Power Equipment',
            'description': 'Diesel-powered portable generator for construction site power needs.',
            'unit': 'unit',
            'price_per_day': 75.00,
            'quantity_available': 30,
            'specifications': 'Power: 50kW, Fuel: Diesel, Runtime: 12 hours per tank'
        },
        {
            'name': 'Cement Mixer (Industrial)',
            'category': 'Concrete Equipment',
            'description': 'Industrial cement mixer for large-scale concrete preparation.',
            'unit': 'unit',
            'price_per_day': 85.00,
            'quantity_available': 15,
            'specifications': 'Capacity: 500 liters, Power: Electric/Diesel, Output: 25 cubic meters/hour'
        },
        {
            'name': 'Aluminum Ladder (Extension)',
            'category': 'Access Equipment',
            'description': 'Heavy-duty aluminum extension ladder for construction work.',
            'unit': 'piece',
            'price_per_day': 12.00,
            'quantity_available': 100,
            'specifications': 'Max height: 40ft, Material: Aluminum, Weight capacity: 375 lbs'
        },
        {
            'name': 'Safety Barrier Fencing',
            'category': 'Safety Equipment',
            'description': 'Temporary safety barrier fencing for construction site perimeter.',
            'unit': 'panel',
            'price_per_day': 3.00,
            'quantity_available': 1000,
            'specifications': 'Size: 6x10 ft, Material: Steel mesh, Includes feet and couplers'
        },
        {
            'name': 'Excavator (Mini)',
            'category': 'Heavy Equipment',
            'description': 'Mini excavator for digging, trenching, and site preparation.',
            'unit': 'unit',
            'price_per_day': 350.00,
            'quantity_available': 8,
            'specifications': 'Weight: 5 tons, Dig depth: 10ft, Bucket capacity: 0.5 cubic yards'
        },
        {
            'name': 'Pneumatic Drill',
            'category': 'Power Tools',
            'description': 'Heavy-duty pneumatic drill for concrete and masonry work.',
            'unit': 'piece',
            'price_per_day': 25.00,
            'quantity_available': 50,
            'specifications': 'Type: Rotary hammer, Power: Pneumatic, Chuck size: 1 inch'
        },
        {
            'name': 'Construction Lighting Tower',
            'category': 'Lighting Equipment',
            'description': 'Mobile lighting tower for nighttime construction work.',
            'unit': 'unit',
            'price_per_day': 100.00,
            'quantity_available': 20,
            'specifications': 'Height: 30ft, Lights: 4x1000W LED, Power: Built-in generator'
        },
        {
            'name': 'Steel Reinforcement Bars (Rebar)',
            'category': 'Structural Materials',
            'description': 'High-strength steel reinforcement bars for concrete structures.',
            'unit': 'ton',
            'price_per_day': 5.00,
            'quantity_available': 500,
            'specifications': 'Grade: 60, Sizes: #3 to #10, Length: 20ft standard'
        },
        {
            'name': 'Insulation Boards (Rigid Foam)',
            'category': 'Insulation',
            'description': 'Rigid foam insulation boards for walls and roofs.',
            'unit': 'sqft',
            'price_per_day': 1.50,
            'quantity_available': 10000,
            'specifications': 'R-value: R-6 per inch, Thickness: 2 inches, Fire-rated'
        },
        {
            'name': 'Temporary Fencing Panels',
            'category': 'Site Security',
            'description': 'Chain-link temporary fencing for site security and boundary marking.',
            'unit': 'panel',
            'price_per_day': 4.00,
            'quantity_available': 800,
            'specifications': 'Size: 6x12 ft, Material: Galvanized chain-link, Includes bases'
        },
        {
            'name': 'Drywall Panels',
            'category': 'Interior Finish',
            'description': 'Standard drywall panels for interior wall construction.',
            'unit': 'sheet',
            'price_per_day': 1.00,
            'quantity_available': 3000,
            'specifications': 'Size: 4x8 ft, Thickness: 1/2 inch, Fire-resistant Type X available'
        },
        {
            'name': 'Forklift (Rough Terrain)',
            'category': 'Material Handling',
            'description': 'Rough terrain forklift for moving materials on construction sites.',
            'unit': 'unit',
            'price_per_day': 250.00,
            'quantity_available': 10,
            'specifications': 'Capacity: 5000 lbs, Lift height: 15ft, Fuel: Diesel'
        }
    ]
    
    # Create materials
    for mat_data in sample_materials:
        material = Material(**mat_data)
        db.session.add(material)
    
    # Create a sample user
    sample_user = User(
        username='demo_user',
        email='demo@example.com',
        company_name='Demo Construction Co.',
        phone='+1-555-0123'
    )
    db.session.add(sample_user)
    
    db.session.commit()
    print("Sample data initialized successfully!")


if __name__ == '__main__':
    import os
    app = create_app()
    print("=" * 60)
    print("AI Building Materials Leasing Platform")
    print("=" * 60)
    print("Server starting on http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  GET  /api/health - Health check")
    print("  GET  /api/materials - List all materials")
    print("  POST /api/recommendations/project - Get AI recommendations")
    print("  POST /api/pricing/optimize - Get optimized pricing")
    print("  POST /api/leases - Create a new lease")
    print("\nWeb Interface: http://localhost:5000")
    print("=" * 60)
    
    # Use debug mode from environment variable, default to False for production
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
