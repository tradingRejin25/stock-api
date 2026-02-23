"""
Nifty stocks API: GET /api/nifty-stocks (all, or filter by nseCode, isin, search).
Returns { count, stocks: [{ stockName, nseCode, isin }] }.
Data from data/nifty_stocks.csv if present; otherwise empty list (200 OK).
"""
import csv
from pathlib import Path
from fastapi import APIRouter, Query
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter(prefix="/api/nifty-stocks", tags=["Nifty Stocks"])

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
NIFTY_CSV = _DATA_DIR / "nifty_stocks.csv"


class NiftyStockItem(BaseModel):
    stockName: str
    nseCode: str
    isin: str


class NiftyStocksResponse(BaseModel):
    count: int
    stocks: List[NiftyStockItem]


def _load_nifty_stocks() -> List[dict]:
    if not NIFTY_CSV.exists():
        return []
    out = []
    with open(NIFTY_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        # Find column names (case-insensitive)
        name_col = next((c for c in fieldnames if "name" in c.lower() or "stock" in c.lower()), None)
        nse_col = next((c for c in fieldnames if "nse" in c.lower() or "code" in c.lower() or "symbol" in c.lower()), None)
        isin_col = next((c for c in fieldnames if "isin" in c.lower()), None)
        if not name_col and not nse_col:
            return []
        for row in reader:
            def v(col):
                if not col:
                    return ""
                return (row.get(col) or "").strip()
            stock_name = v(name_col) if name_col else ""
            nse_code = v(nse_col) if nse_col else ""
            isin = v(isin_col) if isin_col else ""
            if stock_name or nse_code:
                out.append({"stockName": stock_name, "nseCode": nse_code, "isin": isin})
    return out


@router.get("", response_model=NiftyStocksResponse)
async def get_nifty_stocks(
    nseCode: Optional[str] = Query(None, alias="nseCode"),
    isin: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
):
    """
    GET /api/nifty-stocks - all stocks (or filter by nseCode, isin, search).
    Returns 200 with { count, stocks }. Data from data/nifty_stocks.csv if present.
    """
    stocks = _load_nifty_stocks()
    if nseCode:
        nse = nseCode.strip().upper()
        stocks = [s for s in stocks if (s.get("nseCode") or "").strip().upper() == nse]
    elif isin:
        isin_ = isin.strip()
        stocks = [s for s in stocks if (s.get("isin") or "").strip() == isin_]
    elif search:
        q = search.strip().lower()
        stocks = [s for s in stocks if q in (s.get("stockName") or "").lower() or q in (s.get("nseCode") or "").lower()]
    return NiftyStocksResponse(count=len(stocks), stocks=[NiftyStockItem(**s) for s in stocks])
