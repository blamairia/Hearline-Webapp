# Technical Architecture - Hearline Webapp

## System Overview

The Hearline Webapp is a sophisticated AI-powered cardiology management system built on a modern, scalable architecture. This document provides comprehensive technical specifications, architectural decisions, and implementation details for developers, system administrators, and technical stakeholders.

## High-Level Architecture

### System Architecture Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Load Balancer │    │   CDN/Assets    │
│   (Bootstrap)   │◄──►│   (Nginx)       │◄──►│   Distribution  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Flask Application Server                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Auth      │  │   ECG AI    │  │   Patient   │            │
│  │   Module    │  │   Engine    │  │   Management│            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │   ONNX Runtime  │    │   File Storage  │
│   Database      │    │   AI Models     │    │   (ECG/Docs)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Architecture Principles

1. **Separation of Concerns**: Clear division between presentation, business logic, and data layers
2. **Scalability**: Horizontal scaling capabilities with load balancing
3. **Security**: Multi-layer security implementation with encryption and access controls
4. **Performance**: Optimized AI inference with ONNX Runtime
5. **Maintainability**: Modular design with clear interfaces and documentation

## Core Components

### 1. Flask Application Framework

#### Application Structure
```
app.py                    # Main application entry point
├── Config Management     # Environment-based configuration
├── Database Integration  # SQLAlchemy ORM setup
├── Authentication       # Flask-Login user management
├── AI Model Loading     # ONNX Runtime initialization
└── Route Definitions    # API and web endpoints
```

#### Flask Configuration
```python
class Config:
    """Base configuration with security defaults"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://localhost/hearline'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 20
    }
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    
class ProductionConfig(Config):
    """Production-specific configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = False
    
class DevelopmentConfig(Config):
    """Development-specific configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
```

#### Application Factory Pattern
```python
def create_app(config_name='production'):
    """Application factory for different environments"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    moment.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(ecg_bp)
    app.register_blueprint(api_bp)
    
    return app
```

### 2. Database Architecture

#### PostgreSQL Schema Design

##### Core Entities
```sql
-- Patient entity with comprehensive demographic data
CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10) CHECK (gender IN ('Male', 'Female', 'Other')),
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(255) UNIQUE,
    medical_history TEXT,
    emergency_contact JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Visit entity with ECG analysis integration
CREATE TABLE visits (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id) ON DELETE CASCADE,
    doctor_id INTEGER REFERENCES users(id),
    visit_date TIMESTAMP WITH TIME ZONE NOT NULL,
    diagnosis TEXT,
    follow_up_date TIMESTAMP WITH TIME ZONE,
    
    -- ECG Analysis Fields
    ecg_prediction JSONB,  -- AI model predictions
    ecg_mat VARCHAR(255),  -- Path to .mat file
    ecg_hea VARCHAR(255),  -- Path to .hea file
    ecg_analysis_date TIMESTAMP WITH TIME ZONE,
    
    -- Payment Information
    payment_total DECIMAL(10,2) DEFAULT 0.00,
    payment_status VARCHAR(20) DEFAULT 'pending',
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- User management with role-based access
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('doctor', 'assistant')),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Medication database (7000+ Algerian medications)
CREATE TABLE medicaments (
    id SERIAL PRIMARY KEY,
    commercial_name VARCHAR(255) NOT NULL,
    scientific_name VARCHAR(255),
    pharmaceutical_form VARCHAR(100),
    dosage VARCHAR(100),
    presentation VARCHAR(100),
    price DECIMAL(10,2),
    manufacturer VARCHAR(255),
    therapeutic_class VARCHAR(100),
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Prescription management
CREATE TABLE prescriptions (
    id SERIAL PRIMARY KEY,
    visit_id INTEGER REFERENCES visits(id) ON DELETE CASCADE,
    medicament_id INTEGER REFERENCES medicaments(id),
    quantity INTEGER NOT NULL,
    dosage_instructions TEXT,
    duration_days INTEGER,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

##### Performance Optimization Indexes
```sql
-- Performance indexes for common queries
CREATE INDEX idx_patients_name ON patients USING gin(to_tsvector('english', first_name || ' ' || last_name));
CREATE INDEX idx_visits_date ON visits(visit_date DESC);
CREATE INDEX idx_visits_patient ON visits(patient_id);
CREATE INDEX idx_visits_ecg_prediction ON visits USING gin(ecg_prediction) WHERE ecg_prediction IS NOT NULL;
CREATE INDEX idx_medicaments_search ON medicaments USING gin(to_tsvector('english', commercial_name || ' ' || scientific_name));
CREATE INDEX idx_users_role ON users(role) WHERE is_active = TRUE;

