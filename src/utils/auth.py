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
        self.secret_key = os.getenv('JWT_SECRET')
        if not self.secret_key:
            raise ValueError(
                "JWT_SECRET environment variable must be set. "
                "Generate a secure key with: python -c 'import secrets; print(secrets.token_hex(32))'"
            )
        # Parse JWT_EXPIRATION (format: "24h", "7d", etc.)
        expiration_str = os.getenv('JWT_EXPIRATION', '24h')
        self.expiration_hours = self._parse_expiration(expiration_str)
    
    def _parse_expiration(self, expiration_str: str) -> int:
        """
        Parse expiration string to hours.
        
        Args:
            expiration_str: Expiration string (e.g., "24h", "7d")
        
        Returns:
            Number of hours
        """
        if expiration_str.endswith('h'):
            return int(expiration_str[:-1])
        elif expiration_str.endswith('d'):
            return int(expiration_str[:-1]) * 24
        else:
            return 24  # Default to 24 hours
    
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
            'exp': datetime.utcnow() + timedelta(hours=self.expiration_hours)
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
