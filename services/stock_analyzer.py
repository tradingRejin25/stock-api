"""
Stock analyzer service
Provides methods to filter, analyze, and find great stocks
"""

from typing import List, Optional, Dict
import logging

from models.stock import Stock, StockFilters, GreatStockCriteria

logger = logging.getLogger(__name__)

class StockAnalyzer:
    """Analyzes stocks and finds great investment opportunities"""
    
    def filter_stocks(self, stocks: List[Stock], filters: StockFilters) -> List[Stock]:
        """
        Filter stocks based on criteria
        
        Args:
            stocks: List of stocks to filter
            filters: Filter criteria
        
        Returns:
            Filtered list of stocks
        """
        filtered = stocks
        
        if filters.symbol:
            filtered = [s for s in filtered if s.symbol and filters.symbol.upper() in s.symbol.upper()]
        
        if filters.sector:
            filtered = [s for s in filtered if s.sector and filters.sector.lower() in s.sector.lower()]
        
        if filters.market_cap_min is not None:
            filtered = [s for s in filtered if s.market_cap and s.market_cap >= filters.market_cap_min]
        
        if filters.market_cap_max is not None:
            filtered = [s for s in filtered if s.market_cap and s.market_cap <= filters.market_cap_max]
        
        if filters.pe_min is not None:
            filtered = [s for s in filtered if s.pe_ratio and s.pe_ratio >= filters.pe_min]
        
        if filters.pe_max is not None:
            filtered = [s for s in filtered if s.pe_ratio and s.pe_ratio <= filters.pe_max]
        
        if filters.pb_min is not None:
            filtered = [s for s in filtered if s.pb_ratio and s.pb_ratio >= filters.pb_min]
        
        if filters.pb_max is not None:
            filtered = [s for s in filtered if s.pb_ratio and s.pb_ratio <= filters.pb_max]
        
        if filters.roe_min is not None:
            filtered = [s for s in filtered if s.roe and s.roe >= filters.roe_min]
        
        if filters.roe_max is not None:
            filtered = [s for s in filtered if s.roe and s.roe <= filters.roe_max]
        
        if filters.dividend_yield_min is not None:
            filtered = [s for s in filtered if s.dividend_yield and s.dividend_yield >= filters.dividend_yield_min]
        
        if filters.dividend_yield_max is not None:
            filtered = [s for s in filtered if s.dividend_yield and s.dividend_yield <= filters.dividend_yield_max]
        
        return filtered
    
    def find_stock_by_symbol(self, stocks: List[Stock], symbol: str) -> Optional[Stock]:
        """
        Find stock by symbol (case-insensitive)
        
        Args:
            stocks: List of stocks to search
            symbol: Stock symbol to find
        
        Returns:
            Stock object if found, None otherwise
        """
        symbol_upper = symbol.upper()
        for stock in stocks:
            if stock.symbol and stock.symbol.upper() == symbol_upper:
                return stock
        return None
    
    def find_stock_by_isin(self, stocks: List[Stock], isin: str) -> Optional[Stock]:
        """
        Find stock by ISIN code (case-insensitive)
        
        Args:
            stocks: List of stocks to search
            isin: ISIN code to find
        
        Returns:
            Stock object if found, None otherwise
        """
        isin_upper = isin.upper().strip()
        for stock in stocks:
            if stock.isin and stock.isin.upper().strip() == isin_upper:
                return stock
        return None
    
    def calculate_stock_score(self, stock: Stock, criteria: GreatStockCriteria) -> float:
        """
        Calculate a weighted score for a stock based on criteria
        Now includes Trendlyne scores and comprehensive metrics
        
        Args:
            stock: Stock to score
            criteria: Criteria for scoring
        
        Returns:
            Score from 0-100
        """
        valuation_score = 0.0
        valuation_max = 0.0
        profitability_score = 0.0
        profitability_max = 0.0
        growth_score = 0.0
        growth_max = 0.0
        trendlyne_score = 0.0
        trendlyne_max = 0.0
        
        # ========== VALUATION SCORING ==========
        # PE Ratio (lower is better)
        if stock.pe_ratio and criteria.max_pe_ratio:
            if stock.pe_ratio <= criteria.max_pe_ratio:
                valuation_score += (1 - (stock.pe_ratio / criteria.max_pe_ratio))
            valuation_max += 1
        
        # PE TTM (lower is better)
        if stock.pe_ttm and criteria.max_pe_ttm:
            if stock.pe_ttm <= criteria.max_pe_ttm:
                valuation_score += (1 - (stock.pe_ttm / criteria.max_pe_ttm))
            valuation_max += 1
        
        # PEG TTM (lower is better, < 1 is ideal)
        if stock.peg_ttm and criteria.max_peg_ttm:
            if stock.peg_ttm <= criteria.max_peg_ttm:
                valuation_score += (1 - min(1.0, stock.peg_ttm / criteria.max_peg_ttm))
            valuation_max += 1
        
        # PB Ratio (lower is better)
        if stock.pb_ratio and criteria.max_pb_ratio:
            if stock.pb_ratio <= criteria.max_pb_ratio:
                valuation_score += (1 - (stock.pb_ratio / criteria.max_pb_ratio))
            valuation_max += 1
        
        # Price to Sales (lower is better)
        if stock.price_to_sales and criteria.max_price_to_sales:
            if stock.price_to_sales <= criteria.max_price_to_sales:
                valuation_score += (1 - (stock.price_to_sales / criteria.max_price_to_sales))
            valuation_max += 1
        
        # %Days below PE (higher is better - means trading at lower valuation)
        if stock.pct_days_below_current_pe and criteria.max_pct_days_below_pe:
            if stock.pct_days_below_current_pe <= criteria.max_pct_days_below_pe:
                valuation_score += (stock.pct_days_below_current_pe / criteria.max_pct_days_below_pe)
            valuation_max += 1
        
        # ========== PROFITABILITY SCORING ==========
        # ROE (higher is better)
        if stock.roe and criteria.min_roe:
            if stock.roe >= criteria.min_roe:
                profitability_score += min(1.0, stock.roe / (criteria.min_roe * 2))
            profitability_max += 1
        
        # ROA (higher is better)
        if stock.roa and criteria.min_roa:
            if stock.roa >= criteria.min_roa:
                profitability_score += min(1.0, stock.roa / (criteria.min_roa * 2))
            profitability_max += 1
        
        # Profit Margin (higher is better)
        if stock.profit_margin and criteria.min_profit_margin:
            if stock.profit_margin >= criteria.min_profit_margin:
                profitability_score += min(1.0, stock.profit_margin / (criteria.min_profit_margin * 2))
            profitability_max += 1
        
        # Operating Margin (higher is better)
        if stock.operating_margin and criteria.min_operating_margin:
            if stock.operating_margin >= criteria.min_operating_margin:
                profitability_score += min(1.0, stock.operating_margin / (criteria.min_operating_margin * 2))
            profitability_max += 1
        
        # Operating Profit Margin Qtr (higher is better)
        if stock.operating_profit_margin_qtr and criteria.min_operating_profit_margin_qtr:
            if stock.operating_profit_margin_qtr >= criteria.min_operating_profit_margin_qtr:
                profitability_score += min(1.0, stock.operating_profit_margin_qtr / (criteria.min_operating_profit_margin_qtr * 2))
            profitability_max += 1
        
        # Piotroski Score (higher is better, 0-9)
        if stock.piotroski_score is not None and criteria.min_piotroski_score:
            if stock.piotroski_score >= criteria.min_piotroski_score:
                profitability_score += min(1.0, stock.piotroski_score / 9.0)
            profitability_max += 1
        
        # ========== GROWTH SCORING ==========
        # Revenue Growth Annual YoY (higher is better)
        if stock.revenue_growth and criteria.min_revenue_growth:
            if stock.revenue_growth >= criteria.min_revenue_growth:
                growth_score += min(1.0, stock.revenue_growth / (criteria.min_revenue_growth * 2))
            growth_max += 1
        
        # Profit Growth Annual YoY (higher is better)
        if stock.profit_growth and criteria.min_profit_growth:
            if stock.profit_growth >= criteria.min_profit_growth:
                growth_score += min(1.0, stock.profit_growth / (criteria.min_profit_growth * 2))
            growth_max += 1
        
        # Revenue Growth Qtr YoY (higher is better)
        if stock.revenue_growth_qtr_yoy and criteria.min_revenue_growth_qtr_yoy:
            if stock.revenue_growth_qtr_yoy >= criteria.min_revenue_growth_qtr_yoy:
                growth_score += min(1.0, stock.revenue_growth_qtr_yoy / (criteria.min_revenue_growth_qtr_yoy * 2))
            growth_max += 1
        
        # Net Profit Qtr Growth YoY (higher is better)
        if stock.net_profit_qtr_growth_yoy and criteria.min_net_profit_qtr_growth_yoy:
            if stock.net_profit_qtr_growth_yoy >= criteria.min_net_profit_qtr_growth_yoy:
                growth_score += min(1.0, stock.net_profit_qtr_growth_yoy / (criteria.min_net_profit_qtr_growth_yoy * 2))
            growth_max += 1
        
        # Revenue QoQ Growth (higher is better)
        if stock.revenue_qoq_growth and criteria.min_revenue_qoq_growth:
            if stock.revenue_qoq_growth >= criteria.min_revenue_qoq_growth:
                growth_score += min(1.0, stock.revenue_qoq_growth / (criteria.min_revenue_qoq_growth * 2))
            growth_max += 1
        
        # EPS TTM Growth (higher is better)
        if stock.eps_ttm_growth and criteria.min_eps_ttm_growth:
            if stock.eps_ttm_growth >= criteria.min_eps_ttm_growth:
                growth_score += min(1.0, stock.eps_ttm_growth / (criteria.min_eps_ttm_growth * 2))
            growth_max += 1
        
        # ========== TRENDLYNE SCORES ==========
        if criteria.use_trendlyne_scores:
            # Durability Score (higher is better, typically 0-100)
            if stock.trendlyne_durability_score is not None:
                if criteria.min_trendlyne_durability_score:
                    if stock.trendlyne_durability_score >= criteria.min_trendlyne_durability_score:
                        trendlyne_score += (stock.trendlyne_durability_score / 100.0)
                else:
                    trendlyne_score += (stock.trendlyne_durability_score / 100.0)
                trendlyne_max += 1
            
            # Valuation Score (higher is better, typically 0-100)
            if stock.trendlyne_valuation_score is not None:
                if criteria.min_trendlyne_valuation_score:
                    if stock.trendlyne_valuation_score >= criteria.min_trendlyne_valuation_score:
                        trendlyne_score += (stock.trendlyne_valuation_score / 100.0)
                else:
                    trendlyne_score += (stock.trendlyne_valuation_score / 100.0)
                trendlyne_max += 1
            
            # Momentum Score (higher is better, typically 0-100)
            if stock.trendlyne_momentum_score is not None:
                if criteria.min_trendlyne_momentum_score:
                    if stock.trendlyne_momentum_score >= criteria.min_trendlyne_momentum_score:
                        trendlyne_score += (stock.trendlyne_momentum_score / 100.0)
                else:
                    trendlyne_score += (stock.trendlyne_momentum_score / 100.0)
                trendlyne_max += 1
        
        # ========== COMBINE SCORES WITH WEIGHTS ==========
        final_score = 0.0
        total_weight = 0.0
        
        # Valuation component
        if valuation_max > 0:
            valuation_normalized = (valuation_score / valuation_max) * 100
            final_score += valuation_normalized * criteria.valuation_weight
            total_weight += criteria.valuation_weight
        
        # Profitability component
        if profitability_max > 0:
            profitability_normalized = (profitability_score / profitability_max) * 100
            final_score += profitability_normalized * criteria.profitability_weight
            total_weight += criteria.profitability_weight
        
        # Growth component
        if growth_max > 0:
            growth_normalized = (growth_score / growth_max) * 100
            final_score += growth_normalized * criteria.growth_weight
            total_weight += criteria.growth_weight
        
        # Trendlyne component
        if criteria.use_trendlyne_scores and trendlyne_max > 0:
            trendlyne_normalized = (trendlyne_score / trendlyne_max) * 100
            final_score += trendlyne_normalized * criteria.trendlyne_weight
            total_weight += criteria.trendlyne_weight
        
        # Normalize to 0-100 scale
        if total_weight > 0:
            normalized_score = final_score / total_weight
        else:
            normalized_score = 0.0
        
        return round(normalized_score, 2)
    
    def find_great_stocks(self, stocks: List[Stock], criteria: GreatStockCriteria) -> List[Stock]:
        """
        Find great stocks based on criteria
        
        Args:
            stocks: List of stocks to analyze
            criteria: Criteria for great stocks
        
        Returns:
            List of great stocks sorted by score
        """
        great_stocks = []
        
        for stock in stocks:
            # Apply basic filters
            if criteria.min_market_cap and (not stock.market_cap or stock.market_cap < criteria.min_market_cap):
                continue
            
            if criteria.max_market_cap and (not stock.market_cap or stock.market_cap > criteria.max_market_cap):
                continue
            
            if criteria.max_pe_ratio and stock.pe_ratio and stock.pe_ratio > criteria.max_pe_ratio:
                continue
            
            if criteria.max_pb_ratio and stock.pb_ratio and stock.pb_ratio > criteria.max_pb_ratio:
                continue
            
            if criteria.max_price_to_sales and stock.price_to_sales and stock.price_to_sales > criteria.max_price_to_sales:
                continue
            
            if criteria.min_roe and (not stock.roe or stock.roe < criteria.min_roe):
                continue
            
            if criteria.min_roa and (not stock.roa or stock.roa < criteria.min_roa):
                continue
            
            if criteria.min_profit_margin and (not stock.profit_margin or stock.profit_margin < criteria.min_profit_margin):
                continue
            
            if criteria.min_operating_margin and (not stock.operating_margin or stock.operating_margin < criteria.min_operating_margin):
                continue
            
            if criteria.min_revenue_growth and (not stock.revenue_growth or stock.revenue_growth < criteria.min_revenue_growth):
                continue
            
            if criteria.min_profit_growth and (not stock.profit_growth or stock.profit_growth < criteria.min_profit_growth):
                continue
            
            if criteria.max_debt_to_equity and stock.debt_to_equity and stock.debt_to_equity > criteria.max_debt_to_equity:
                continue
            
            if criteria.min_current_ratio and (not stock.current_ratio or stock.current_ratio < criteria.min_current_ratio):
                continue
            
            if criteria.min_quick_ratio and (not stock.quick_ratio or stock.quick_ratio < criteria.min_quick_ratio):
                continue
            
            if criteria.min_dividend_yield and (not stock.dividend_yield or stock.dividend_yield < criteria.min_dividend_yield):
                continue
            
            if criteria.max_price_to_52w_high and stock.current_price and stock.week_52_high:
                price_ratio = stock.current_price / stock.week_52_high
                if price_ratio > criteria.max_price_to_52w_high:
                    continue
            
            # Additional filters for new fields
            if criteria.max_pe_ttm and stock.pe_ttm and stock.pe_ttm > criteria.max_pe_ttm:
                continue
            
            if criteria.max_peg_ttm and stock.peg_ttm and stock.peg_ttm > criteria.max_peg_ttm:
                continue
            
            if criteria.min_operating_profit_margin_qtr and (not stock.operating_profit_margin_qtr or stock.operating_profit_margin_qtr < criteria.min_operating_profit_margin_qtr):
                continue
            
            if criteria.min_revenue_growth_qtr_yoy and (not stock.revenue_growth_qtr_yoy or stock.revenue_growth_qtr_yoy < criteria.min_revenue_growth_qtr_yoy):
                continue
            
            if criteria.min_net_profit_qtr_growth_yoy and (not stock.net_profit_qtr_growth_yoy or stock.net_profit_qtr_growth_yoy < criteria.min_net_profit_qtr_growth_yoy):
                continue
            
            if criteria.min_revenue_qoq_growth and (not stock.revenue_qoq_growth or stock.revenue_qoq_growth < criteria.min_revenue_qoq_growth):
                continue
            
            if criteria.min_net_profit_qoq_growth and (not stock.net_profit_qoq_growth or stock.net_profit_qoq_growth < criteria.min_net_profit_qoq_growth):
                continue
            
            if criteria.min_eps_ttm_growth and (not stock.eps_ttm_growth or stock.eps_ttm_growth < criteria.min_eps_ttm_growth):
                continue
            
            if criteria.min_piotroski_score and (stock.piotroski_score is None or stock.piotroski_score < criteria.min_piotroski_score):
                continue
            
            if criteria.min_cash_from_operating_annual and (not stock.cash_from_operating_annual or stock.cash_from_operating_annual < criteria.min_cash_from_operating_annual):
                continue
            
            if criteria.min_net_cash_flow_annual and (not stock.net_cash_flow_annual or stock.net_cash_flow_annual < criteria.min_net_cash_flow_annual):
                continue
            
            # Trendlyne score filters
            if criteria.min_trendlyne_durability_score and (stock.trendlyne_durability_score is None or stock.trendlyne_durability_score < criteria.min_trendlyne_durability_score):
                continue
            
            if criteria.min_trendlyne_valuation_score and (stock.trendlyne_valuation_score is None or stock.trendlyne_valuation_score < criteria.min_trendlyne_valuation_score):
                continue
            
            if criteria.min_trendlyne_momentum_score and (stock.trendlyne_momentum_score is None or stock.trendlyne_momentum_score < criteria.min_trendlyne_momentum_score):
                continue
            
            if criteria.min_normalized_momentum_score and (stock.normalized_momentum_score is None or stock.normalized_momentum_score < criteria.min_normalized_momentum_score):
                continue
            
            # Sector/Industry comparison filters
            if criteria.max_pe_vs_sector and stock.pe_ttm and stock.sector_pe_ttm:
                pe_ratio_vs_sector = stock.pe_ttm / stock.sector_pe_ttm
                if pe_ratio_vs_sector > criteria.max_pe_vs_sector:
                    continue
            
            if criteria.max_pe_vs_industry and stock.pe_ttm and stock.industry_pe_ttm:
                pe_ratio_vs_industry = stock.pe_ttm / stock.industry_pe_ttm
                if pe_ratio_vs_industry > criteria.max_pe_vs_industry:
                    continue
            
            if criteria.min_revenue_growth_vs_sector and stock.revenue_growth and stock.sector_revenue_growth_annual_yoy:
                growth_ratio_vs_sector = stock.revenue_growth / stock.sector_revenue_growth_annual_yoy
                if growth_ratio_vs_sector < criteria.min_revenue_growth_vs_sector:
                    continue
            
            if criteria.min_profit_growth_vs_sector and stock.profit_growth and stock.sector_net_profit_growth_qtr_yoy:
                profit_ratio_vs_sector = stock.profit_growth / stock.sector_net_profit_growth_qtr_yoy
                if profit_ratio_vs_sector < criteria.min_profit_growth_vs_sector:
                    continue
            
            if criteria.max_pct_days_below_pe and stock.pct_days_below_current_pe and stock.pct_days_below_current_pe > criteria.max_pct_days_below_pe:
                continue
            
            if criteria.max_pct_days_below_pb and stock.pct_days_below_current_pb and stock.pct_days_below_current_pb > criteria.max_pct_days_below_pb:
                continue
            
            # Calculate score
            score = self.calculate_stock_score(stock, criteria)
            
            # Check minimum score
            if criteria.min_score and score < criteria.min_score:
                continue
            
            # Store stock with its score for sorting
            great_stocks.append((stock, score))
        
        # Sort by criteria
        if criteria.sort_by == 'score':
            great_stocks.sort(key=lambda x: x[1], reverse=True)
        elif criteria.sort_by == 'market_cap':
            great_stocks.sort(key=lambda x: x[0].market_cap or 0, reverse=True)
        elif criteria.sort_by == 'pe_ratio':
            great_stocks.sort(key=lambda x: x[0].pe_ratio or x[0].pe_ttm or float('inf'))
        elif criteria.sort_by == 'roe':
            great_stocks.sort(key=lambda x: x[0].roe or 0, reverse=True)
        elif criteria.sort_by == 'revenue_growth':
            great_stocks.sort(key=lambda x: x[0].revenue_growth or x[0].revenue_growth_qtr_yoy or 0, reverse=True)
        elif criteria.sort_by == 'trendlyne_durability_score':
            great_stocks.sort(key=lambda x: x[0].trendlyne_durability_score or 0, reverse=True)
        elif criteria.sort_by == 'trendlyne_valuation_score':
            great_stocks.sort(key=lambda x: x[0].trendlyne_valuation_score or 0, reverse=True)
        elif criteria.sort_by == 'trendlyne_momentum_score':
            great_stocks.sort(key=lambda x: x[0].trendlyne_momentum_score or 0, reverse=True)
        elif criteria.sort_by == 'piotroski_score':
            great_stocks.sort(key=lambda x: x[0].piotroski_score or 0, reverse=True)
        else:
            great_stocks.sort(key=lambda x: x[1], reverse=True)
        
        # Return stocks (without score for now, as Stock model doesn't have it)
        # In a production system, you might want to create a GreatStock model that extends Stock
        return [stock for stock, _ in great_stocks[:criteria.limit]]
    
    def calculate_statistics(self, stocks: List[Stock]) -> Dict:
        """Calculate statistics about the stock dataset"""
        if not stocks:
            return {}
        
        stats = {
            "total_stocks": len(stocks),
            "sectors": {},
            "market_cap_stats": {},
            "pe_ratio_stats": {},
            "roe_stats": {},
        }
        
        # Sector distribution
        sectors = {}
        for stock in stocks:
            if stock.sector:
                sectors[stock.sector] = sectors.get(stock.sector, 0) + 1
        stats["sectors"] = dict(sorted(sectors.items(), key=lambda x: x[1], reverse=True)[:10])
        
        # Market cap statistics
        market_caps = [s.market_cap for s in stocks if s.market_cap]
        if market_caps:
            stats["market_cap_stats"] = {
                "min": min(market_caps),
                "max": max(market_caps),
                "avg": sum(market_caps) / len(market_caps),
                "count": len(market_caps)
            }
        
        # PE ratio statistics
        pe_ratios = [s.pe_ratio for s in stocks if s.pe_ratio and s.pe_ratio > 0]
        if pe_ratios:
            stats["pe_ratio_stats"] = {
                "min": min(pe_ratios),
                "max": max(pe_ratios),
                "avg": sum(pe_ratios) / len(pe_ratios),
                "count": len(pe_ratios)
            }
        
        # ROE statistics
        roes = [s.roe for s in stocks if s.roe]
        if roes:
            stats["roe_stats"] = {
                "min": min(roes),
                "max": max(roes),
                "avg": sum(roes) / len(roes),
                "count": len(roes)
            }
        
        return stats