-- Partial indexes for ECG data
CREATE INDEX idx_visits_with_ecg ON visits(id) WHERE ecg_prediction IS NOT NULL;
CREATE INDEX idx_visits_pending_analysis ON visits(id) WHERE ecg_mat IS NOT NULL AND ecg_prediction IS NULL;
```

#### Database Connection Management
```python
class DatabaseManager:
    """Advanced database connection and session management"""
    
    def __init__(self, app=None):
        self.db = SQLAlchemy()
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize database with application"""
        self.db.init_app(app)
        
        # Configure connection pooling
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_size': 10,
            'pool_recycle': 3600,
            'pool_pre_ping': True,
            'max_overflow': 20,
            'pool_timeout': 30
        }
        
        # Setup event listeners for monitoring
        self._setup_event_listeners()
    
    def _setup_event_listeners(self):
        """Setup database event listeners for monitoring"""
        from sqlalchemy import event
        
        @event.listens_for(self.db.engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            if 'postgresql' in str(dbapi_connection):
                cursor = dbapi_connection.cursor()
                cursor.execute("SET timezone TO 'UTC'")
                cursor.close()
```

### 3. AI/ML Architecture

#### ONNX Runtime Integration

##### Model Loading and Initialization
```python
class ECGModelManager:
    """Centralized ECG model management with ONNX Runtime"""
    
    def __init__(self, model_path='resnet34_model.onnx'):
        self.model_path = model_path
        self.session = None
        self.input_name = None
        self.output_name = None
        self._load_model()
    
    def _load_model(self):
        """Load ONNX model with optimized session options"""
        try:
            # Configure session options for performance
            session_options = ort.SessionOptions()
            session_options.intra_op_num_threads = 4
            session_options.inter_op_num_threads = 2
            session_options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
            session_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
            
            # Create inference session
            self.session = ort.InferenceSession(
                self.model_path, 
                session_options,
                providers=['CPUExecutionProvider']
            )
            
            # Get input/output names
            self.input_name = self.session.get_inputs()[0].name
            self.output_name = self.session.get_outputs()[0].name
            
            logging.info(f"ECG model loaded successfully: {self.model_path}")
            logging.info(f"Input shape: {self.session.get_inputs()[0].shape}")
            logging.info(f"Output shape: {self.session.get_outputs()[0].shape}")
            
        except Exception as e:
            logging.error(f"Failed to load ECG model: {e}")
            raise
    
    def predict(self, ecg_signal):
        """Perform ECG prediction with error handling"""
        try:
            if self.session is None:
                raise RuntimeError("Model not loaded")
            
            # Validate input shape
            if ecg_signal.shape != (12, 15000):
                raise ValueError(f"Invalid input shape: {ecg_signal.shape}, expected (12, 15000)")
            
            # Prepare input for model
            input_data = np.expand_dims(ecg_signal, axis=0).astype(np.float32)
            
            # Run inference
            outputs = self.session.run([self.output_name], {self.input_name: input_data})
            probabilities = outputs[0][0]
            
            # Convert to probability dictionary
            class_names = ["SNR", "AF", "IAVB", "LBBB", "RBBB", "PAC", "PVC", "STD", "STE"]
            prob_dict = {name: float(prob) for name, prob in zip(class_names, probabilities)}
            
            return prob_dict
            
        except Exception as e:
            logging.error(f"ECG prediction failed: {e}")
            raise
```

##### Signal Processing Pipeline
```python
class ECGPreprocessor:
    """Advanced ECG signal preprocessing pipeline"""
    
    def __init__(self, sampling_rate=250, target_length=15000):
        self.sampling_rate = sampling_rate
        self.target_length = target_length
    
    def preprocess(self, signal_data, header_data=None):
        """Complete preprocessing pipeline"""
        try:
            # 1. Load and validate ECG data
            signal = self._load_ecg_data(signal_data, header_data)
            
            # 2. Signal quality assessment
            if not self._assess_signal_quality(signal):
                logging.warning("Poor signal quality detected")
            
            # 3. Noise filtering
            signal = self._apply_filters(signal)
            
            # 4. Baseline correction
            signal = self._remove_baseline_wander(signal)
            
            # 5. Lead standardization
            signal = self._standardize_leads(signal)
            
            # 6. Duration normalization
            signal = self._normalize_duration(signal)
            
            # 7. Amplitude normalization
            signal = self._normalize_amplitude(signal)
            
            return signal
            
        except Exception as e:
            logging.error(f"ECG preprocessing failed: {e}")
            raise
    
    def _apply_filters(self, signal):
        """Apply bandpass filtering to remove noise"""
        from scipy import signal as scipy_signal
        
        # Design bandpass filter (0.5-40 Hz for ECG)
        nyquist = self.sampling_rate / 2
        low_freq = 0.5 / nyquist
        high_freq = 40.0 / nyquist
        
        b, a = scipy_signal.butter(4, [low_freq, high_freq], btype='band')
        
        # Apply filter to each lead
        filtered_signal = np.zeros_like(signal)
        for lead in range(signal.shape[0]):
            filtered_signal[lead, :] = scipy_signal.filtfilt(b, a, signal[lead, :])
        
        return filtered_signal
    
    def _remove_baseline_wander(self, signal):
        """Remove baseline wander using high-pass filtering"""
        from scipy import signal as scipy_signal
        
        # High-pass filter at 0.5 Hz
        nyquist = self.sampling_rate / 2
        high_freq = 0.5 / nyquist
        
        b, a = scipy_signal.butter(2, high_freq, btype='high')
        
        corrected_signal = np.zeros_like(signal)
        for lead in range(signal.shape[0]):
            corrected_signal[lead, :] = scipy_signal.filtfilt(b, a, signal[lead, :])
        
        return corrected_signal
    
    def _normalize_duration(self, signal):
        """Normalize signal duration to target length"""
        current_length = signal.shape[1]
        
        if current_length == self.target_length:
            return signal
        elif current_length > self.target_length:
            # Truncate from the end (keep most recent data)
            return signal[:, -self.target_length:]
        else:
            # Zero-pad at the beginning
            padded_signal = np.zeros((signal.shape[0], self.target_length))
            padded_signal[:, -current_length:] = signal
            return padded_signal
```

### 4. Security Architecture

#### Authentication and Authorization

##### Role-Based Access Control (RBAC)
```python
class RoleManager:
    """Advanced role-based access control system"""
    
    ROLES = {
        'doctor': {
            'permissions': [
                'view_patients', 'create_patients', 'edit_patients',
                'view_visits', 'create_visits', 'edit_visits',
                'analyze_ecg', 'prescribe_medications',
                'view_ecg_history', 'export_data'
            ],
            'description': 'Full access to patient management and ECG analysis'
        },
        'assistant': {
            'permissions': [
                'view_patients', 'create_patients', 'edit_patients',
                'view_visits', 'create_visits',
                'schedule_appointments', 'manage_documents'
            ],
            'description': 'Patient management and administrative tasks'
        }
    }
    
    @staticmethod
    def has_permission(user, permission):
        """Check if user has specific permission"""
        if not user or not user.is_authenticated:
            return False
        
        user_permissions = RoleManager.ROLES.get(user.role, {}).get('permissions', [])
        return permission in user_permissions
    
    @staticmethod
    def require_permission(permission):
        """Decorator for permission-based route protection"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if not RoleManager.has_permission(current_user, permission):
                    abort(403)
                return f(*args, **kwargs)
            return decorated_function
        return decorator
