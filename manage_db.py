#!/usr/bin/env python3
"""
Database migration and maintenance utility for AI Leasing Platform.
"""
import os
import sys
import argparse
from datetime import datetime
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import create_app
from app.models import db, Material, User, Lease, LeaseItem


def backup_database(backup_dir='backups'):
    """Create a backup of the current database."""
    app = create_app()
    
    with app.app_context():
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        
        if not os.path.exists(db_path):
            print("❌ Database file not found")
            return False
        
        # Create backup directory
        os.makedirs(backup_dir, exist_ok=True)
        
        # Create backup with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(backup_dir, f'db_backup_{timestamp}.db')
        
        shutil.copy2(db_path, backup_path)
        print(f"✅ Database backed up to: {backup_path}")
        return True


def export_data(output_file='data_export.json'):
    """Export all data to JSON format."""
    import json
    
    app = create_app()
    
    with app.app_context():
        data = {
            'materials': [m.to_dict() for m in Material.query.all()],
            'users': [u.to_dict() for u in User.query.all()],
            'leases': [l.to_dict() for l in Lease.query.all()],
            'export_date': datetime.utcnow().isoformat()
        }
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Data exported to: {output_file}")
        print(f"   Materials: {len(data['materials'])}")
        print(f"   Users: {len(data['users'])}")
        print(f"   Leases: {len(data['leases'])}")


def import_data(input_file='data_export.json'):
    """Import data from JSON format."""
    import json
    
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return False
    
    app = create_app()
    
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    with app.app_context():
        # Import materials
        for mat_data in data.get('materials', []):
            # Remove auto-generated fields
            mat_data.pop('id', None)
            mat_data.pop('created_at', None)
            mat_data.pop('updated_at', None)
            
            material = Material(**mat_data)
            db.session.add(material)
        
        # Import users
        for user_data in data.get('users', []):
            user_data.pop('id', None)
            user_data.pop('created_at', None)
            
            user = User(**user_data)
            db.session.add(user)
        
        db.session.commit()
        print(f"✅ Data imported successfully")


def show_stats():
    """Show database statistics."""
    app = create_app()
    
    with app.app_context():
        material_count = Material.query.count()
        user_count = User.query.count()
        lease_count = Lease.query.count()
        active_leases = Lease.query.filter_by(status='active').count()
        
        print("\n📊 Database Statistics")
        print("=" * 50)
        print(f"Materials:        {material_count:>10}")
        print(f"Users:            {user_count:>10}")
        print(f"Total Leases:     {lease_count:>10}")
        print(f"Active Leases:    {active_leases:>10}")
        print("=" * 50)
        
        # Category breakdown
        print("\n📦 Materials by Category:")
        categories = db.session.query(
            Material.category, 
            db.func.count(Material.id)
        ).group_by(Material.category).all()
        
        for category, count in categories:
            print(f"  {category:<25} {count:>5}")


def reset_database():
    """Reset database (WARNING: deletes all data)."""
    response = input("⚠️  WARNING: This will delete ALL data. Type 'yes' to continue: ")
    
    if response.lower() != 'yes':
        print("❌ Operation cancelled")
        return False
    
    # Backup first
    print("\n📦 Creating backup before reset...")
    backup_database()
    
    app = create_app()
    
    with app.app_context():
        print("🗑️  Dropping all tables...")
        db.drop_all()
        
        print("🔨 Creating new tables...")
        db.create_all()
        
        print("✅ Database reset complete")
        return True


def add_sample_data():
    """Add sample data to database."""
    from main import _initialize_sample_data, _update_recommender
    
    app = create_app()
    
    with app.app_context():
        if Material.query.first():
            print("⚠️  Database already has data")
            response = input("Continue and add more data? (yes/no): ")
            if response.lower() != 'yes':
                return False
        
        print("📝 Adding sample data...")
        _initialize_sample_data()
        _update_recommender()
        
        print("✅ Sample data added successfully")


def compact_database():
    """Compact and optimize database."""
    app = create_app()
    
    with app.app_context():
        print("🔧 Compacting database...")
        db.session.execute(db.text('VACUUM'))
        db.session.commit()
        print("✅ Database compacted")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Database management utility for AI Leasing Platform'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Backup command
    subparsers.add_parser('backup', help='Backup database')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export data to JSON')
    export_parser.add_argument('-o', '--output', default='data_export.json',
                              help='Output file path')
    
    # Import command
    import_parser = subparsers.add_parser('import', help='Import data from JSON')
    import_parser.add_argument('-i', '--input', default='data_export.json',
                              help='Input file path')
    
    # Stats command
    subparsers.add_parser('stats', help='Show database statistics')
    
    # Reset command
    subparsers.add_parser('reset', help='Reset database (deletes all data)')
    
    # Sample data command
    subparsers.add_parser('sample', help='Add sample data')
    
    # Compact command
    subparsers.add_parser('compact', help='Compact and optimize database')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute command
    if args.command == 'backup':
        backup_database()
    elif args.command == 'export':
        export_data(args.output)
    elif args.command == 'import':
        import_data(args.input)
    elif args.command == 'stats':
        show_stats()
    elif args.command == 'reset':
        reset_database()
    elif args.command == 'sample':
        add_sample_data()
    elif args.command == 'compact':
        compact_database()


if __name__ == '__main__':
    main()
