# Deployment Guide - Hearline Webapp

## Overview

This comprehensive deployment guide covers all aspects of deploying the Hearline Webapp in production environments, from cloud platforms to on-premises installations.

## Prerequisites

### System Requirements
- **Python**: 3.7 or higher
- **Database**: PostgreSQL 12+
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 20GB minimum for application and ECG files
- **Network**: HTTPS capability for secure communication

### Dependencies
```bash
# Core dependencies
pip install -r requirements.txt

# ONNX Runtime dependencies
pip install -r requirements_onnx.txt
```

## Environment Configuration

### Environment Variables
Create a `.env` file with the following variables:

```env
# Database Configuration
DB_HOST=your-db-host
DB_PORT=5432
DB_USER=hearline_user
DB_PASSWORD=secure_password
DB_NAME=hearline_webapp

# Application Security
SECRET_KEY=your-super-secret-key-here-use-32-chars-min
FLASK_ENV=production

# File Upload Configuration
MAX_CONTENT_LENGTH=16777216  # 16MB max file size
UPLOAD_FOLDER=uploads

# ECG Model Configuration
MODEL_PATH=resnet34_model.onnx
ECG_SAMPLE_RATE=250
```

## Cloud Deployment Options

### 1. Vercel Deployment (Recommended)

The application is pre-configured for Vercel deployment with optimized settings.

#### Step 1: Prepare for Deployment
```powershell
# Ensure all dependencies are listed
pip freeze > requirements.txt

# Verify vercel.json configuration
cat vercel.json
```

#### Step 2: Deploy to Vercel
```powershell
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

#### Vercel Configuration (`vercel.json`)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb",
        "runtime": "python3.9"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "PYTHONPATH": ".",
    "FLASK_APP": "app.py"
  }
}
```

### 2. Heroku Deployment

#### Step 1: Create Heroku App
```powershell
# Install Heroku CLI
# Download from https://devcenter.heroku.com/articles/heroku-cli

# Login and create app
heroku login
heroku create hearline-webapp
```

#### Step 2: Configure Database
```powershell
# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set FLASK_ENV=production
```

#### Step 3: Deploy
```powershell
# Initialize git repository
git init
git add .
git commit -m "Initial deployment"

# Deploy to Heroku
git remote add heroku https://git.heroku.com/hearline-webapp.git
git push heroku main
```

### 3. AWS Deployment

#### Using AWS Elastic Beanstalk

1. **Create application package**:
```powershell
# Create deployment package
Compress-Archive -Path . -DestinationPath hearline-webapp.zip
```

2. **Deploy via AWS Console**:
   - Navigate to Elastic Beanstalk console
   - Create new application
   - Upload hearline-webapp.zip
   - Configure environment variables

#### Using AWS EC2

1. **Launch EC2 instance** (Ubuntu 20.04 LTS recommended)

2. **Install dependencies**:
```bash
sudo apt update
sudo apt install python3 python3-pip postgresql postgresql-contrib nginx
```

3. **Deploy application**:
```bash
# Clone repository
git clone https://github.com/your-repo/Hearline-Webapp.git
cd Hearline-Webapp

# Install Python dependencies
pip3 install -r requirements.txt

# Setup database
sudo -u postgres createdb hearline_webapp
```

## Database Setup

### PostgreSQL Configuration

#### 1. Create Database and User
```sql
-- Connect as postgres superuser
CREATE DATABASE hearline_webapp;
CREATE USER hearline_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE hearline_webapp TO hearline_user;
```

#### 2. Initialize Database Schema
```powershell
# Run database initialization
python quick_setup.py
```

#### 3. Import Medication Database
```powershell
# Import Algerian medication database
python -c "
from models import db, Medicament
from app import app
import csv

with app.app_context():
    # Load 7000+ medications
    # Import logic here
"
```

### Database Migration

For existing deployments, use the migration scripts:

```powershell
# Backup existing database
pg_dump hearline_webapp > backup_$(Get-Date -Format "yyyyMMdd_HHmmss").sql

# Run migrations
python migrate_to_onnx.py
```

## Model Deployment

### ONNX Model Setup

The application uses an optimized ONNX model for ECG analysis:

```powershell
# Verify model file exists
Test-Path "resnet34_model.onnx"

# Test model loading
python -c "
import onnxruntime as ort
session = ort.InferenceSession('resnet34_model.onnx')
print('Model loaded successfully')
print(f'Input shape: {session.get_inputs()[0].shape}')
print(f'Output shape: {session.get_outputs()[0].shape}')
"
```

### Model Performance Optimization

#### CPU Optimization
```python
# Configure ONNX Runtime for CPU
session_options = ort.SessionOptions()
session_options.intra_op_num_threads = 4
session = ort.InferenceSession('resnet34_model.onnx', session_options)
```

#### GPU Optimization (if available)
```python
# Configure for GPU acceleration
providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
session = ort.InferenceSession('resnet34_model.onnx', providers=providers)
```

## Security Configuration

### HTTPS Setup

#### Using Nginx (Recommended for production)

1. **Install Nginx**:
```bash
sudo apt install nginx
```

