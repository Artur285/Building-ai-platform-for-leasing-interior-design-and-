"""REST API routes for the Building Materials Leasing Platform."""
from flask import Blueprint, request, jsonify
from datetime import datetime, date
from app.models import db, Material, User, Lease, LeaseItem
from app.ai_engine import MaterialRecommender

api = Blueprint('api', __name__)

# Global recommender instance (will be initialized on app start)
recommender = MaterialRecommender()


@api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'message': 'AI Building Materials Leasing Platform'}), 200


@api.route('/materials', methods=['GET'])
def get_materials():
    """Get all materials with optional filtering."""
    category = request.args.get('category')
    search = request.args.get('search')
    
    query = Material.query
    
    if category:
        query = query.filter(Material.category == category)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            db.or_(
                Material.name.ilike(search_term),
                Material.description.ilike(search_term)
            )
        )
    
    materials = query.all()
    return jsonify([mat.to_dict() for mat in materials]), 200


@api.route('/materials/<int:material_id>', methods=['GET'])
def get_material(material_id):
    """Get a specific material by ID."""
    material = Material.query.get_or_404(material_id)
    return jsonify(material.to_dict()), 200


@api.route('/materials', methods=['POST'])
def create_material():
    """Create a new material."""
    data = request.get_json()
    
    material = Material(
        name=data.get('name'),
        category=data.get('category'),
        description=data.get('description'),
        unit=data.get('unit'),
        price_per_day=data.get('price_per_day'),
        quantity_available=data.get('quantity_available', 0),
        specifications=data.get('specifications', '')
    )
    
    db.session.add(material)
    db.session.commit()
    
    # Update recommender
    _update_recommender()
    
    return jsonify(material.to_dict()), 201


@api.route('/materials/<int:material_id>', methods=['PUT'])
def update_material(material_id):
    """Update an existing material."""
    material = Material.query.get_or_404(material_id)
    data = request.get_json()
    
    material.name = data.get('name', material.name)
    material.category = data.get('category', material.category)
    material.description = data.get('description', material.description)
    material.unit = data.get('unit', material.unit)
    material.price_per_day = data.get('price_per_day', material.price_per_day)
    material.quantity_available = data.get('quantity_available', material.quantity_available)
    material.specifications = data.get('specifications', material.specifications)
    
    db.session.commit()
    
    # Update recommender
    _update_recommender()
    
    return jsonify(material.to_dict()), 200


@api.route('/recommendations/project', methods=['POST'])
def recommend_for_project():
    """Get AI-powered material recommendations for a project."""
    data = request.get_json()
    
    project_description = data.get('project_description', '')
    project_type = data.get('project_type')
    top_n = data.get('top_n', 5)
    
    if not project_description:
        return jsonify({'error': 'project_description is required'}), 400
    
    # Get recommendations
    recommendations = recommender.recommend_by_project(
        project_description, 
        project_type, 
        top_n
    )
    
    # Format response
    result = []
    for material, score in recommendations:
        result.append({
            'material': material,
            'relevance_score': round(score, 3),
            'recommendation_reason': _generate_recommendation_reason(material, score)
        })
    
    return jsonify(result), 200


@api.route('/recommendations/complementary', methods=['POST'])
def recommend_complementary():
    """Get complementary material recommendations based on selected materials."""
    data = request.get_json()
    
    material_ids = data.get('material_ids', [])
    top_n = data.get('top_n', 5)
    
    if not material_ids:
        return jsonify({'error': 'material_ids is required'}), 400
    
    # Get recommendations
    recommendations = recommender.recommend_complementary(material_ids, top_n)
    
    # Format response
    result = []
    for material, score in recommendations:
        result.append({
            'material': material,
            'relevance_score': round(score, 3)
        })
    
    return jsonify(result), 200


@api.route('/pricing/optimize', methods=['POST'])
def optimize_pricing():
    """Calculate optimized pricing with AI-based discounts."""
    data = request.get_json()
    
    material_id = data.get('material_id')
    lease_duration_days = data.get('lease_duration_days')
    quantity = data.get('quantity')
    
    if not all([material_id, lease_duration_days, quantity]):
        return jsonify({'error': 'material_id, lease_duration_days, and quantity are required'}), 400
    
    pricing = recommender.optimize_pricing(material_id, lease_duration_days, quantity)
    
    if not pricing:
        return jsonify({'error': 'Material not found'}), 404
    
    return jsonify(pricing), 200


