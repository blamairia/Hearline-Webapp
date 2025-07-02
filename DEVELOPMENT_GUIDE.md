# HeartLine Development Guide

## Real-time Development with Auto-reload

### Option 1: Modified app.py (Current Setup) ✅
Your `app.py` now has `debug=True` enabled. Simply run:
```bash
python app.py
```

**What this enables:**
- ✅ Auto-reload on HTML/CSS/JS changes
- ✅ Auto-reload on Python code changes  
- ✅ Detailed error messages in browser
- ✅ Interactive debugger

### Option 2: Using Flask CLI (Recommended for Production-like Development)
```bash
# Install python-dotenv if not already installed
pip install python-dotenv

# Run using Flask CLI
flask run
```

### Option 3: Development Script
```bash
python run_dev.py
```

## What Files Auto-reload?

### ✅ Files that trigger auto-reload:
- `templates/*.html` (Jinja2 templates)
- `static/css/*.css` (Stylesheets)
- `static/js/*.js` (JavaScript files)
- `*.py` (Python source files)
- `models.py`, `forms.py`, etc.

### ❌ Files that require manual restart:
- `.env` files (environment variables)
- Database schema changes (migrations)
- New package installations

## Development Workflow

1. **Start the development server:**
   ```bash
   python app.py
   ```

2. **Make changes to HTML/CSS/JS:**
   - Edit files in `templates/` or `static/`
   - Save the file
   - Refresh your browser (F5) - changes appear immediately!

3. **Make changes to Python code:**
   - Edit `app.py`, `models.py`, etc.
   - Save the file
   - Flask automatically restarts the server
   - Refresh your browser to see changes

## Browser Development Tools

### Enable Live Reload in Browser:
1. **Chrome**: Press F12 → Sources tab → Enable "Auto-reload"
2. **Firefox**: Press F12 → Settings → Check "Auto Refresh"
3. **Edge**: Press F12 → Sources → Enable "Auto-reload"

### Browser Extensions for Enhanced Development:
- **Live Reload** (Chrome/Firefox)
- **Flask Debug Toolbar** (shows SQL queries, template info)

## Hot Tips for Rapid UI Development

### 1. Use Browser DevTools for Real-time CSS Testing:
```html
<!-- In your templates, you can test CSS changes live -->
<style>
  /* Temporary CSS for testing */
  .sidebar { background: red !important; }
</style>
```

### 2. Template Caching (for faster development):
```python
# Add to app.py for instant template updates
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True
```

### 3. Static File Caching:
```html
<!-- Force browser to reload CSS/JS files -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}?v={{ moment().unix() }}">
```

## Debugging Features Available

With `debug=True`, you get:
- 📊 **Interactive Debugger**: Click on error traces to inspect variables
- 🔍 **Detailed Error Pages**: See exactly what went wrong
- 📋 **Console Logging**: All `print()` statements show in terminal
- 🔄 **Auto-reload**: Changes appear without manual restart

## Current Status: ✅ READY FOR REAL-TIME DEVELOPMENT

Your HeartLine app is now configured for optimal development experience!

**Next Steps:**
1. Run: `python app.py`
2. Open: http://127.0.0.1:5000
3. Edit any template file
4. Save and refresh browser
5. See changes immediately! 🚀
