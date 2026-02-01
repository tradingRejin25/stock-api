"""
Service to load and provide Nifty stocks data from Firebase Firestore
"""
from typing import List, Optional
from pydantic import BaseModel
from config.firebase_config import get_firestore_client
from google.cloud.firestore import Client as FirestoreClient


class NiftyStock(BaseModel):
    """Model for Nifty stock details"""
    stockName: str
    nseCode: str
    isin: str

    class Config:
        json_schema_extra = {
            "example": {
                "stockName": "Reliance Industries Ltd",
                "nseCode": "RELIANCE",
                "isin": "INE467B01029"
            }
        }


class NiftyStocksService:
    """Service to load and query Nifty stocks from Firebase Firestore"""
    
    COLLECTION_NAME = "nifty_stocks"
    
    def __init__(self):
        """Initialize the service with Firebase Firestore"""
        self.db: FirestoreClient = get_firestore_client()
        self.collection = self.db.collection(self.COLLECTION_NAME)
    
    def _doc_to_stock(self, doc_id: str, doc_data: dict) -> NiftyStock:
        """Convert Firestore document to NiftyStock model"""
        return NiftyStock(
            stockName=doc_data.get('stockName', ''),
            nseCode=doc_data.get('nseCode', ''),
            isin=doc_data.get('isin', '')
        )
    
    def get_all_stocks(self) -> List[NiftyStock]:
        """Get all Nifty stocks from Firebase"""
        try:
            docs = self.collection.stream()
            stocks = []
            for doc in docs:
                stock_data = doc.to_dict()
                if stock_data:
                    stocks.append(self._doc_to_stock(doc.id, stock_data))
            return stocks
        except Exception as e:
            raise Exception(f"Failed to fetch stocks from Firebase: {str(e)}")
    
    def get_stock_by_nse_code(self, nse_code: str) -> Optional[NiftyStock]:
        """Get stock by NSE code from Firebase"""
        try:
            # Query by nseCode field
            query = self.collection.where('nseCode', '==', nse_code.upper()).limit(1)
            docs = list(query.stream())
            
            if docs:
                return self._doc_to_stock(docs[0].id, docs[0].to_dict())
            return None
        except Exception as e:
            raise Exception(f"Failed to fetch stock by NSE code from Firebase: {str(e)}")
    
    def get_stock_by_isin(self, isin: str) -> Optional[NiftyStock]:
        """Get stock by ISIN from Firebase"""
        try:
            # Query by isin field
            query = self.collection.where('isin', '==', isin.upper()).limit(1)
            docs = list(query.stream())
            
            if docs:
                return self._doc_to_stock(docs[0].id, docs[0].to_dict())
            return None
        except Exception as e:
            raise Exception(f"Failed to fetch stock by ISIN from Firebase: {str(e)}")
    
    def search_by_name(self, query: str) -> List[NiftyStock]:
        """Search stocks by name (case-insensitive partial match) from Firebase"""
        try:
            # Firestore doesn't support case-insensitive search natively
            # We'll fetch all and filter in memory (for small datasets)
            # For larger datasets, consider using Algolia or maintaining lowercase search fields
            all_stocks = self.get_all_stocks()
            query_lower = query.lower()
            return [
                s for s in all_stocks 
                if query_lower in s.stockName.lower()
            ]
        except Exception as e:
            raise Exception(f"Failed to search stocks from Firebase: {str(e)}")
    
    def save_stock(self, stock: NiftyStock) -> str:
        """
        Save or update a stock in Firebase
        Uses ISIN as document ID for uniqueness
        
        Returns:
            Document ID
        """
        try:
            doc_id = stock.isin.upper()
            doc_ref = self.collection.document(doc_id)
            doc_ref.set({
                'stockName': stock.stockName,
                'nseCode': stock.nseCode.upper(),
                'isin': stock.isin.upper()
            }, merge=True)
            return doc_id
        except Exception as e:
            raise Exception(f"Failed to save stock to Firebase: {str(e)}")
    
    def save_stocks_batch(self, stocks: List[NiftyStock]) -> int:
        """
        Save multiple stocks to Firebase in a batch
        
        Returns:
            Number of stocks saved
        """
        try:
            batch = self.db.batch()
            count = 0
            
            for stock in stocks:
                doc_id = stock.isin.upper()
                doc_ref = self.collection.document(doc_id)
                batch.set(doc_ref, {
                    'stockName': stock.stockName,
                    'nseCode': stock.nseCode.upper(),
                    'isin': stock.isin.upper()
                }, merge=True)
                count += 1
            
            batch.commit()
            return count
        except Exception as e:
            raise Exception(f"Failed to save stocks batch to Firebase: {str(e)}")
    
    def delete_stock(self, isin: str) -> bool:
        """
        Delete a stock from Firebase by ISIN
        
        Returns:
            True if deleted, False if not found
        """
        try:
            doc_ref = self.collection.document(isin.upper())
            doc = doc_ref.get()
            if doc.exists:
                doc_ref.delete()
                return True
            return False
        except Exception as e:
            raise Exception(f"Failed to delete stock from Firebase: {str(e)}")


# Singleton instance
_nifty_stocks_service: Optional[NiftyStocksService] = None


def get_nifty_stocks_service() -> NiftyStocksService:
    """Get the singleton NiftyStocksService instance"""
    global _nifty_stocks_service
    if _nifty_stocks_service is None:
        _nifty_stocks_service = NiftyStocksService()
    return _nifty_stocks_service
