"""Monitoring and metrics for the application."""
from flask import Blueprint, jsonify, current_app
from datetime import datetime
import psutil
import os
from app.models import db, Material, User, Lease

monitoring = Blueprint('monitoring', __name__)


@monitoring.route('/health', methods=['GET'])
def health_check():
    """Comprehensive health check endpoint."""
    try:
        # Check database connection
        db.session.execute(db.text('SELECT 1'))
        db_status = 'healthy'
    except Exception as e:
        current_app.logger.error(f'Database health check failed: {str(e)}')
        db_status = 'unhealthy'
    
    health_status = {
        'status': 'healthy' if db_status == 'healthy' else 'unhealthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'AI Building Materials Leasing Platform',
        'version': '1.0.0',
        'checks': {
            'database': db_status,
            'api': 'healthy'
        }
    }
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return jsonify(health_status), status_code


@monitoring.route('/health/ready', methods=['GET'])
def readiness_check():
    """Readiness probe for Kubernetes/container orchestration."""
    try:
        # Check if database is accessible
        db.session.execute(db.text('SELECT 1'))
        
        # Check if at least one material exists (app initialized)
        material_count = Material.query.count()
        
        if material_count > 0:
            return jsonify({
                'status': 'ready',
                'timestamp': datetime.utcnow().isoformat()
            }), 200
        else:
            return jsonify({
                'status': 'not_ready',
                'reason': 'Database not initialized',
                'timestamp': datetime.utcnow().isoformat()
            }), 503
            
    except Exception as e:
        current_app.logger.error(f'Readiness check failed: {str(e)}')
        return jsonify({
            'status': 'not_ready',
            'reason': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 503


@monitoring.route('/health/live', methods=['GET'])
def liveness_check():
    """Liveness probe for Kubernetes/container orchestration."""
    return jsonify({
        'status': 'alive',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@monitoring.route('/metrics', methods=['GET'])
def metrics():
    """Application metrics endpoint."""
    try:
        # Database metrics
        material_count = Material.query.count()
        user_count = User.query.count()
        lease_count = Lease.query.count()
        active_leases = Lease.query.filter(Lease.status == 'active').count()
        
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        metrics_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'application': {
                'materials_total': material_count,
                'users_total': user_count,
                'leases_total': lease_count,
                'leases_active': active_leases
            },
            'system': {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_used_mb': memory.used / (1024 * 1024),
                'memory_total_mb': memory.total / (1024 * 1024),
                'disk_percent': disk.percent,
                'disk_used_gb': disk.used / (1024 * 1024 * 1024),
                'disk_total_gb': disk.total / (1024 * 1024 * 1024)
            },
            'process': {
                'pid': os.getpid(),
                'threads': psutil.Process().num_threads()
            }
        }
        
        return jsonify(metrics_data), 200
        
    except Exception as e:
        current_app.logger.error(f'Metrics collection failed: {str(e)}')
        return jsonify({
            'error': 'Failed to collect metrics',
            'message': str(e)
        }), 500


@monitoring.route('/info', methods=['GET'])
def app_info():
    """Application information endpoint."""
    return jsonify({
        'name': 'AI Building Materials Leasing Platform',
        'version': '1.0.0',
        'description': 'AI-powered platform for leasing building materials and interior design items',
        'environment': os.getenv('FLASK_ENV', 'production'),
        'timestamp': datetime.utcnow().isoformat()
    }), 200
