"""Configuration settings for the AI Building Materials Leasing Platform."""
import os
from pathlib import Path

basedir = Path(__file__).parent.absolute()


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{basedir / "materials_leasing.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AI Model settings
    MODEL_PATH = basedir / 'models'
    RECOMMENDATION_MODEL = 'material_recommender.pkl'
    
    # Application settings
    ITEMS_PER_PAGE = 20
    MAX_LEASE_DURATION_DAYS = 365
