"""
E-Paper Dashboard API Server
A modular plugin-based Flask application for generating e-paper display content
"""
import sys
sys.dont_write_bytecode = True

from flask import Flask, send_from_directory, render_template
from core.plugin_manager import PluginManager
from config import get_config
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask application
app = Flask(__name__)

# Load configuration
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(get_config(config_name))
logger.info(f"Loaded configuration: {config_name}")

# Initialize plugin manager
plugin_manager = PluginManager(app)

# Discover and register all plugins
logger.info("Starting plugin discovery...")
registered_count = plugin_manager.load_all_plugins('plugins')
logger.info(f"Plugin registration complete: {registered_count} plugins registered")

# Static routes
@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return send_from_directory('assets/logo', 'logo.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def home():
    """Serve home page"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'plugins_loaded': len(plugin_manager.plugins)
    }

if __name__ == '__main__':
    # Production environment
    app.run(debug=True)
    # For testing on network
    # app.run(host='0.0.0.0', port=5000, debug=True)
