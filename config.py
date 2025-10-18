"""Configuration management for E-Paper Dashboard"""
import os


class Config:
    """Base configuration"""
    # Flask settings
    DEBUG = False
    TESTING = False
    JSON_AS_ASCII = False
    
    # Plugin settings
    PLUGIN_DIR = 'plugins'
    
    # Image settings
    DEFAULT_IMAGE_FORMAT = 'JPEG'
    DEFAULT_IMAGE_QUALITY = 95
    DEFAULT_IMAGE_SUBSAMPLING = 0  # 4:4:4
    
    # Asset paths
    ASSET_DIR = 'assets'
    FONT_PATH = os.path.join(ASSET_DIR, 'simhei.ttf')
    ICON_FONT_PATH = os.path.join(ASSET_DIR, 'weather-icon.ttf')
    LOGO_PATH = os.path.join(ASSET_DIR, 'logo')
    
    # Data paths
    DATA_DIR = 'data'
    COURSE_DATA_PATH = os.path.join(DATA_DIR, 'course.json')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    """
    Get configuration by name
    
    Args:
        config_name: Configuration name ('development', 'production', 'testing')
        
    Returns:
        Configuration class
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    return config.get(config_name, config['default'])
