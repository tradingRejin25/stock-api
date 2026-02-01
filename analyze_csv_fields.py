"""
Script to analyze CSV files and show all field mappings
"""
import csv
import os
from typing import Dict, List, Set
from collections import defaultdict

def find_csv_files(data_folder: str = 'data') -> List[str]:
    """Find all CSV files matching the pattern trendlyne-filtered (N).csv"""
    csv_files = []
    
    if not os.path.exists(data_folder):
        return csv_files
    
    import re
    pattern = re.compile(r'trendlyne-filtered\s*\((\d+)\)\.csv', re.IGNORECASE)
    
    for filename in os.listdir(data_folder):
        if pattern.match(filename):
            csv_files.append(os.path.join(data_folder, filename))
    
    # Sort by file number
    def extract_number(file_path: str) -> int:
        match = pattern.match(os.path.basename(file_path))
        return int(match.group(1)) if match else 0
    
    csv_files.sort(key=extract_number)
    return csv_files

def analyze_csv_fields(csv_file: str) -> Dict[str, any]:
    """Analyze a CSV file and return all field names"""
    fields_info = {
        'file': os.path.basename(csv_file),
        'columns': [],
        'sample_values': {}
    }
    
    try:
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            
            if fieldnames:
                fields_info['columns'] = list(fieldnames)
                
                # Read first row to get sample values
                try:
                    first_row = next(reader)
                    for field in fieldnames:
                        if field:
                            fields_info['sample_values'][field] = first_row.get(field, '')
                except StopIteration:
                    pass
    
    except Exception as e:
        print(f"Error reading {csv_file}: {e}")
    
    return fields_info

def get_all_fields_from_all_files(data_folder: str = 'data') -> Dict[str, Set[str]]:
    """Get all unique fields from all CSV files"""
    csv_files = find_csv_files(data_folder)
    
    all_fields = defaultdict(set)
    file_fields = {}
    
    for csv_file in csv_files:
        info = analyze_csv_fields(csv_file)
        file_fields[info['file']] = info['columns']
        for field in info['columns']:
            if field:  # Skip empty field names
                all_fields[field].add(info['file'])
    
    return {
        'all_fields': dict(all_fields),
        'file_fields': file_fields,
        'total_files': len(csv_files)
    }