2. **Configure Nginx**:
```nginx
# /etc/nginx/sites-available/hearline-webapp
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/certificate.pem;
    ssl_certificate_key /path/to/private.key;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Increase max file upload size for ECG files
    client_max_body_size 50M;
}
```

### Application Security

#### Environment Security
```bash
# Secure environment file
chmod 600 .env
chown app-user:app-group .env
```

#### Database Security
```sql
-- Restrict database permissions
REVOKE ALL ON DATABASE hearline_webapp FROM PUBLIC;
GRANT CONNECT ON DATABASE hearline_webapp TO hearline_user;
```

## Monitoring and Logging

### Application Logging

Configure logging in production:

```python
# Add to app.py
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/hearline.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### Health Monitoring

#### Health Check Endpoint
```python
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'database': 'connected' if db.session.execute('SELECT 1').scalar() else 'disconnected',
        'model': 'loaded' if ort_session else 'not_loaded',
        'timestamp': datetime.utcnow().isoformat()
    })
```

#### System Monitoring
```bash
# Monitor system resources
htop
iostat -x 1
df -h
```

## Backup and Recovery

### Database Backup

#### Automated Backup Script
```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="/opt/backups/hearline"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump hearline_webapp > "$BACKUP_DIR/hearline_backup_$DATE.sql"

# Keep only last 30 backups
find $BACKUP_DIR -name "hearline_backup_*.sql" -mtime +30 -delete
```

#### Backup Cron Job
```bash
# Add to crontab
0 2 * * * /opt/scripts/backup.sh
```

### File System Backup

```bash
# Backup uploads directory
rsync -avz uploads/ /backup/location/uploads/

# Backup application files
tar -czf hearline_app_backup_$(date +%Y%m%d).tar.gz \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    .
```

## Performance Optimization

### Application Performance

#### Gunicorn Configuration
```python
# gunicorn.conf.py
bind = "127.0.0.1:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
```

#### Database Connection Pooling
```python
# Configure SQLAlchemy pool
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
    'max_overflow': 20
}
```

### ECG Processing Optimization

#### Batch Processing
```python
# For multiple ECG analyses
def batch_analyze_ecg(ecg_files):
    results = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(predict_ecg_onnx, ecg) for ecg in ecg_files]
        for future in as_completed(futures):
            results.append(future.result())
    return results
```

## Troubleshooting

### Common Issues

#### 1. ONNX Model Loading Errors
```powershell
# Verify model integrity
python -c "
import onnx
model = onnx.load('resnet34_model.onnx')
onnx.checker.check_model(model)
print('Model is valid')
"
```

#### 2. Database Connection Issues
```sql
-- Check connection limits
SELECT * FROM pg_settings WHERE name = 'max_connections';

-- Monitor active connections
SELECT count(*) FROM pg_stat_activity;
```

#### 3. Memory Issues
```bash
# Monitor memory usage
free -h
ps aux --sort=-%mem | head

# Check ECG processing memory
python -c "
import psutil
import os
process = psutil.Process(os.getpid())
print(f'Memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB')
"
```

### Log Analysis

#### Application Logs
```bash
# Monitor application logs
tail -f logs/hearline.log

# Search for errors
grep -i "error" logs/hearline.log | tail -20
```

#### Database Logs
```bash
# PostgreSQL logs location varies by system
tail -f /var/log/postgresql/postgresql-*.log
```

## Scaling Considerations

### Horizontal Scaling

#### Load Balancer Configuration (Nginx)
```nginx
upstream hearline_app {
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
}

server {
    location / {
        proxy_pass http://hearline_app;
    }
}
```

### Database Scaling

#### Read Replicas
```sql
-- Configure read replica for reporting queries
-- Use master for writes, replica for ECG history queries
```

#### Database Partitioning
```sql
-- Partition visits table by date for better performance
CREATE TABLE visits_2024 PARTITION OF visits 
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

## Maintenance Procedures

### Regular Maintenance Tasks

#### Weekly Tasks
- Database vacuum and analyze
- Log rotation
- Backup verification
- Security updates

#### Monthly Tasks
- Performance review
- Storage cleanup
- Model performance analysis
- User access review

### Update Procedures

#### Application Updates
```bash
# 1. Backup current version
git tag "backup-$(date +%Y%m%d)"

# 2. Pull updates
git pull origin main

# 3. Update dependencies
pip install -r requirements.txt

# 4. Run migrations if needed
python migrate.py

# 5. Restart application
sudo systemctl restart hearline-webapp
```

## Support and Documentation

### Additional Resources
- **Technical Documentation**: `/doc/technical_architecture.md`
- **API Reference**: `/doc/api_documentation.md`
- **Research Methodology**: `/doc/research_methodology.md`
- **Migration Guide**: `ONNX_MIGRATION_GUIDE.md`

### Contact Information
- **Technical Support**: support@hearline.healthcare
- **Documentation Issues**: docs@hearline.healthcare
- **Security Issues**: security@hearline.healthcare

---

*This deployment guide is maintained by the Hearline development team. Last updated: June 2025*
