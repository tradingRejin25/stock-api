"""
Firebase configuration and initialization
"""
import os
import firebase_admin
from firebase_admin import credentials, firestore
from typing import Optional

# Global Firestore client
_db: Optional[firestore.Client] = None


def initialize_firebase(credential_path: Optional[str] = None, project_id: Optional[str] = None):
    """
    Initialize Firebase Admin SDK
    
    Args:
        credential_path: Path to Firebase service account JSON file.
                        If not provided, looks for:
                        1. FIREBASE_CREDENTIALS environment variable
                        2. firebase-credentials.json in project root
        project_id: Firebase project ID. If not provided, uses:
                   1. FIREBASE_PROJECT_ID environment variable
                   2. Default project from credentials
    """
    global _db
    
    if firebase_admin._apps:
        # Already initialized
        _db = firestore.client()
        return _db
    
    # Determine credential path
    if not credential_path:
        credential_path = os.getenv('FIREBASE_CREDENTIALS')
        if not credential_path:
            # Try default location
            import pathlib
            project_root = pathlib.Path(__file__).parent.parent
            default_path = project_root / 'firebase-credentials.json'
            if default_path.exists():
                credential_path = str(default_path)
    
    # Determine project ID
    if not project_id:
        project_id = os.getenv('FIREBASE_PROJECT_ID')
    
    # Initialize Firebase
    if credential_path and os.path.exists(credential_path):
        cred = credentials.Certificate(credential_path)
        if project_id:
            firebase_admin.initialize_app(cred, {'projectId': project_id})
        else:
            firebase_admin.initialize_app(cred)
    else:
        # Try to use default credentials (for Google Cloud environments)
        try:
            if project_id:
                firebase_admin.initialize_app(options={'projectId': project_id})
            else:
                firebase_admin.initialize_app()
        except Exception as e:
            raise Exception(
                f"Failed to initialize Firebase. Please provide credentials file or set up default credentials. "
                f"Error: {str(e)}"
            )
    
    _db = firestore.client()
    return _db


def get_firestore_client() -> firestore.Client:
    """
    Get Firestore client instance
    Initializes Firebase if not already initialized
    """
    global _db
    
    if _db is None:
        initialize_firebase()
    
    return _db

