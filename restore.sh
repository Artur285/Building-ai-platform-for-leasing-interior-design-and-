#!/bin/bash
# Restore script for AI Building Materials Leasing Platform

# Configuration
BACKUP_DIR="${BACKUP_DIR:-/backups}"
DATA_DIR="${DATA_DIR:-/app/data}"

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

# Check if backup directory exists
if [ ! -d "$BACKUP_DIR" ]; then
    error "Backup directory not found: $BACKUP_DIR"
    exit 1
fi

log "AI Building Materials Leasing Platform - Restore Utility"
echo "========================================================"
echo ""

# List available backups
log "Available database backups:"
backups=($(ls -t "$BACKUP_DIR"/leasing_platform_*.db.gz 2>/dev/null))

if [ ${#backups[@]} -eq 0 ]; then
    error "No backups found in $BACKUP_DIR"
    exit 1
fi

# Display backups with numbers
for i in "${!backups[@]}"; do
    backup_file=$(basename "${backups[$i]}")
    backup_date=$(echo "$backup_file" | sed 's/leasing_platform_\(.*\)\.db\.gz/\1/')
    backup_size=$(du -h "${backups[$i]}" | cut -f1)
    echo "  [$i] $backup_date ($backup_size)"
done

echo ""
read -p "Select backup to restore (enter number): " selection

# Validate selection
if ! [[ "$selection" =~ ^[0-9]+$ ]] || [ "$selection" -ge "${#backups[@]}" ]; then
    error "Invalid selection"
    exit 1
fi

selected_backup="${backups[$selection]}"
log "Selected backup: $(basename "$selected_backup")"

# Confirm restoration
warn "This will replace the current database. Are you sure?"
read -p "Type 'yes' to continue: " confirmation

if [ "$confirmation" != "yes" ]; then
    log "Restore cancelled"
    exit 0
fi

# Stop the application (if using systemd)
if systemctl is-active --quiet ai-leasing; then
    log "Stopping application..."
    sudo systemctl stop ai-leasing
    APP_WAS_RUNNING=true
fi

# Backup current database before restore
if [ -f "$DATA_DIR/leasing_platform.db" ]; then
    log "Backing up current database..."
    cp "$DATA_DIR/leasing_platform.db" "$DATA_DIR/leasing_platform.db.before_restore"
fi

# Restore database
log "Restoring database..."
mkdir -p "$DATA_DIR"
gunzip -c "$selected_backup" > "$DATA_DIR/leasing_platform.db"

if [ $? -eq 0 ]; then
    log "Database restored successfully!"
else
    error "Database restore failed"
    
    # Restore previous database
    if [ -f "$DATA_DIR/leasing_platform.db.before_restore" ]; then
        warn "Restoring previous database..."
        mv "$DATA_DIR/leasing_platform.db.before_restore" "$DATA_DIR/leasing_platform.db"
    fi
    
    exit 1
fi

# Set proper permissions
chmod 644 "$DATA_DIR/leasing_platform.db"

# Restart application if it was running
if [ "$APP_WAS_RUNNING" = true ]; then
    log "Starting application..."
    sudo systemctl start ai-leasing
fi

log "Restore completed successfully!"
log "Previous database saved as: leasing_platform.db.before_restore"

exit 0
