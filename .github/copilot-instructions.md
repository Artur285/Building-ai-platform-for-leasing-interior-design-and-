# AI Building Materials Leasing Platform - Coding Agent Instructions

## Architecture Overview

This is a Flask-based AI platform for leasing construction materials with intelligent recommendations. The system uses TF-IDF vectorization and cosine similarity for material matching.

**Core Components:**
- `main.py` - Flask app factory with database initialization and PWA routes
- `app/models.py` - SQLAlchemy models (Material, User, Lease, LeaseItem with relationships)
- `app/routes.py` - REST API blueprint with 15+ endpoints
- `app/ai_engine.py` - MaterialRecommender class implementing TF-IDF similarity matching
- `config.py` - Configuration (uses SQLite by default, configurable via env vars)
- `static/index.html` - Single-page web interface with PWA support

**Key Data Flow:**
1. Materials are loaded/created → stored in SQLite → vectorized by AI engine
2. Project description submitted → TF-IDF vectorization → cosine similarity matching → ranked recommendations
3. Lease creation → validates material availability → updates inventory → calculates pricing with AI discounts

## Development Workflow

### Starting the Application
```bash
# Standard mode
python main.py

# Debug mode (use sparingly in production)
FLASK_DEBUG=True python main.py

# VS Code: Press F5 or run task "Start Flask Server"
```

### Database Initialization
- Database auto-creates on first run via `db.create_all()` in `create_app()`
- Sample data (15 materials) seeds automatically if database is empty
- No migrations - uses SQLAlchemy's create_all pattern
- Database file: `materials_leasing.db` (gitignored)

### Testing APIs
Use `api-tests.http` with VS Code REST Client extension:
- Open file → click "Send Request" above any HTTP request
- Requests are pre-configured with sample data
- Change `@baseUrl` variable for different environments

### AI Engine Updates
The recommender re-trains automatically when:
- Materials are created/updated (via `_update_recommender()` in routes.py)
- Application starts (loads all materials from database)
- Pattern: Always call `_update_recommender()` after modifying Material table

## Project-Specific Patterns

### Model Relationships
**Critical**: Use `backref` for bidirectional relationships:
```python
# In Material model
lease_items = db.relationship('LeaseItem', backref='material', lazy=True)
# This creates material.lease_items AND lease_item.material
```

**Cascade Deletes**: Leases use `cascade='all, delete-orphan'` for LeaseItems - deleting a lease removes all items.

### API Response Pattern
All models have `to_dict()` methods for serialization. Always use these instead of manual dict construction:
```python
return jsonify(material.to_dict()), 200  # Correct
return jsonify({'id': material.id, ...}), 200  # Avoid - misses fields
```

### AI Recommendation Workflow
1. **Training**: `recommender.fit(materials_list)` - combines name + category + description + specs into single text
2. **Querying**: Vectorizes query text → computes cosine similarity → returns top N with scores > 0
3. **Complementary**: Finds materials from different categories than selected items
4. **Pricing**: Applies duration discounts (5%/10%/20% at 7/30/90 days) + quantity discounts (5%/10%/15% at 20/50/100 units), max 30% total

### Error Handling Convention
- Use Flask's `get_or_404()` for single resource lookups (returns 404 automatically)
- Return explicit error JSON with status codes for validation errors
- No authentication yet - add JWT if implementing auth

## VS Code Integration

### Debug Configurations (`.vscode/launch.json`)
- **Python: Flask** - Main debugger, sets FLASK_APP=main.py
- **Python: Current File** - Debug any Python file
- **Python: Run Tests/Examples** - Execute test_api.py or examples.py

### Tasks (`.vscode/tasks.json`)
- **Start Flask Server** - Normal mode
- **Start Flask Server (Debug)** - Sets FLASK_DEBUG=True
- **Run Tests/Examples** - Execute Python scripts
- **Install Dependencies** - pip install from requirements.txt

### Formatting
- Python: Black (88 char line length) - auto-formats on save
- Configured in `.vscode/settings.json`

## PWA Features

### Service Worker Pattern (`static/service-worker.js`)
- Cache-first for static assets (HTML, CSS, images)
- Network-first for API calls (ensures fresh data)
- Caches version: Update `CACHE_VERSION` when deploying changes

### Manifest (`static/manifest.json`)
- Defines app name, icons, theme colors
- `start_url: "/"` launches to homepage
- `display: "standalone"` removes browser UI

### Installation
Chrome shows install prompt automatically when manifest + service worker + HTTPS (or localhost) are present.

## Common Tasks

### Adding New Material Categories
1. Create materials with new category name (categories are strings, not enums)
2. AI engine automatically handles new categories
3. Update frontend category list in `static/index.html` if filtering UI exists

### Modifying AI Algorithm
- `MaterialRecommender` in `app/ai_engine.py`
- Uses scikit-learn TfidfVectorizer - adjust `max_features` or `stop_words` for tuning
- To change similarity metric: Modify `cosine_similarity` call (line ~67)
- Always call `recommender.fit()` with updated data after changes

### Database Changes
No migration system currently. For schema changes:
1. Delete `materials_leasing.db`
2. Restart app (auto-creates new schema)
3. For production: Implement Alembic migrations

### Pricing Logic Customization
Located in `app/routes.py` → `optimize_pricing()` endpoint:
- Duration thresholds: 7, 30, 90 days
- Quantity thresholds: 20, 50, 100 units
- Modify these constants or extract to config.py

## Key Files & Locations

- **API Endpoints**: All in `app/routes.py` - single Blueprint pattern
- **Database Models**: All in `app/models.py` - 4 models with relationships
- **AI Logic**: All in `app/ai_engine.py` - single class with fit/predict pattern
- **Sample Data**: `main.py` → `_initialize_sample_data()` - 15 hardcoded materials
- **Static Files**: `static/` folder - served directly by Flask
- **Tests**: `test_api.py` (programmatic), `api-tests.http` (REST Client), `examples.py` (usage examples)

## Dependencies

**Core**: Flask 3.0, SQLAlchemy 3.1, scikit-learn 1.3
**Why scikit-learn**: TF-IDF vectorization and cosine similarity for text-based recommendations
**No JWT/Auth**: Not implemented yet - users are simple records without passwords

## Gotchas

1. **Recommender State**: Global instance in `routes.py` - not thread-safe for write operations (OK for reads)
2. **Date Handling**: Lease dates are `date` objects, not `datetime` - use `.isoformat()` for JSON serialization
3. **Price Snapshots**: LeaseItem stores `price_per_day` at creation time (historical pricing)
4. **Quantity Updates**: No automatic inventory deduction on lease creation - implement if needed
5. **PWA Updates**: Service worker caches aggressively - users may need hard refresh (Ctrl+Shift+R) after deploys
