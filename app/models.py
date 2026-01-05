"""Database models for the Building Materials Leasing Platform."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Material(db.Model):
    """Building material inventory model."""
    __tablename__ = 'materials'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    unit = db.Column(db.String(50), nullable=False)  # e.g., 'sqft', 'piece', 'ton'
    price_per_day = db.Column(db.Float, nullable=False)
    quantity_available = db.Column(db.Integer, nullable=False)
    specifications = db.Column(db.Text)  # JSON string for material specs
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    lease_items = db.relationship('LeaseItem', backref='material', lazy=True)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'unit': self.unit,
            'price_per_day': self.price_per_day,
            'quantity_available': self.quantity_available,
            'specifications': self.specifications,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class User(db.Model):
    """User model for authentication and tracking."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    company_name = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    leases = db.relationship('Lease', backref='user', lazy=True)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'company_name': self.company_name,
            'phone': self.phone,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Lease(db.Model):
    """Lease/rental agreement model."""
    __tablename__ = 'leases'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_name = db.Column(db.String(200), nullable=False)
    project_description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')  # pending, active, completed, cancelled
    total_cost = db.Column(db.Float)
    delivery_address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    lease_items = db.relationship('LeaseItem', backref='lease', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'project_name': self.project_name,
            'project_description': self.project_description,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'total_cost': self.total_cost,
            'delivery_address': self.delivery_address,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'items': [item.to_dict() for item in self.lease_items]
        }


class LeaseItem(db.Model):
    """Individual items in a lease."""
    __tablename__ = 'lease_items'
    
    id = db.Column(db.Integer, primary_key=True)
    lease_id = db.Column(db.Integer, db.ForeignKey('leases.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_per_day = db.Column(db.Float, nullable=False)  # Snapshot of price at time of lease
    subtotal = db.Column(db.Float)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'lease_id': self.lease_id,
            'material_id': self.material_id,
            'material_name': self.material.name if self.material else None,
            'quantity': self.quantity,
            'price_per_day': self.price_per_day,
            'subtotal': self.subtotal
        }