def create_field_mapping() -> Dict[str, str]:
    """Create mapping from Excel field names to API variable names"""
    # This is the current mapping from the code
    mapping = {
        # Basic Info
        'Stock': 'stock_name',
        'NSE Code': 'nse_code',
        'BSE Code': 'bse_code',
        'ISIN': 'isin',
        'Market Cap': 'market_cap',
        
        # Core Quality Metrics
        'ROE Ann  %': 'roe',
        'ROCE Ann  %': 'roce',
        'Total Debt to Total Equity Ann ': 'debt_to_equity',
        'Interest Coverage Ratio Ann ': 'interest_coverage',
        'Current Ratio Ann ': 'current_ratio',
        'Current Ratio TTM': 'current_ratio_ttm',
        'Promoter holding latest %': 'promoter_holding',
        'Promoter holding change 1Y %': 'promoter_holding_change_1y',
        
        # Growth Metrics
        'EPS TTM Growth %': 'eps_ttm_growth',
        'Operating Rev  growth TTM %': 'operating_rev_growth_ttm',
        'Net Profit Ann ': 'net_profit_ann',
        'Net Profit Ann  1Y Ago': 'net_profit_ann_1y_ago',
        'Net Profit 3Y Growth %': 'net_profit_3y_growth',
        'Net Profit 5Y Growth %': 'net_profit_5y_growth',
        'Net Profit QoQ Growth %': 'net_profit_qoq_growth',
        'OPM Ann  %': 'opm_ann',
        'OPM Ann  1Y ago %': 'opm_ann_1y_ago',
        'OPM TTM %': 'opm_ttm',
        'Basic EPS TTM': 'basic_eps_ttm',
        'Basic EPS TTM 1Y Ago': 'basic_eps_ttm_1y_ago',
        
        # Valuation Metrics
        'Industry PE TTM': 'industry_pe_ttm',
        'PEG TTM': 'peg_ttm',
        'Industry PBV TTM': 'price_to_book',
        'EV Per EBITDA Ann ': 'ev_per_ebitda_ann',
        
        # Trendlyne Scores
        'Durability Score': 'durability_score',
        'Valuation Score': 'valuation_score',
        
        # Quality Scores
        'Piotroski Score': 'piotroski_score',
        'Altman Zscore': 'altman_zscore',
        'Tobin Q Ratio': 'tobin_q_ratio',
        'Graham No ': 'graham_number',
        
        # Additional Metrics
        'EPS Qtr YoY Growth %': 'eps_qtr_yoy_growth',
        'Basic EPS QoQ Growth %': 'basic_eps_qoq_growth',
        'NPM Ann  %': 'npm_ann',
        'NPM TTM %': 'npm_ttm',
        
        # Quarterly Data
        'Basic EPS Qtr': 'basic_eps_qtr',
        'Basic EPS 1Q Ago': 'basic_eps_1q_ago',
        'Basic EPS 2Q Ago': 'basic_eps_2q_ago',
        'Net Profit Qtr': 'net_profit_qtr',
        'Net Profit 1Q Ago': 'net_profit_1q_ago',
        'Net Profit 2Q Ago': 'net_profit_2q_ago',
        'Operating Profit Margin Qtr %': 'opm_qtr',
        'OPM 1Q ago %': 'opm_1q_ago',
        'OPM Qtr 4Qtr ago %': 'opm_qtr_4q_ago',
        
        # Promoter Holding Trends
        'Promoter holding change QoQ %': 'promoter_holding_change_qoq',
        'Promoter holding change 2Y %': 'promoter_holding_change_2y',
        
        # Additional Valuation
        'Sector PE TTM': 'sector_pe_ttm',
        'Sector PBV TTM': 'sector_pbv_ttm',
        'Industry PBV TTM': 'industry_pbv_ttm',
        
        # Additional Quality Metrics
        'RoA Ann  %': 'roa_ann',
        'RoA Ann  1Y Ago %': 'roa_ann_1y_ago',
        'ROE Ann  1Y Ago %': 'roe_1y_ago',
        'ROE Ann  2Y Ago %': 'roe_2y_ago',
        'ROE Ann  3Y Ago %': 'roe_3y_ago',
        'ROCE Ann  3Y Avg %': 'roce_3y_avg',
        'ROCE Ann  5Y Avg %': 'roce_5y_avg',
        'Cash Flow Return on Assets Ann ': 'cash_flow_return_on_assets',
        'Cash Flow Return on Assets Ann  1Y ago': 'cash_flow_return_on_assets_1y_ago',
        'Cash EPS Ann ': 'cash_eps_ann',
        'Cash EPS Ann  1Y Ago': 'cash_eps_ann_1y_ago',
        'Cash EPS 1Y Growth %': 'cash_eps_1y_growth',
        'Working Capital Turnover Ann ': 'working_capital_turnover',
        'Book Value Inc Reval Reserve Ann ': 'book_value',
        'Price To Sales Ann ': 'price_to_sales_ann',
        'Price to Sales TTM': 'price_to_sales_ttm',
        'Price to Cashflow from Operations': 'price_to_cashflow',
        'Operating Profit TTM': 'operating_profit_ttm',
        'Operating Profit TTM 1Y Ago': 'operating_profit_ttm_1y_ago',
        'Operating Profit Growth Qtr YoY %': 'operating_profit_growth_qtr_yoy',
        'EBITDA Ann ': 'ebitda_ann',
        'EBITDA TTM': 'ebitda_ttm',
        'EBITDA Ann  margin %': 'ebitda_ann_margin',
        'EBITDA Ann  Margin %': 'ebitda_ann_margin',  # Alternative spelling
        'EBIT Ann  Margin %': 'ebit_ann_margin',
        'EBITDA Qtr YoY Growth %': 'ebitda_qtr_yoy_growth',
        'Promoter holding pledge percentage % Qtr': 'promoter_pledge_percentage',
        'Gross NPA ratio Qtr %': 'gross_npa_ratio',
        'Capital Adequacy Ratios Ann  %': 'capital_adequacy_ratio',
        'Industry Score': 'industry_score',
        'Sector Score': 'sector_score',
        'TL Checklist Positive Score': 'tl_checklist_positive_score',
        'TL Checklist Negative Score': 'tl_checklist_negative_score',
        
        # SWOT Analysis
        'SWOT Strengths': 'swot_strengths',
        'SWOT Weakness': 'swot_weakness',
        'SWOT Opportunities': 'swot_opportunities',
        'SWOT Threats': 'swot_threats',
        
        # Sector/Industry Metrics
        'Sector ROCE': 'sector_roce',
        'Industry ROCE': 'industry_roce',
        'Sector ROE': 'sector_roe',
        'Industry ROE': 'industry_roe',
        'Sector PEG TTM': 'sector_peg_ttm',
        'Industry PEG TTM': 'industry_peg_ttm',
        'Sector Net Profit Growth Qtr QoQ %': 'sector_net_profit_growth_qtr_qoq',
        'Sector Net Profit Growth Ann  YoY %': 'sector_net_profit_growth_ann_yoy',
        'Industry Net Profit Growth Qtr QoQ %': 'industry_net_profit_growth_qtr_qoq',
        'Industry Net Profit Growth Ann  YoY %': 'industry_net_profit_growth_ann_yoy',
        'PBV Adjusted': 'price_to_book_adjusted',
        'FC Est  1Q forward EBIT Qtr': 'fc_est_1q_forward_ebit_qtr',
        'FC Est  1Q fwd Cash EPS Qtr': 'fc_est_1q_fwd_cash_eps_qtr',
        'FC Est  1Q fwd Interest Expense Qtr': 'fc_est_1q_fwd_interest_expense_qtr',
    }
    
    return mapping

