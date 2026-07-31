#!/bin/bash
# ===========================================
# GIPIS Institucional - Docker Entrypoint
# ===========================================

echo "=== GIPIS Institucional - Starting ==="

# Initialize database if needed
if [ ! -f /app/instance/gipis.db ]; then
    echo "Database not found. Initializing..."
    
    # Create tables
    python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
    
    # Migrate data from JSON
    if [ -f /app/scripts/migrate_json.py ]; then
        echo "Running data migration from database.json..."
        python scripts/migrate_json.py
    fi
    
    # Set initial passwords
    if [ -f /app/scripts/set_passwords.py ]; then
        echo "Setting initial passwords..."
        python scripts/set_passwords.py
    fi
    
    echo "Database initialized!"
else
    echo "Database found. Running pending migrations..."
    # Ejecutar migraciones pendientes (idempotente)
    if [ -f /app/scripts/add_email_columns.py ]; then
        python scripts/add_email_columns.py
    fi
    if [ -f /app/scripts/add_phone_column.py ]; then
        python scripts/add_phone_column.py
    fi
    if [ -f /app/scripts/add_member_features.py ]; then
        python scripts/add_member_features.py
    fi
fi

echo "Starting server..."
if [ "$FLASK_DEBUG" = "1" ]; then
    echo "Development mode - Flask dev server with auto-reload"
    exec python -m flask --app run:app run --host 0.0.0.0 --port 5000 --reload --debug
else
    echo "Production mode - Gunicorn"
    exec gunicorn --bind 0.0.0.0:5000 --workers 2 --access-logfile - --error-logfile - run:app
fi