@api.route('/users', methods=['POST'])
def create_user():
    """Create a new user."""
    data = request.get_json()
    
    # Check if user exists
    existing_user = User.query.filter(
        (User.username == data.get('username')) | 
        (User.email == data.get('email'))
    ).first()
    
    if existing_user:
        return jsonify({'error': 'Username or email already exists'}), 400
    
    user = User(
        username=data.get('username'),
        email=data.get('email'),
        company_name=data.get('company_name'),
        phone=data.get('phone')
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201


@api.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user details."""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200


@api.route('/leases', methods=['POST'])
def create_lease():
    """Create a new lease."""
    data = request.get_json()
    
    # Parse dates
    start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
    end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()
    
    lease = Lease(
        user_id=data.get('user_id'),
        project_name=data.get('project_name'),
        project_description=data.get('project_description'),
        start_date=start_date,
        end_date=end_date,
        status='pending',
        delivery_address=data.get('delivery_address')
    )
    
    # Add lease items
    items = data.get('items', [])
    total_cost = 0
    
    for item_data in items:
        material = Material.query.get(item_data['material_id'])
        if not material:
            return jsonify({'error': f'Material {item_data["material_id"]} not found'}), 404
        
        # Check availability
        if material.quantity_available < item_data['quantity']:
            return jsonify({'error': f'Insufficient quantity for {material.name}'}), 400
        
        # Calculate cost
        days = (end_date - start_date).days + 1
        subtotal = material.price_per_day * item_data['quantity'] * days
        
        lease_item = LeaseItem(
            material_id=item_data['material_id'],
            quantity=item_data['quantity'],
            price_per_day=material.price_per_day,
            subtotal=subtotal
        )
        lease.lease_items.append(lease_item)
        total_cost += subtotal
        
        # Update material availability
        material.quantity_available -= item_data['quantity']
    
    lease.total_cost = total_cost
    
    db.session.add(lease)
    db.session.commit()
    
    return jsonify(lease.to_dict()), 201


@api.route('/leases/<int:lease_id>', methods=['GET'])
def get_lease(lease_id):
    """Get lease details."""
    lease = Lease.query.get_or_404(lease_id)
    return jsonify(lease.to_dict()), 200


@api.route('/leases/user/<int:user_id>', methods=['GET'])
def get_user_leases(user_id):
    """Get all leases for a user."""
    leases = Lease.query.filter_by(user_id=user_id).all()
    return jsonify([lease.to_dict() for lease in leases]), 200


@api.route('/leases/<int:lease_id>/status', methods=['PUT'])
def update_lease_status(lease_id):
    """Update lease status."""
    lease = Lease.query.get_or_404(lease_id)
    data = request.get_json()
    
    new_status = data.get('status')
    if new_status not in ['pending', 'active', 'completed', 'cancelled']:
        return jsonify({'error': 'Invalid status'}), 400
    
    old_status = lease.status
    lease.status = new_status
    
    # If lease is completed or cancelled, return materials to inventory
    if new_status in ['completed', 'cancelled'] and old_status not in ['completed', 'cancelled']:
        for item in lease.lease_items:
            material = Material.query.get(item.material_id)
            if material:
                material.quantity_available += item.quantity
    
    db.session.commit()
    
    return jsonify(lease.to_dict()), 200


@api.route('/categories', methods=['GET'])
def get_categories():
    """Get all material categories."""
    categories = db.session.query(Material.category).distinct().all()
    return jsonify([cat[0] for cat in categories if cat[0]]), 200


def _update_recommender():
    """Update the recommender with current materials."""
    materials = Material.query.all()
    materials_data = [mat.to_dict() for mat in materials]
    recommender.fit(materials_data)


def _generate_recommendation_reason(material, score):
    """Generate a human-readable recommendation reason."""
    if score > 0.7:
        return "Highly relevant for your project requirements"
    elif score > 0.5:
        return "Good match for your project"
    elif score > 0.3:
        return "May be useful for your project"
    else:
        return "Consider for complementary needs"
