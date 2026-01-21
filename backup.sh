#!/bin/bash
# Automated backup script for AI Building Materials Leasing Platform

# Configuration
BACKUP_DIR="${BACKUP_DIR:-/backups}"
DATA_DIR="${DATA_DIR:-/app/data}"
LOG_DIR="${LOG_DIR:-/app/logs}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"
DATE=$(date +%Y%m%d_%H%M%S)

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

# Create backup directory
mkdir -p "$BACKUP_DIR"

log "Starting backup process..."

# Backup database
if [ -f "$DATA_DIR/leasing_platform.db" ]; then
    log "Backing up database..."
    cp "$DATA_DIR/leasing_platform.db" "$BACKUP_DIR/leasing_platform_$DATE.db"
    
    # Compress the backup
    gzip "$BACKUP_DIR/leasing_platform_$DATE.db"
    
    if [ $? -eq 0 ]; then
        log "Database backup completed: leasing_platform_$DATE.db.gz"
    else
        error "Database backup failed"
        exit 1
    fi
else
    warn "Database file not found at $DATA_DIR/leasing_platform.db"
fi

# Backup configuration files
log "Backing up configuration files..."
CONFIG_BACKUP="$BACKUP_DIR/config_$DATE.tar.gz"
tar -czf "$CONFIG_BACKUP" \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    --exclude='venv' \
    --exclude='*.log' \
    config.py \
    gunicorn_config.py \
    .env 2>/dev/null

if [ $? -eq 0 ]; then
    log "Configuration backup completed: config_$DATE.tar.gz"
else
    error "Configuration backup failed"
fi

# Backup logs (last 7 days)
if [ -d "$LOG_DIR" ]; then
    log "Backing up recent logs..."
    LOGS_BACKUP="$BACKUP_DIR/logs_$DATE.tar.gz"
    find "$LOG_DIR" -name "*.log" -mtime -7 -print0 | tar -czf "$LOGS_BACKUP" --null -T -
    
    if [ $? -eq 0 ]; then
        log "Logs backup completed: logs_$DATE.tar.gz"
    else
        warn "Logs backup failed or no logs found"
    fi
fi

# Clean up old backups
log "Cleaning up old backups (older than $RETENTION_DAYS days)..."
find "$BACKUP_DIR" -name "leasing_platform_*.db.gz" -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR" -name "config_*.tar.gz" -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR" -name "logs_*.tar.gz" -mtime +$RETENTION_DAYS -delete

# Calculate backup size
BACKUP_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
log "Total backup size: $BACKUP_SIZE"

# List recent backups
log "Recent backups:"
ls -lh "$BACKUP_DIR" | grep "leasing_platform\|config\|logs" | tail -5

log "Backup process completed successfully!"

# Send notification (optional - requires mail command)
if command -v mail &> /dev/null; then
    echo "Backup completed at $(date)" | mail -s "AI Leasing Platform Backup" admin@yourcompany.com
fi

exit 0
