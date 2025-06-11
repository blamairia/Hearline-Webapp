# app/decorators/auth.py

from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def role_required(allowed_roles):
    """Decorator to require specific roles for access."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))
            
            if isinstance(allowed_roles, str):
                allowed_roles_list = [allowed_roles]
            else:
                allowed_roles_list = allowed_roles
            
            if current_user.role not in allowed_roles_list:
                flash('You do not have permission to access this page.', 'error')
                return redirect(url_for('dashboard.index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def doctor_required(f):
    """Decorator to require doctor role."""
    return role_required('doctor')(f)


def assistant_required(f):
    """Decorator to require assistant role."""
    return role_required('assistant')(f)


def any_role_required(f):
    """Decorator to require any authenticated user."""
    return role_required(['doctor', 'assistant'])(f)