```

##### Session Management
```python
class SecureSessionManager:
    """Enhanced session security with timeout and validation"""
    
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize secure session management"""
        app.permanent_session_lifetime = timedelta(hours=8)  # 8-hour session timeout
        
        @app.before_request
        def validate_session():
            """Validate session on each request"""
            if current_user.is_authenticated:
                # Check session timeout
                if self._is_session_expired():
                    logout_user()
                    flash('Session expired. Please log in again.', 'warning')
                    return redirect(url_for('login'))
                
                # Update last activity
                session['last_activity'] = datetime.utcnow().timestamp()
    
    def _is_session_expired(self):
        """Check if current session has expired"""
        last_activity = session.get('last_activity')
        if not last_activity:
            return True
        
        timeout_seconds = self.app.permanent_session_lifetime.total_seconds()
        return (datetime.utcnow().timestamp() - last_activity) > timeout_seconds
```

#### Data Encryption and Privacy

##### File Upload Security
```python
class SecureFileHandler:
    """Secure file upload and storage management"""
    
    ALLOWED_EXTENSIONS = {
        'ecg': {'mat', 'hea'},
        'document': {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}
    }
    
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
    
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        os.makedirs(upload_folder, exist_ok=True)
    
    def validate_file(self, file, file_type='document'):
        """Comprehensive file validation"""
        if not file or not file.filename:
            raise ValueError("No file provided")
        
        # Check file extension
        if not self._allowed_file(file.filename, file_type):
            raise ValueError(f"File type not allowed for {file_type}")
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > self.MAX_FILE_SIZE:
            raise ValueError(f"File too large: {file_size} bytes")
        
        # Validate file content (basic magic number check)
        if not self._validate_file_content(file, file_type):
            raise ValueError("File content validation failed")
        
        return True
    
    def secure_save(self, file, subfolder='', filename=None):
        """Securely save file with virus scanning"""
        try:
            # Generate secure filename
            if not filename:
                filename = self._generate_secure_filename(file.filename)
            
            # Create full path
            save_path = os.path.join(self.upload_folder, subfolder)
            os.makedirs(save_path, exist_ok=True)
            
            full_path = os.path.join(save_path, filename)
            
            # Save file
            file.save(full_path)
            
            # Set secure file permissions
            os.chmod(full_path, 0o644)
            
            return full_path
            
        except Exception as e:
            logging.error(f"File save failed: {e}")
            raise
    
    def _generate_secure_filename(self, original_filename):
        """Generate cryptographically secure filename"""
        import secrets
        import string
        
        # Extract file extension
        _, ext = os.path.splitext(original_filename)
        
        # Generate random filename
        alphabet = string.ascii_letters + string.digits
        random_name = ''.join(secrets.choice(alphabet) for _ in range(16))
        
        return f"{random_name}{ext}"
```

### 5. API Architecture

#### RESTful API Design

##### API Blueprint Structure
```python
# api/__init__.py
from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

from . import patients, visits, ecg, auth

# api/patients.py
class PatientAPI:
    """RESTful Patient API with comprehensive CRUD operations"""
    
    @api_bp.route('/patients', methods=['GET'])
    @require_api_auth
    @require_permission('view_patients')
    def get_patients():
        """Get paginated list of patients with search functionality"""
        try:
            # Parse query parameters
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', 10, type=int), 100)
            search = request.args.get('search', '')
            
            # Build query
            query = Patient.query
            
            if search:
                search_filter = or_(
                    Patient.first_name.ilike(f'%{search}%'),
                    Patient.last_name.ilike(f'%{search}%'),
                    Patient.email.ilike(f'%{search}%')
                )
                query = query.filter(search_filter)
            
            # Execute paginated query
            patients = query.order_by(Patient.created_at.desc()).paginate(
                page=page, per_page=per_page, error_out=False
            )
            
            # Serialize response
            response_data = {
                'patients': [patient.to_dict() for patient in patients.items],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': patients.total,
                    'pages': patients.pages,
                    'has_next': patients.has_next,
                    'has_prev': patients.has_prev
                }
            }
            
            return jsonify(response_data), 200
            
        except Exception as e:
            logging.error(f"API error in get_patients: {e}")
            return jsonify({'error': 'Internal server error'}), 500
```

##### API Authentication
```python
class APIAuthManager:
    """JWT-based API authentication"""
    
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize API authentication"""
        app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', app.config['SECRET_KEY'])
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
        
    def generate_token(self, user):
        """Generate JWT token for user"""
        payload = {
            'user_id': user.id,
            'username': user.username,
            'role': user.role,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }
        
        return jwt.encode(payload, self.app.config['JWT_SECRET_KEY'], algorithm='HS256')
    
    def verify_token(self, token):
        """Verify JWT token and return user"""
        try:
            payload = jwt.decode(token, self.app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            user = User.query.get(payload['user_id'])
            return user
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

def require_api_auth(f):
    """Decorator for API authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return jsonify({'error': 'Authentication token required'}), 401
        
        user = api_auth_manager.verify_token(token)
        if not user:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Set user context for the request
        g.current_user = user
        return f(*args, **kwargs)
    
    return decorated_function
```

### 6. Frontend Architecture

#### Modern Web Stack

##### JavaScript Architecture
```javascript
// static/js/core/app.js
class HearlineApp {
    constructor() {
        this.modules = new Map();
        this.eventBus = new EventBus();
        this.apiClient = new APIClient();
        this.init();
    }
    
    init() {
        // Initialize core modules
        this.loadModule('ecg', new ECGAnalysisModule());
        this.loadModule('patients', new PatientManagementModule());
        this.loadModule('forms', new FormHandlerModule());
        
        // Setup global event listeners
        this.setupGlobalEvents();
        
        // Initialize UI components
        this.initializeUI();
    }
    
    loadModule(name, module) {
        this.modules.set(name, module);
        module.init(this.eventBus, this.apiClient);
    }
    
    setupGlobalEvents() {
        // Handle global errors
        window.addEventListener('error', (event) => {
            console.error('Global error:', event.error);
            this.showNotification('An unexpected error occurred', 'error');
        });
        
        // Handle unhandled promise rejections
        window.addEventListener('unhandledrejection', (event) => {
            console.error('Unhandled promise rejection:', event.reason);
            this.showNotification('A network error occurred', 'error');
        });
    }
}

// static/js/modules/ecg-analysis.js
class ECGAnalysisModule {
    constructor() {
        this.currentAnalysis = null;
        this.waveformChart = null;
    }
    
    init(eventBus, apiClient) {
        this.eventBus = eventBus;
        this.apiClient = apiClient;
        this.setupEventListeners();
    }
    
    async analyzeECG(matFile, heaFile) {
        try {
            this.showAnalysisLoading();
            
            const formData = new FormData();
            formData.append('mat_file', matFile);
            formData.append('hea_file', heaFile);
            
            const response = await this.apiClient.post('/analyze_ecg', formData);
            
            if (response.success) {
                this.displayAnalysisResults(response);
                this.eventBus.emit('ecg:analysis-complete', response);
            } else {
                throw new Error(response.error || 'Analysis failed');
            }
            
        } catch (error) {
            this.showAnalysisError(error.message);
            this.eventBus.emit('ecg:analysis-error', error);
        } finally {
            this.hideAnalysisLoading();
        }
    }
    
    displayAnalysisResults(analysisData) {
        const resultsContainer = document.getElementById('ecg-analysis-results');
        
        const template = `
            <div class="analysis-results">
                <div class="primary-diagnosis">
                    <h4>${analysisData.primary_diagnosis.name}</h4>
                    <div class="confidence-score">${(analysisData.primary_diagnosis.probability * 100).toFixed(1)}%</div>
                </div>
                <div class="detailed-probabilities">
                    ${this.renderProbabilityBars(analysisData.probabilities)}
                </div>
            </div>
        `;
        
        resultsContainer.innerHTML = template;
        this.animateResults();
    }
}
```

##### CSS Architecture
```scss
// static/css/core/_variables.scss
:root {
    // Color palette
    --primary-color: #007bff;
    --secondary-color: #6c757d;
    --success-color: #28a745;
    --warning-color: #ffc107;
    --danger-color: #dc3545;
    --info-color: #17a2b8;
    
    // Healthcare-specific colors
    --ecg-normal: #28a745;
    --ecg-warning: #ffc107;
    --ecg-critical: #dc3545;
    --ecg-background: #f8f9fa;
    
    // Typography
    --font-family-base: 'Segoe UI', system-ui, sans-serif;
    --font-size-base: 1rem;
    --line-height-base: 1.5;
    
    // Spacing
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 3rem;
    
    // Breakpoints
    --breakpoint-sm: 576px;
    --breakpoint-md: 768px;
    --breakpoint-lg: 992px;
    --breakpoint-xl: 1200px;
}

// static/css/components/_ecg-analysis.scss
.ecg-analysis-container {
    background: var(--ecg-background);
    border-radius: 8px;
    padding: var(--spacing-lg);
    margin-bottom: var(--spacing-lg);
    
    .analysis-results {
        .primary-diagnosis {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: var(--spacing-md);
            background: white;
            border-radius: 6px;
            margin-bottom: var(--spacing-md);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            
            h4 {
                margin: 0;
                color: var(--primary-color);
                font-weight: 600;
            }
            
            .confidence-score {
                font-size: 1.25rem;
                font-weight: bold;
                padding: var(--spacing-sm) var(--spacing-md);
                border-radius: 20px;
                
                &.high-confidence {
                    background: var(--ecg-normal);
                    color: white;
                }
                
                &.medium-confidence {
                    background: var(--ecg-warning);
                    color: #333;
                }
                
                &.low-confidence {
                    background: var(--ecg-critical);
                    color: white;
                }
            }
        }
        
        .probability-bars {
            .probability-item {
                display: flex;
                align-items: center;
                margin-bottom: var(--spacing-sm);
                
                .condition-name {
                    min-width: 200px;
                    font-weight: 500;
                }
                
                .probability-bar {
                    flex-grow: 1;
                    height: 24px;
                    background: #e9ecef;
                    border-radius: 12px;
                    overflow: hidden;
                    margin: 0 var(--spacing-md);
                    
                    .probability-fill {
                        height: 100%;
                        background: linear-gradient(90deg, var(--primary-color), var(--info-color));
                        border-radius: 12px;
                        transition: width 0.8s ease-in-out;
                    }
                }
                
                .probability-value {
                    min-width: 60px;
                    text-align: right;
                    font-weight: 600;
                }
            }
        }
    }
}
```

### 7. Performance Optimization

#### Caching Strategy

##### Multi-Level Caching
```python
class CacheManager:
    """Multi-level caching system for performance optimization"""
    
    def __init__(self, app=None):
        self.app = app
        self.redis_client = None
        self.memory_cache = {}
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize caching system"""
        # Redis configuration
        redis_url = app.config.get('REDIS_URL', 'redis://localhost:6379/0')
        try:
            import redis
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            self.redis_client.ping()  # Test connection
        except:
            logging.warning("Redis not available, using memory cache only")
    
    def get(self, key, default=None):
        """Get value from cache with fallback hierarchy"""
        # 1. Try memory cache first (fastest)
        if key in self.memory_cache:
            return self.memory_cache[key]['value']
        
        # 2. Try Redis cache
        if self.redis_client:
            try:
                value = self.redis_client.get(key)
                if value:
                    import json
                    parsed_value = json.loads(value)
                    # Store in memory cache for next access
                    self.memory_cache[key] = {
                        'value': parsed_value,
                        'timestamp': time.time()
                    }
                    return parsed_value
            except Exception as e:
                logging.error(f"Redis cache error: {e}")
        
        return default
    
    def set(self, key, value, ttl=3600):
        """Set value in all cache levels"""
        # Store in memory cache
        self.memory_cache[key] = {
            'value': value,
            'timestamp': time.time()
        }
        
        # Store in Redis cache
        if self.redis_client:
            try:
                import json
                self.redis_client.setex(key, ttl, json.dumps(value))
            except Exception as e:
                logging.error(f"Redis cache set error: {e}")
    
    def cache_ecg_analysis(self, visit_id, analysis_result):
        """Cache ECG analysis results"""
        cache_key = f"ecg_analysis:{visit_id}"
        self.set(cache_key, analysis_result, ttl=86400)  # 24 hours
    
    def get_cached_ecg_analysis(self, visit_id):
        """Get cached ECG analysis"""
        cache_key = f"ecg_analysis:{visit_id}"
        return self.get(cache_key)
```

#### Database Query Optimization
```python
class QueryOptimizer:
    """Database query optimization utilities"""
    
    @staticmethod
    def get_patient_with_visits(patient_id, limit=10):
        """Optimized patient query with visit data"""
        return db.session.query(Patient).options(
            joinedload(Patient.visits.and_(
                Visit.visit_date >= datetime.utcnow() - timedelta(days=365)
            )).options(
                joinedload(Visit.prescriptions).joinedload(Prescription.medicament)
            )
        ).filter(Patient.id == patient_id).first()
    
    @staticmethod
    def get_ecg_history_paginated(page=1, per_page=20, filters=None):
        """Optimized ECG history query with filtering"""
        query = db.session.query(Visit).options(
            joinedload(Visit.patient)
        ).filter(
            Visit.ecg_prediction.isnot(None)
        )
        
        # Apply filters
        if filters:
            if filters.get('patient_name'):
                query = query.join(Patient).filter(
                    or_(
                        Patient.first_name.ilike(f"%{filters['patient_name']}%"),
                        Patient.last_name.ilike(f"%{filters['patient_name']}%")
                    )
                )
            
            if filters.get('date_from'):
                query = query.filter(Visit.visit_date >= filters['date_from'])
            
            if filters.get('date_to'):
                query = query.filter(Visit.visit_date <= filters['date_to'])
        
        return query.order_by(Visit.visit_date.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
```

### 8. Monitoring and Logging

#### Application Monitoring
```python
class ApplicationMonitor:
    """Comprehensive application monitoring and metrics"""
    
    def __init__(self, app=None):
        self.app = app
        self.metrics = {
            'requests_total': 0,
            'ecg_analyses_total': 0,
            'error_count': 0,
            'response_times': []
        }
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize monitoring"""
        @app.before_request
        def before_request():
            g.start_time = time.time()
            self.metrics['requests_total'] += 1
        
        @app.after_request
        def after_request(response):
            response_time = time.time() - g.start_time
            self.metrics['response_times'].append(response_time)
            
            # Keep only last 1000 response times
            if len(self.metrics['response_times']) > 1000:
                self.metrics['response_times'] = self.metrics['response_times'][-1000:]
            
            # Log slow requests
            if response_time > 5.0:
                logging.warning(f"Slow request: {request.endpoint} took {response_time:.2f}s")
            
            return response
        
        @app.errorhandler(500)
        def handle_500_error(error):
            self.metrics['error_count'] += 1
            logging.error(f"Server error: {error}")
            return render_template('errors/500.html'), 500
    
    def get_health_status(self):
        """Get application health status"""
        return {
            'status': 'healthy',
            'metrics': {
                'total_requests': self.metrics['requests_total'],
                'total_ecg_analyses': self.metrics['ecg_analyses_total'],
                'error_count': self.metrics['error_count'],
                'avg_response_time': np.mean(self.metrics['response_times']) if self.metrics['response_times'] else 0
            },
            'timestamp': datetime.utcnow().isoformat()
        }
```

### 9. Deployment Architecture

#### Container Configuration
```dockerfile
# Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash hearline
RUN chown -R hearline:hearline /app
USER hearline

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Start application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

#### Kubernetes Deployment
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hearline-webapp
  labels:
    app: hearline-webapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hearline-webapp
  template:
    metadata:
      labels:
        app: hearline-webapp
    spec:
      containers:
      - name: hearline-webapp
        image: hearline/webapp:latest
        ports:
        - containerPort: 5000
        env:
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: hearline-secrets
              key: db-host
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: hearline-secrets
              key: db-password
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Scalability Considerations

### Horizontal Scaling

#### Load Balancing Strategy
- **Application Servers**: Multiple Flask instances behind Nginx
- **Database**: Read replicas for reporting queries
- **File Storage**: Distributed storage with CDN integration
- **Caching**: Redis cluster for distributed caching

#### Auto-scaling Configuration
```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: hearline-webapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: hearline-webapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## Conclusion

The Hearline Webapp technical architecture represents a modern, scalable, and secure approach to healthcare application development. By leveraging cutting-edge technologies and best practices, the system delivers high-performance AI-powered ECG analysis while maintaining the flexibility and reliability required for critical healthcare applications.

The architecture's modular design ensures maintainability and extensibility, while the comprehensive security framework protects sensitive patient data. Performance optimizations and caching strategies enable the system to scale efficiently as demand grows.

This technical foundation supports the application's primary goal of revolutionizing cardiac care through AI-powered diagnosis while providing healthcare professionals with an intuitive, reliable, and comprehensive patient management platform.

---

*Technical Architecture Document - Hearline Webapp v2.0*  
*Last Updated: June 2025*  
*Document Classification: Technical Reference*
