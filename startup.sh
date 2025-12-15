#!/bin/bash
set -e

echo "=== Azure Flask Heartline Startup BEGIN ==="

# Always run from app root
cd /app || cd /home/site/wwwroot || true

#######################################
# Apply nginx config
#######################################
if [ -f /home/site/wwwroot/nginx.conf ]; then
  echo "Applying nginx config"
  cp /home/site/wwwroot/nginx.conf /etc/nginx/sites-available/default
  service nginx reload
fi

#######################################
# Create necessary directories
#######################################
mkdir -p \
  uploads/ecg_files \
  uploads/visit_docs \
  instance \
  logs

# Set ownership to web server user (Azure uses www-data or nginx)
chown -R www-data:www-data uploads instance logs || chown -R nginx:nginx uploads instance logs || true
chmod -R 775 uploads instance logs || true

#######################################
# Install Python dependencies
#######################################
echo "Installing Python dependencies..."
python3 -m pip install --upgrade pip
pip install -r requirements.txt

#######################################
# Database initialization
#######################################
# Start Gunicorn (Production WSGI server)
echo "Starting Gunicorn..."
gunicorn --bind=0.0.0.0:8000 \
         --workers=4 \
         --threads=2 \
         --timeout=120 \
         --access-logfile=- \
         --error-logfile=- \
         --log-level=info \
         app:app &

# Wait for Gunicorn to start
sleep 5

# Run Database tasks in background so they don't block container startup
(
    echo "Initializing database..."
    python3 -c "
from app import app, db
with app.app_context():
    try:
        db.create_all()
        print('✅ Database tables created/verified')
    except Exception as e:
        print(f'❌ Database error: {e}')
" || echo "⚠️ Database initialization had issues"

    echo "Checking/Importing Medicaments..."
    python3 import_medicaments.py || echo "⚠️ Medicament import failed"

    echo "Checking/Creating Demo Data..."
    python3 create_demo_data.py || echo "⚠️ Demo data creation failed"
) &

# Wait for Gunicorn to be ready
sleep 3

# Pre-warm the application
echo "Pre-warming application..."
curl -s http://localhost:8000 > /dev/null 2>&1 || true

echo "=== Azure Flask Heartline Startup DONE ==="

# Keep container alive
tail -f /dev/null
