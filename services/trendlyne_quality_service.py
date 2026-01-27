"""
Quality filtering service for Trendlyne stocks
Categorizes stocks into Great, Medium, and Good quality based on user criteria
"""
from typing import List, Optional, Dict, Any
from services.trendlyne_stocks_service import TrendlyneStock, get_trendlyne_stocks_service
from pydantic import Field
from enum import Enum


class QualityTier(str, Enum):
    """Quality tier classification"""
    GREAT = "great"
    MEDIUM = "medium"
    GOOD = "good"
    NONE = "none"


class QualityFilteredStock(TrendlyneStock):
    """Stock with quality tier and score"""
    quality_tier: QualityTier = Field(default=QualityTier.NONE)
    quality_score: float = Field(default=0.0)
    quality_notes: List[str] = Field(default_factory=list)
    passed_criteria: Dict[str, bool] = Field(default_factory=dict)


class TrendlyneQualityService:
    """Service to filter and categorize Trendlyne stocks by quality"""
    
    def __init__(self):
        self.trendlyne_service = get_trendlyne_stocks_service()
    
    def _safe_float(self, value: Any, default: float = 0.0) -> float:
        """Safely convert value to float"""
        if value is None or value == '' or value == '-':
            return default
        try:
            if isinstance(value, str):
                value = value.replace(',', '').strip()
            return float(value)
        except (ValueError, TypeError):
            return default
    
    def _get_value(self, stock: TrendlyneStock, key: str, default: float = 0.0) -> float:
        """Get float value from stock data"""
        value = stock.data.get(key, default)
        return self._safe_float(value, default)
    
    def _check_promoter_holding_stable(self, stock: TrendlyneStock) -> bool:
        """Check if promoter holding is stable or rising"""
        holding_change = self._get_value(stock, "Promoter holding change QoQ %", 0)
        # Stable: change between -1% and 1%, Rising: positive change
        return -1 <= holding_change <= 10  # Allow small decrease or any increase
    
    def _check_positive_quarters(self, stock: TrendlyneStock) -> tuple:
        """Check for positive quarterly EPS growth"""
        eps_qoq = self._get_value(stock, "Basic EPS QoQ Growth %", 0)
        eps_qtr_yoy = self._get_value(stock, "EPS Qtr YoY Growth %", 0)
        
        # Count positive quarters (simplified - check if recent growth is positive)
        positive_count = 0
        if eps_qoq > 0:
            positive_count += 1
        if eps_qtr_yoy > 0:
            positive_count += 1
        
        return positive_count >= 1, positive_count >= 2
    
    def _check_profit_growth_consistent(self, stock: TrendlyneStock) -> bool:
        """Check if profit growth is consistent"""
        profit_3y = self._get_value(stock, "Net Profit 3Y Growth %", 0)
        profit_5y = self._get_value(stock, "Net Profit 5Y Growth %", 0)
        profit_qoq = self._get_value(stock, "Net Profit QoQ Growth %", 0)
        
        # Consistent if all are positive or at least 2 out of 3 are positive
        positive_count = sum([
            profit_3y > 0,
            profit_5y > 0,
            profit_qoq > 0
        ])
        return positive_count >= 2
    
    def _check_margin_stable(self, stock: TrendlyneStock) -> bool:
        """Check if operating margin is stable or expanding"""
        opm_ann = self._get_value(stock, "OPM Ann  %", 0)
        opm_ttm = self._get_value(stock, "OPM TTM %", 0)
        
        # Stable if both are positive and similar (within 5%)
        if opm_ann > 0 and opm_ttm > 0:
            diff = abs(opm_ann - opm_ttm)
            return diff <= 5 or opm_ttm >= opm_ann  # Stable or expanding
        return opm_ann > 0 or opm_ttm > 0
    
    def _check_eps_trend_rising(self, stock: TrendlyneStock) -> bool:
        """Check if EPS trend (TTM) is rising"""
        eps_ttm_growth = self._get_value(stock, "EPS TTM Growth %", 0)
        return eps_ttm_growth > 0
    
    def _check_sales_growth(self, stock: TrendlyneStock) -> bool:
        """Check if sales growth is > 10-15%"""
        # Use operating revenue growth if available, otherwise use profit growth as proxy
        # Since we don't have direct sales growth, we'll use profit growth as indicator
        profit_3y = self._get_value(stock, "Net Profit 3Y Growth %", 0)
        profit_qoq = self._get_value(stock, "Net Profit QoQ Growth %", 0)
        
        # If profit growth is good, assume sales growth is also good
        return profit_3y > 10 or profit_qoq > 10
    
    def _check_valuation(self, stock: TrendlyneStock) -> tuple:
        """Check valuation parameters - returns (pe_ok, peg_ok, pb_ok, ev_ok)"""
        # PE vs Industry PE - prefer lower or similar
        # Note: We don't have direct PE, but we can check PEG
        peg = self._get_value(stock, "PEG TTM", None)
        peg_ok = True  # Default to OK if not available
        if peg is not None and peg > 0:
            peg_ok = 0.7 <= peg <= 1.5
        
        # Price to Book
        pbv = self._get_value(stock, "PBV Adjusted", None)
        pb_ok = True  # Depends on sector, so we'll be lenient
        if pbv is not None and pbv > 0:
            pb_ok = pbv < 5  # Reasonable upper limit
        
        # EV/EBITDA
        ev_ebitda = self._get_value(stock, "EV Per EBITDA Ann ", None)
        ev_ok = True  # Cross-check for capital-heavy stocks
        if ev_ebitda is not None and ev_ebitda > 0:
            ev_ok = ev_ebitda < 20  # Reasonable upper limit
        
        # PE check - we don't have direct PE, so skip
        pe_ok = True
        
        return pe_ok, peg_ok, pb_ok, ev_ok
    
    def filter_great_quality_stocks(self) -> List[QualityFilteredStock]:
        """
        Filter stocks that meet GREAT quality criteria
        All core quality parameters must be met
        """
        all_stocks = self.trendlyne_service.get_all_stocks()
        great_stocks = []
        
        for stock in all_stocks:
            # Extract values (note: keys are cleaned, no trailing spaces)
            roe = self._get_value(stock, "ROE Ann  %", 0)
            roce = self._get_value(stock, "ROCE Ann  %", 0)
            debt_equity = self._get_value(stock, "Total Debt to Total Equity Ann", 999)
            interest_coverage = self._get_value(stock, "Interest Coverage Ratio Ann", 0)
            current_ratio = self._get_value(stock, "Current Ratio Ann", 0)
            if current_ratio == 0:
                current_ratio = self._get_value(stock, "Current Ratio TTM", 0)
            
            # Check core quality parameters
            roe_ok = roe > 12
            roce_ok = roce > 15
            debt_ok = debt_equity < 1
            interest_ok = interest_coverage > 3
            current_ok = current_ratio > 1.2
            promoter_ok = self._check_promoter_holding_stable(stock)
            
            # Check growth parameters
            positive_quarters, two_quarters = self._check_positive_quarters(stock)
            sales_growth_ok = self._check_sales_growth(stock)
            profit_consistent = self._check_profit_growth_consistent(stock)
            margin_stable = self._check_margin_stable(stock)
            eps_rising = self._check_eps_trend_rising(stock)
            
            # Check valuation
            pe_ok, peg_ok, pb_ok, ev_ok = self._check_valuation(stock)
            
            # Get Durability and Valuation scores
            durability_score = self._safe_float(stock.data.get("Durability Score"), None)
            valuation_score = self._safe_float(stock.data.get("Valuation Score"), None)
            
            # All core parameters must pass for GREAT quality
            if (roe_ok and roce_ok and debt_ok and interest_ok and 
                current_ok and promoter_ok and positive_quarters and 
                sales_growth_ok and profit_consistent and margin_stable and 
                eps_rising):
                
                # Create quality filtered stock
                stock_dict = stock.model_dump() if hasattr(stock, 'model_dump') else stock.dict()
                quality_stock = QualityFilteredStock(
                    **stock_dict,
                    quality_tier=QualityTier.GREAT,
                    quality_score=self._calculate_quality_score(stock, roe, roce, debt_equity, 
                                                               interest_coverage, current_ratio,
                                                               durability_score, valuation_score),
                    passed_criteria={
                        "roe": roe_ok,
                        "roce": roce_ok,
                        "debt_equity": debt_ok,
                        "interest_coverage": interest_ok,
                        "current_ratio": current_ok,
                        "promoter_holding": promoter_ok,
                        "positive_quarters": positive_quarters,
                        "sales_growth": sales_growth_ok,
                        "profit_consistent": profit_consistent,
                        "margin_stable": margin_stable,
                        "eps_rising": eps_rising,
                        "valuation": pe_ok and peg_ok and pb_ok and ev_ok
                    }
                )
                great_stocks.append(quality_stock)
        
        # Sort by quality score descending
        great_stocks.sort(key=lambda x: x.quality_score, reverse=True)
        return great_stocks
    
    def filter_medium_quality_stocks(self) -> List[QualityFilteredStock]:
        """
        Filter stocks that meet MEDIUM quality criteria
        Most core parameters must be met, with some flexibility
        """
        all_stocks = self.trendlyne_service.get_all_stocks()
        great_stocks = self.filter_great_quality_stocks()
        great_stock_keys = {self._get_stock_key(s) for s in great_stocks}
        
        medium_stocks = []
        
        for stock in all_stocks:
            stock_key = self._get_stock_key(stock)
            if stock_key in great_stock_keys:
                continue  # Skip stocks already in great tier
            
            # Extract values (note: keys are cleaned, no trailing spaces)
            roe = self._get_value(stock, "ROE Ann  %", 0)
            roce = self._get_value(stock, "ROCE Ann  %", 0)
            debt_equity = self._get_value(stock, "Total Debt to Total Equity Ann", 999)
            interest_coverage = self._get_value(stock, "Interest Coverage Ratio Ann", 0)
            current_ratio = self._get_value(stock, "Current Ratio Ann", 0)
            if current_ratio == 0:
                current_ratio = self._get_value(stock, "Current Ratio TTM", 0)
            
            # Medium quality: Stricter criteria - should be between Great and Good
            # Require strong fundamentals but not as strict as Great
            roe_ok = roe > 11.5  # Close to Great threshold (12)
            roce_ok = roce > 14  # Close to Great threshold (15)
            debt_ok = debt_equity < 1.1  # Close to Great threshold (1.0)
            interest_ok = interest_coverage > 2.8  # Close to Great threshold (3)
            current_ok = current_ratio > 1.15  # Close to Great threshold (1.2)
            promoter_ok = self._check_promoter_holding_stable(stock)
            
            # Count passed core criteria
            core_passed = sum([roe_ok, roce_ok, debt_ok, interest_ok, current_ok, promoter_ok])
            
            # Check growth parameters - require multiple positive growth indicators
            positive_quarters, two_quarters = self._check_positive_quarters(stock)
            sales_growth_ok = self._check_sales_growth(stock) or roe > 10
            profit_consistent = self._check_profit_growth_consistent(stock)
            margin_stable = self._check_margin_stable(stock)
            eps_rising = self._check_eps_trend_rising(stock)
            
            # Check valuation
            pe_ok, peg_ok, pb_ok, ev_ok = self._check_valuation(stock)
            
            # Get Durability and Valuation scores
            durability_score = self._safe_float(stock.data.get("Durability Score"), None)
            valuation_score = self._safe_float(stock.data.get("Valuation Score"), None)
            
            # Medium quality: Very strict - require 5+ core criteria AND multiple growth indicators
            # OR exceptional fundamentals (4 criteria with very high ROE/ROCE + strong growth)
            has_strong_core = core_passed >= 5
            has_exceptional_fundamentals = (core_passed >= 4 and 
                                         (roe > 14 or roce > 17) and 
                                         two_quarters and  # Require 2+ positive quarters
                                         profit_consistent and
                                         margin_stable)
            
            # Medium should be significantly stricter - require both strong fundamentals AND growth
            if (has_strong_core and (two_quarters or (positive_quarters and profit_consistent and margin_stable))) or has_exceptional_fundamentals:
                stock_dict = stock.model_dump() if hasattr(stock, 'model_dump') else stock.dict()
                quality_stock = QualityFilteredStock(
                    **stock_dict,
                    quality_tier=QualityTier.MEDIUM,
                    quality_score=self._calculate_quality_score(stock, roe, roce, debt_equity,
                                                               interest_coverage, current_ratio,
                                                               durability_score, valuation_score),
                    passed_criteria={
                        "roe": roe_ok,
                        "roce": roce_ok,
                        "debt_equity": debt_ok,
                        "interest_coverage": interest_ok,
                        "current_ratio": current_ok,
                        "promoter_holding": promoter_ok,
                        "positive_quarters": positive_quarters,
                        "sales_growth": sales_growth_ok,
                        "profit_consistent": profit_consistent,
                        "margin_stable": margin_stable,
                        "eps_rising": eps_rising,
                        "valuation": pe_ok and peg_ok and pb_ok and ev_ok
                    }
                )
                medium_stocks.append(quality_stock)
        
        # Sort by quality score descending
        medium_stocks.sort(key=lambda x: x.quality_score, reverse=True)
        return medium_stocks
    
    def filter_good_quality_stocks(self) -> List[QualityFilteredStock]:
        """
        Filter stocks that meet GOOD quality criteria
        Balanced criteria with more flexibility
        """
        all_stocks = self.trendlyne_service.get_all_stocks()
        great_stocks = self.filter_great_quality_stocks()
        medium_stocks = self.filter_medium_quality_stocks()
        
        great_stock_keys = {self._get_stock_key(s) for s in great_stocks}
        medium_stock_keys = {self._get_stock_key(s) for s in medium_stocks}
        
        good_stocks = []
        
        for stock in all_stocks:
            stock_key = self._get_stock_key(stock)
            if stock_key in great_stock_keys or stock_key in medium_stock_keys:
                continue  # Skip stocks already in higher tiers
            
            # Extract values (note: keys are cleaned, no trailing spaces)
            roe = self._get_value(stock, "ROE Ann  %", 0)
            roce = self._get_value(stock, "ROCE Ann  %", 0)
            debt_equity = self._get_value(stock, "Total Debt to Total Equity Ann", 999)
            interest_coverage = self._get_value(stock, "Interest Coverage Ratio Ann", 0)
            current_ratio = self._get_value(stock, "Current Ratio Ann", 0)
            if current_ratio == 0:
                current_ratio = self._get_value(stock, "Current Ratio TTM", 0)
            
            # Good quality: Most lenient thresholds - catch all stocks with any decent fundamentals
            # This should be the largest tier as it's the most inclusive
            # Use very lenient thresholds to catch stocks that don't meet Medium but still have merit
            roe_ok = roe > 3  # Very lenient
            roce_ok = roce > 4  # Very lenient  
            debt_ok = debt_equity < 4.0  # Very lenient
            interest_ok = interest_coverage > 0.1  # Very lenient (just not severely negative)
            current_ok = current_ratio > 0.5  # Very lenient
            promoter_ok = self._check_promoter_holding_stable(stock) or roe > 1 or roce > 3  # Very lenient
            
            # Count passed core criteria
            core_passed = sum([roe_ok, roce_ok, debt_ok, interest_ok, current_ok, promoter_ok])
            
            # Check growth parameters (very lenient - mostly optional)
            positive_quarters, _ = self._check_positive_quarters(stock)
            sales_growth_ok = self._check_sales_growth(stock) or roe > 1 or roce > 3
            profit_consistent = self._check_profit_growth_consistent(stock)
            margin_stable = self._check_margin_stable(stock)
            eps_rising = self._check_eps_trend_rising(stock)
            
            # Check valuation
            pe_ok, peg_ok, pb_ok, ev_ok = self._check_valuation(stock)
            
            # Get Durability and Valuation scores
            durability_score = self._safe_float(stock.data.get("Durability Score"), None)
            valuation_score = self._safe_float(stock.data.get("Valuation Score"), None)
            
            # Good quality: Very inclusive - catch stocks with any reasonable quality indicators
            # At least 1 core criteria OR any positive returns OR any growth indicators
            # This makes Good truly the most inclusive tier
            has_any_quality = core_passed >= 1
            has_any_returns = roe > 0 or roce > 0
            has_any_growth = positive_quarters or sales_growth_ok or profit_consistent
            has_durability_score = durability_score is not None and durability_score > 0
            has_valuation_score = valuation_score is not None and valuation_score > 0
            
            # Good quality should catch most stocks that don't meet Medium but have some merit
            # This is the catch-all tier for decent stocks
            if (has_any_quality or has_any_returns or has_any_growth or 
                has_durability_score or has_valuation_score):
                stock_dict = stock.model_dump() if hasattr(stock, 'model_dump') else stock.dict()
                quality_stock = QualityFilteredStock(
                    **stock_dict,
                    quality_tier=QualityTier.GOOD,
                    quality_score=self._calculate_quality_score(stock, roe, roce, debt_equity,
                                                               interest_coverage, current_ratio,
                                                               durability_score, valuation_score),
                    passed_criteria={
                        "roe": roe_ok,
                        "roce": roce_ok,
                        "debt_equity": debt_ok,
                        "interest_coverage": interest_ok,
                        "current_ratio": current_ok,
                        "promoter_holding": promoter_ok,
                        "positive_quarters": positive_quarters,
                        "sales_growth": sales_growth_ok,
                        "profit_consistent": profit_consistent,
                        "margin_stable": margin_stable,
                        "eps_rising": eps_rising,
                        "valuation": pe_ok and peg_ok and pb_ok and ev_ok
                    }
                )
                good_stocks.append(quality_stock)
        
        # Sort by quality score descending
        good_stocks.sort(key=lambda x: x.quality_score, reverse=True)
        return good_stocks
    
    def _get_stock_key(self, stock: TrendlyneStock) -> str:
        """Get unique key for stock"""
        if stock.isin:
            return f"ISIN:{stock.isin.upper()}"
        elif stock.nse_code:
            return f"NSE:{stock.nse_code.upper()}"
        elif stock.bse_code:
            return f"BSE:{stock.bse_code.upper()}"
        return f"STOCK:{stock.stock.upper()}"
    
    def _calculate_quality_score(self, stock: TrendlyneStock, roe: float, roce: float,
                                 debt_equity: float, interest_coverage: float,
                                 current_ratio: float, durability_score: Optional[float],
                                 valuation_score: Optional[float]) -> float:
        """Calculate overall quality score (0-100)"""
        score = 0.0
        
        # Core quality parameters (60 points)
        if roe > 20:
            score += 15
        elif roe > 15:
            score += 12
        elif roe > 12:
            score += 10
        elif roe > 8:
            score += 5
        
        if roce > 25:
            score += 15
        elif roce > 20:
            score += 12
        elif roce > 15:
            score += 10
        elif roce > 10:
            score += 5
        
        if debt_equity == 0:
            score += 10
        elif debt_equity < 0.3:
            score += 8
        elif debt_equity < 0.5:
            score += 6
        elif debt_equity < 1.0:
            score += 4
        
        if interest_coverage > 10:
            score += 8
        elif interest_coverage > 5:
            score += 6
        elif interest_coverage > 3:
            score += 4
        
        if current_ratio > 2.0:
            score += 7
        elif current_ratio > 1.5:
            score += 5
        elif current_ratio > 1.2:
            score += 3
        
        # Durability and Valuation scores (20 points)
        if durability_score is not None:
            score += (durability_score / 100) * 10  # Max 10 points
        if valuation_score is not None:
            score += (valuation_score / 100) * 10  # Max 10 points
        
        # Growth indicators (20 points)
        eps_ttm_growth = self._get_value(stock, "EPS TTM Growth %", 0)
        if eps_ttm_growth > 20:
            score += 10
        elif eps_ttm_growth > 10:
            score += 7
        elif eps_ttm_growth > 0:
            score += 4
        
        profit_3y = self._get_value(stock, "Net Profit 3Y Growth %", 0)
        if profit_3y > 20:
            score += 10
        elif profit_3y > 10:
            score += 7
        elif profit_3y > 0:
            score += 4
        
        return min(score, 100.0)  # Cap at 100
    
    def get_all_quality_stocks(self, tier: Optional[QualityTier] = None) -> List[QualityFilteredStock]:
        """Get all quality stocks, optionally filtered by tier"""
        if tier == QualityTier.GREAT:
            return self.filter_great_quality_stocks()
        elif tier == QualityTier.MEDIUM:
            return self.filter_medium_quality_stocks()
        elif tier == QualityTier.GOOD:
            return self.filter_good_quality_stocks()
        else:
            # Return all tiers combined
            great = self.filter_great_quality_stocks()
            medium = self.filter_medium_quality_stocks()
            good = self.filter_good_quality_stocks()
            return great + medium + good


# Singleton instance
_trendlyne_quality_service: Optional[TrendlyneQualityService] = None


def get_trendlyne_quality_service() -> TrendlyneQualityService:
    """Get the singleton TrendlyneQualityService instance"""
    global _trendlyne_quality_service
    if _trendlyne_quality_service is None:
        _trendlyne_quality_service = TrendlyneQualityService()
    return _trendlyne_quality_service

