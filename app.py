"""
Main application entry point for the AI Interior Design Platform.
"""
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_app():
    """
    Application factory pattern.
    """
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    from src.api import design_routes, lease_routes, user_routes
    app.register_blueprint(design_routes.bp)
    app.register_blueprint(lease_routes.bp)
    app.register_blueprint(user_routes.bp)
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'AI Interior Design Platform'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)
