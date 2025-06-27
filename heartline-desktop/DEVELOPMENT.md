# Heartline Desktop - Development Guide

## 🏗️ Architecture Overview

The Heartline Desktop application follows **Clean Architecture** principles with clear separation of concerns:

```
📁 Project Structure
├── src/
│   ├── core/           # Core configuration and infrastructure
│   ├── models/         # Database models (Domain layer)
│   ├── repositories/   # Data access layer (Infrastructure)
│   ├── services/       # Business logic layer (Application)
│   ├── ui/            # User interface (Presentation)
│   └── utils/         # Utilities and helpers
├── assets/            # Static assets (icons, images, themes)
├── models/            # AI models (ONNX files)
├── logs/             # Application logs
└── uploads/          # User uploaded files
```

## 🎯 Core Features Implementation

### 1. **Patient Management**
- **Models**: `Patient` with demographic and medical information
- **Repository**: CRUD operations with search and filtering
- **Service**: Business logic for patient validation and statistics
- **UI**: Material Design cards with advanced search

### 2. **ECG Analysis** 
- **Service**: ONNX Runtime integration for AI analysis
- **Models**: Same 9-class detection as web app
- **Processing**: Signal preprocessing and result formatting
- **UI**: File upload with real-time analysis results

### 3. **Appointment System**
- **Models**: `Appointment` with status tracking
- **Service**: Scheduling with conflict detection  
- **UI**: Calendar view with drag-and-drop

### 4. **Visit Documentation**
- **Models**: `Visit` with ECG integration
- **Service**: Complete visit workflow
- **UI**: Tabbed interface for all visit components

## 🛠️ Development Workflow

### **Phase 1: Core Foundation** ✅
- [x] Project structure and configuration
- [x] Database models and repositories
- [x] Core services (ECG analysis, patient management)
- [x] Main window and navigation
- [x] Material Design theme integration

### **Phase 2: UI Components** (Next)
- [ ] Complete patient management UI
- [ ] ECG analysis interface
- [ ] Appointment scheduler
- [ ] Visit documentation forms

### **Phase 3: Advanced Features**
- [ ] Real-time dashboard updates
- [ ] Report generation
- [ ] Data export/import
- [ ] User management

### **Phase 4: Polish & Deploy**
- [ ] Comprehensive testing
- [ ] Error handling
- [ ] Documentation
- [ ] Installer creation

## 🎨 UI Design Principles

### **Material Design Integration**
```python
# Theme Configuration
qt_material.apply_stylesheet(app, theme='dark_blue.xml')

# Custom Medical Theme Colors
PRIMARY_COLOR = "#2196F3"    # Blue
SUCCESS_COLOR = "#4CAF50"    # Green  
WARNING_COLOR = "#FF9800"    # Orange
DANGER_COLOR = "#F44336"     # Red
```

### **Component Structure**
- **Cards**: Patient information, statistics
- **Tables**: Data display with sorting/filtering
- **Forms**: Material input fields with validation
- **Dialogs**: Modal windows for data entry
- **Navigation**: Sidebar with collapsible sections

## 🗄️ Database Integration

### **Connection Management**
```python
# PostgreSQL with connection pooling
engine = create_engine(
    database_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)
```

### **Repository Pattern**
```python
# Base repository with generic CRUD
class BaseRepository(Generic[T]):
    def create(self, **kwargs) -> T
    def get_by_id(self, entity_id: int) -> Optional[T]
    def get_all(self) -> List[T]
    def update(self, entity_id: int, **kwargs) -> Optional[T]
    def delete(self, entity_id: int) -> bool
```

## 🧠 AI Integration

### **ECG Analysis Service**
```python
# ONNX Runtime integration
session = ort.InferenceSession(model_path)
predictions = session.run(None, {input_name: signal})

# 9-class cardiac condition detection
ECG_CLASSES = ["SNR", "AF", "IAVB", "LBBB", "RBBB", "PAC", "PVC", "STD", "STE"]
```

### **Signal Processing**
- **Input**: .mat and .hea files (PhysioNet format)
- **Preprocessing**: Normalization and fixed-length windowing
- **Output**: Confidence scores for all 9 conditions

## 🔧 Configuration Management

### **Environment Variables**
```bash
# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=heartline

# Application
ONNX_MODEL_PATH=models/resnet34_ecg.onnx
THEME=dark_blue.xml
LOG_LEVEL=INFO
```

### **Settings Class**
```python
class Settings(BaseSettings):
    # Pydantic-based configuration with type validation
    DB_HOST: str = "localhost"
    ONNX_MODEL_PATH: str = "models/resnet34_ecg.onnx"
    
    class Config:
        env_file = ".env"
```

## 🧪 Testing Strategy

### **Unit Tests**
```python
# Test structure
tests/
├── test_models/
├── test_repositories/  
├── test_services/
└── test_ui/
```

### **Integration Tests**
- Database connectivity
- ONNX model loading
- File upload/processing

### **UI Tests**
- Widget functionality
- Navigation flow
- Error handling

## 📦 Deployment

### **Requirements**
- Python 3.8+
- PyQt6 + Material Design
- PostgreSQL database
- ONNX Runtime

### **Installation Process**
1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure database in `.env`
4. Copy ONNX model to `models/`
5. Run setup: `python setup.py`
6. Launch app: `python main.py`

### **Distribution**
- **PyInstaller**: Create standalone executable
- **NSIS**: Windows installer
- **DMG**: macOS package
- **AppImage**: Linux portable

## 🔒 Security Considerations

### **Data Protection**
- Password hashing with bcrypt
- Session management
- Input validation and sanitization
- SQL injection prevention

### **File Security**
- Secure file upload with type validation
- Path traversal prevention
- File size limits

## 📊 Performance Optimization

### **Database**
- Connection pooling
- Query optimization
- Lazy loading for relationships

### **UI**
- Asynchronous operations
- Progressive loading
- Memory management

### **AI Processing**
- ONNX optimization
- Batch processing
- Caching strategies

## 🚀 Next Development Steps

1. **Complete Patient Management UI**
   - Advanced search with filters
   - Bulk operations
   - Data import/export

2. **ECG Analysis Interface**
   - File drag-and-drop
   - Real-time visualization
   - Historical comparison

3. **Appointment System**
   - Calendar integration
   - Recurring appointments
   - SMS/Email reminders

4. **Reporting System**
   - PDF generation
   - Custom templates
   - Statistical analysis

## 🤝 Contributing Guidelines

1. Follow Clean Architecture principles
2. Use type hints throughout
3. Write comprehensive tests
4. Document all public APIs
5. Follow Material Design guidelines
6. Maintain database compatibility with web app

---

**Heartline Desktop** - Building the future of healthcare management with modern technology and clean architecture.
