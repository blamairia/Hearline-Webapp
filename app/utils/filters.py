# app/utils/filters.py

import os


def register_template_filters(app):
    """Register custom Jinja2 template filters."""
    
    @app.template_filter('basename')
    def basename_filter(path):
        """Extract filename from path."""
        if path:
            return os.path.basename(path)
        return ''
