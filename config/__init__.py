"""
Configuration module
"""
from config.firebase_config import initialize_firebase, get_firestore_client

__all__ = ['initialize_firebase', 'get_firestore_client']

