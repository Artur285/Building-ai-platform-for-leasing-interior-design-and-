"""Middleware for request logging and error handling."""
from flask import request, g
from datetime import datetime
import time
import traceback


def setup_middleware(app):
    """Setup middleware for the Flask application."""
    
    @app.before_request
    def before_request():
        """Log request details and track request time."""
        g.start_time = time.time()
        app.logger.info(f'Request: {request.method} {request.path} from {request.remote_addr}')
    
    @app.after_request
    def after_request(response):
        """Log response details and request duration."""
        if hasattr(g, 'start_time'):
            elapsed = time.time() - g.start_time
            app.logger.info(
                f'Response: {request.method} {request.path} '
                f'Status={response.status_code} Duration={elapsed:.3f}s'
            )
        return response
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Global exception handler."""
        app.logger.error(f'Unhandled exception: {str(e)}')
        app.logger.error(traceback.format_exc())
        
        return {
            'error': 'Internal server error',
            'message': str(e) if app.debug else 'An unexpected error occurred',
            'timestamp': datetime.utcnow().isoformat()
        }, 500
    
    @app.errorhandler(404)
    def not_found(e):
        """Handle 404 errors."""
        return {
            'error': 'Not found',
            'message': f'The requested resource was not found: {request.path}',
            'timestamp': datetime.utcnow().isoformat()
        }, 404
    
    @app.errorhandler(500)
    def internal_error(e):
        """Handle 500 errors."""
        app.logger.error(f'Internal server error: {str(e)}')
        return {
            'error': 'Internal server error',
            'message': 'An internal error occurred',
            'timestamp': datetime.utcnow().isoformat()
        }, 500
    
    return app
