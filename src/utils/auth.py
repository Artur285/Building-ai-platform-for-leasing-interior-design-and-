"""
Authentication and authorization utilities.
"""
import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Dict, Optional
import os

class AuthManager:
    """
    Handles user authentication and JWT token management.
    """
    
    def __init__(self):
        """Initialize the auth manager."""
        self.secret_key = os.getenv('JWT_SECRET', 'default-secret-key')
        self.expiration = os.getenv('JWT_EXPIRATION', '24h')
    
    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password
        
        Returns:
            Hashed password
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password: Plain text password
            hashed: Hashed password
        
        Returns:
            True if password matches, False otherwise
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def generate_token(self, user_id: str, email: str) -> str:
        """
        Generate a JWT token for a user.
        
        Args:
            user_id: User ID
            email: User email
        
        Returns:
            JWT token string
        """
        payload = {
            'user_id': user_id,
            'email': email,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """
        Verify and decode a JWT token.
        
        Args:
            token: JWT token string
        
        Returns:
            Decoded payload or None if invalid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
