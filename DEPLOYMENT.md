# Production Deployment Guide

## Overview
This guide covers deploying the AI Building Materials Leasing Platform to production environments.

## Prerequisites
- Docker and Docker Compose installed
- Access to a production server or cloud platform
- SSL certificates (for HTTPS)
- Domain name configured (optional)

## Deployment Options

### Option 1: Docker Compose (Recommended for single server)

1. **Prepare Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with production values
   nano .env
   ```

2. **Build and Start Services**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d --build
   ```

3. **Check Service Status**
   ```bash
   docker-compose -f docker-compose.prod.yml ps
   docker-compose -f docker-compose.prod.yml logs -f
   ```

4. **Access the Application**
   - Application: http://your-server-ip
   - Prometheus: http://your-server-ip:9090
   - Grafana: http://your-server-ip:3000

### Option 2: Kubernetes Deployment (Recommended for scaling)

1. **Create Secrets**
   ```bash
   kubectl create secret generic ai-leasing-secrets \
     --from-literal=database-url='your-database-url' \
     --from-literal=secret-key='your-secret-key'
   ```

2. **Deploy Application**
   ```bash
   kubectl apply -f k8s-deployment.yaml
   ```

3. **Check Deployment Status**
   ```bash
   kubectl get pods
   kubectl get services
   kubectl logs -f deployment/ai-leasing-platform
   ```

4. **Scale Application**
   ```bash
   kubectl scale deployment ai-leasing-platform --replicas=5
   ```

### Option 3: Traditional Server Deployment

1. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx
   ```

2. **Setup Application**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure Systemd Service**
   Create `/etc/systemd/system/ai-leasing.service`:
   ```ini
   [Unit]
   Description=AI Leasing Platform
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/opt/ai-leasing-platform
   Environment="PATH=/opt/ai-leasing-platform/venv/bin"
   ExecStart=/opt/ai-leasing-platform/venv/bin/gunicorn -c gunicorn_config.py main:app

   [Install]
   WantedBy=multi-user.target
   ```

4. **Start Service**
   ```bash
   sudo systemctl enable ai-leasing
   sudo systemctl start ai-leasing
   sudo systemctl status ai-leasing
   ```

## Health Checks

The application provides multiple health check endpoints:

- **Basic Health**: `GET /api/health`
- **Liveness Probe**: `GET /api/health/live`
- **Readiness Probe**: `GET /api/health/ready`
- **Metrics**: `GET /api/metrics`
- **App Info**: `GET /api/info`

## Monitoring

### Prometheus Metrics
Access Prometheus at `http://your-server:9090` to view:
- Application metrics (materials, users, leases)
- System metrics (CPU, memory, disk)
- Process metrics

### Grafana Dashboards
1. Access Grafana at `http://your-server:3000`
2. Default credentials: admin/admin
3. Add Prometheus as data source: `http://prometheus:9090`
4. Create dashboards for monitoring

### Log Files
Logs are stored in the `logs/` directory:
- `app.log` - General application logs
- `error.log` - Error logs

View logs:
```bash
tail -f logs/app.log
tail -f logs/error.log
```

## SSL/HTTPS Configuration

1. **Obtain SSL Certificate**
   - Using Let's Encrypt: `certbot --nginx -d your-domain.com`
   - Or use your own certificates

2. **Update Nginx Configuration**
   Uncomment SSL section in `nginx.conf` and update paths

3. **Reload Nginx**
   ```bash
   docker-compose -f docker-compose.prod.yml restart nginx
   ```

## Database Backup

### Automated Backup Script
Create `backup.sh`:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
mkdir -p $BACKUP_DIR
cp data/leasing_platform.db $BACKUP_DIR/leasing_platform_$DATE.db
# Keep only last 7 days
find $BACKUP_DIR -name "leasing_platform_*.db" -mtime +7 -delete
```

### Setup Cron Job
```bash
crontab -e
# Add: 0 2 * * * /path/to/backup.sh
```

## Performance Tuning

### Gunicorn Workers
Adjust in `gunicorn_config.py`:
```python
workers = (2 * cpu_count) + 1  # Default formula
```

### Database Connection Pool
Adjust in `config.py`:
```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 20,
    'max_overflow': 40
}
```

### Nginx Worker Connections
Adjust in `nginx.conf`:
```nginx
worker_connections 2048;
```

## Security Checklist

- [ ] Change all default passwords
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall (ufw/iptables)
- [ ] Set up rate limiting
- [ ] Regular security updates
- [ ] Database backups configured
- [ ] Monitor logs for suspicious activity
- [ ] Use environment variables for secrets
- [ ] Restrict database access

## Troubleshooting

### Application Won't Start
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs app

# Check database
docker-compose -f docker-compose.prod.yml exec app python -c "from main import create_app; app = create_app(); print('OK')"
```

### High CPU Usage
```bash
# Check metrics
curl http://localhost:8000/api/metrics

# Scale up
docker-compose -f docker-compose.prod.yml up -d --scale app=3
```

### Database Issues
```bash
# Backup current database
cp data/leasing_platform.db data/leasing_platform.db.backup

# Recreate database
docker-compose -f docker-compose.prod.yml exec app python -c "from main import create_app; app = create_app()"
```

## Rollback Procedure

1. **Stop Current Version**
   ```bash
   docker-compose -f docker-compose.prod.yml down
   ```

2. **Restore Previous Version**
   ```bash
   git checkout <previous-commit>
   docker-compose -f docker-compose.prod.yml up -d --build
   ```

3. **Restore Database (if needed)**
   ```bash
   cp /backups/leasing_platform_<date>.db data/leasing_platform.db
   ```

## Support and Maintenance

### Regular Maintenance Tasks
- Weekly: Review logs and metrics
- Monthly: Update dependencies
- Quarterly: Security audit
- As needed: Database optimization

### Update Procedure
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up -d --build

# Verify health
curl http://localhost:8000/api/health
```

## Contact and Support
For issues or questions, check:
- Application logs: `logs/app.log`
- Health status: `/api/health`
- Metrics: `/api/metrics`
