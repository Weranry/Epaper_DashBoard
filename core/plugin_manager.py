"""Plugin manager for automatic blueprint discovery and registration"""
import os
import importlib
import logging
from flask import Blueprint

logger = logging.getLogger(__name__)


class PluginManager:
    """Manages plugin discovery and registration"""
    
    def __init__(self, app=None):
        self.app = app
        self.plugins = []
        
    def init_app(self, app):
        """Initialize plugin manager with Flask app"""
        self.app = app
        
    def discover_plugins(self, plugin_dir='plugins'):
        """
        Discover all plugins in the plugins directory
        
        Args:
            plugin_dir: Directory containing plugins
            
        Returns:
            List of discovered plugin modules
        """
        plugins = []
        
        if not os.path.exists(plugin_dir):
            logger.warning(f"Plugin directory {plugin_dir} does not exist")
            return plugins
        
        for item in os.listdir(plugin_dir):
            item_path = os.path.join(plugin_dir, item)
            
            # Check if it's a directory with __init__.py (package)
            if os.path.isdir(item_path):
                init_file = os.path.join(item_path, '__init__.py')
                if os.path.exists(init_file):
                    plugins.append(item)
                    
        return plugins
    
    def load_plugin(self, plugin_name, plugin_dir='plugins'):
        """
        Load a single plugin module
        
        Args:
            plugin_name: Name of the plugin
            plugin_dir: Directory containing plugins
            
        Returns:
            Loaded plugin module or None
        """
        try:
            module_path = f"{plugin_dir}.{plugin_name}"
            plugin_module = importlib.import_module(module_path)
            logger.info(f"Loaded plugin: {plugin_name}")
            return plugin_module
        except Exception as e:
            logger.error(f"Failed to load plugin {plugin_name}: {e}")
            return None
    
    def register_plugin(self, plugin_module):
        """
        Register a plugin's blueprint with the Flask app
        
        Args:
            plugin_module: The plugin module to register
            
        Returns:
            bool: True if registration successful
        """
        if not hasattr(plugin_module, 'blueprint'):
            logger.warning(f"Plugin {plugin_module.__name__} has no blueprint attribute")
            return False
        
        blueprint = plugin_module.blueprint
        
        if not isinstance(blueprint, Blueprint):
            logger.warning(f"Plugin {plugin_module.__name__} blueprint is not a Flask Blueprint")
            return False
        
        try:
            self.app.register_blueprint(blueprint)
            self.plugins.append(plugin_module)
            logger.info(f"Registered blueprint: {blueprint.name}")
            return True
        except Exception as e:
            logger.error(f"Failed to register blueprint {blueprint.name}: {e}")
            return False
    
    def load_all_plugins(self, plugin_dir='plugins'):
        """
        Discover and load all plugins
        
        Args:
            plugin_dir: Directory containing plugins
            
        Returns:
            int: Number of plugins successfully registered
        """
        plugin_names = self.discover_plugins(plugin_dir)
        registered_count = 0
        
        for plugin_name in plugin_names:
            plugin_module = self.load_plugin(plugin_name, plugin_dir)
            if plugin_module:
                if self.register_plugin(plugin_module):
                    registered_count += 1
        
        logger.info(f"Registered {registered_count}/{len(plugin_names)} plugins")
        return registered_count