def main():
    """Main function to analyze CSV files and show field mappings"""
    data_folder = 'data'
    
    print("=" * 80)
    print("CSV FIELD ANALYSIS AND MAPPING")
    print("=" * 80)
    print()
    
    # Get all fields from all CSV files
    analysis = get_all_fields_from_all_files(data_folder)
    
    print(f"Found {analysis['total_files']} CSV file(s)")
    print()
    
    # Show all unique fields
    all_fields = analysis['all_fields']
    print(f"Total unique fields found: {len(all_fields)}")
    print()
    
    # Get current mapping
    current_mapping = create_field_mapping()
    
    print("=" * 80)
    print("FIELD MAPPING: Excel Column Name -> API Variable Name")
    print("=" * 80)
    print()
    
    # Show mapped fields
    mapped_fields = []
    unmapped_fields = []
    
    for excel_field in sorted(all_fields.keys()):
        api_var = current_mapping.get(excel_field)
        if api_var:
            mapped_fields.append((excel_field, api_var))
        else:
            unmapped_fields.append(excel_field)
    
    print(f"[MAPPED] FIELDS ({len(mapped_fields)}):")
    print("-" * 80)
    for excel_field, api_var in mapped_fields:
        files = ', '.join(sorted(all_fields[excel_field]))
        print(f"  Excel: '{excel_field:50s}' -> API: {api_var:40s} (in: {files})")
    
    print()
    print(f"[UNMAPPED] FIELDS ({len(unmapped_fields)}):")
    print("-" * 80)
    for excel_field in sorted(unmapped_fields):
        files = ', '.join(sorted(all_fields[excel_field]))
        sample_value = ""
        # Try to get sample value from first file
        for file_name, columns in analysis['file_fields'].items():
            if excel_field in columns:
                info = analyze_csv_fields(os.path.join(data_folder, file_name))
                sample_value = info['sample_values'].get(excel_field, '')[:50]
                break
        print(f"  '{excel_field:50s}' (in: {files})")
        if sample_value:
            print(f"    Sample value: {sample_value}")
    
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total fields in CSV: {len(all_fields)}")
    print(f"Mapped fields: {len(mapped_fields)}")
    print(f"Unmapped fields: {len(unmapped_fields)}")
    print(f"Coverage: {len(mapped_fields) / len(all_fields) * 100:.1f}%")
    print()

if __name__ == '__main__':
    main()

