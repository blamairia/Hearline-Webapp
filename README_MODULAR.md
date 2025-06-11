# Heartline Medical Clinic - Modular Architecture

This is the refactored version of the Heartline Medical Clinic web application, following clean code architecture principles and best practices.

## Architecture Overview

The application has been completely restructured from a monolithic `app.py` file into a modular, maintainable architecture:

```
app/
├── __init__.py              # Application factory
├── config.py                # Configuration settings
├── extensions.py            # Flask extensions initialization
├── decorators/              # Custom decorators
│   ├── __init__.py
│   └── auth.py             # Authentication decorators
├── models/                  # Database models
│   ├── __init__.py
│   ├── patient.py
│   ├── doctor.py
│   ├── appointment.py
│   ├── visit.py
│   ├── prescription.py
│   ├── user.py
│   ├── settings.py
│   └── waiting_list.py
├── routes/                  # Route blueprints
│   ├── __init__.py
│   ├── main.py             # Main routes
│   ├── auth.py             # Authentication routes
│   ├── dashboard.py        # Dashboard routes
│   ├── patients.py         # Patient management
│   ├── visits.py           # Visit management
│   ├── appointments.py     # Appointment management
│   ├── ecg.py              # ECG-related routes
│   └── api.py              # API endpoints
├── services/                # Business logic services
│   ├── __init__.py
│   ├── ecg_service.py      # ECG analysis service
│   ├── patient_service.py  # Patient operations
│   └── visit_service.py    # Visit operations
├── forms/                   # WTForms
│   ├── __init__.py
│   ├── auth_forms.py
│   ├── patient_forms.py
│   ├── visit_forms.py
│   └── appointment_forms.py
└── utils/                   # Utility functions
    ├── __init__.py
    ├── filters.py          # Jinja2 filters
    └── helpers.py          # Helper functions
```

## Key Improvements

### 1. **Separation of Concerns**
- **Models**: Pure data models with minimal business logic
- **Services**: Business logic and complex operations
- **Routes**: HTTP request handling and routing
- **Forms**: Form validation and rendering

### 2. **Application Factory Pattern**
- Configurable application creation
- Better testing support
- Environment-specific configurations

### 3. **Blueprint Architecture**
- Modular route organization
- Better URL organization
- Easier maintenance and testing

### 4. **Service Layer**
- Centralized business logic
- Reusable operations
- Better error handling

### 5. **Configuration Management**
- Environment-based configuration
- Secure secrets management
- Easy deployment configuration

## Installation and Setup

### 1. Install Dependencies
```bash
pip install -r requirements_modular.txt
```

### 2. Environment Configuration
Create a `.env` file with your database configuration:
```
SECRET_KEY=your-secret-key-here
DB_HOST=your-database-host
DB_PORT=5432
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_NAME=your-database-name
```

### 3. Run the Application
```bash
python main.py
```

## Migration from Old Architecture

### Breaking Changes
1. **Import Paths**: All imports now use the new module structure
2. **URL Structure**: Some URLs now have blueprint prefixes:
   - `/auth/login` instead of `/login`
   - `/patients/new` instead of `/patient/new`
   - `/visits/new` instead of `/visit/new`
   - `/appointments/new` instead of `/appointment/new`

### Database Migration
The database schema remains the same, so no migration is needed for existing data.

### Template Updates
Templates may need minor updates to use the new URL structure:
```html
<!-- Old -->
<a href="{{ url_for('login') }}">Login</a>

<!-- New -->
<a href="{{ url_for('auth.login') }}">Login</a>
```

## Development Guidelines

### Adding New Features
1. **Models**: Add to appropriate model file in `app/models/`
2. **Business Logic**: Add to service layer in `app/services/`
3. **Routes**: Add to appropriate blueprint in `app/routes/`
4. **Forms**: Add to appropriate form file in `app/forms/`

### Code Organization
- Keep models lightweight with minimal business logic
- Put complex operations in service classes
- Use decorators for common functionality (auth, validation)
- Keep routes focused on HTTP handling

### Testing
The modular structure makes testing much easier:
- Unit test individual services
- Integration test routes with mock services
- Test models independently

## Benefits of the New Architecture

1. **Maintainability**: Easier to find and modify specific functionality
2. **Scalability**: Easy to add new features without affecting existing code
3. **Testability**: Isolated components are easier to test
4. **Reusability**: Services can be reused across different routes
5. **Team Development**: Multiple developers can work on different modules
6. **Performance**: Better code organization leads to more efficient imports

## File Structure Explanation

- **`main.py`**: Application entry point using factory pattern
- **`app/__init__.py`**: Application factory and blueprint registration
- **`app/config.py`**: Configuration classes for different environments
- **`app/extensions.py`**: Flask extension initialization
- **`app/models/`**: Database models with relationships
- **`app/services/`**: Business logic and complex operations
- **`app/routes/`**: Flask blueprints for different feature areas
- **`app/forms/`**: WTForms for form validation
- **`app/utils/`**: Utility functions and helpers
- **`app/decorators/`**: Custom decorators for common functionality

This architecture follows modern Flask best practices and is designed for long-term maintainability and scalability.
