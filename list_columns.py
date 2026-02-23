"""List all columns in the Excel file"""
import pandas as pd
import os
import sys

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(script_dir, 'data', 'trendlyne_data.xlsx')

print(f"Looking for file: {excel_path}")
print(f"File exists: {os.path.exists(excel_path)}")
print()

if os.path.exists(excel_path):
    try:
        df = pd.read_excel(excel_path)
        print(f"Total columns: {len(df.columns)}")
        print(f"Total rows: {len(df)}")
        print("\n" + "="*100)
        print("ALL COLUMN NAMES:")
        print("="*100)
        for i, col in enumerate(df.columns, 1):
            # Show sample value
            sample_val = df[col].iloc[0] if len(df) > 0 else "N/A"
            sample_str = str(sample_val)[:50] if pd.notna(sample_val) else "NaN"
            print(f"{i:3d}. {col:70s} | Sample: {sample_str}")
        
        # Save to file
        with open('excel_columns.txt', 'w', encoding='utf-8') as f:
            f.write("ALL COLUMNS IN trendlyne_data.xlsx\n")
            f.write("="*100 + "\n")
            for i, col in enumerate(df.columns, 1):
                f.write(f"{i:3d}. {col}\n")
        print("\n" + "="*100)
        print("Column list also saved to: excel_columns.txt")
    except Exception as e:
        print(f"Error reading file: {e}")
        import traceback
        traceback.print_exc()
else:
    print(f"File not found: {excel_path}")
    print("\nTrying alternative paths...")
    alt_paths = [
        os.path.join('data', 'trendlyne_data.xlsx'),
        r'c:\Work\Trading\stock_ai\stock_api_service\data\trendlyne_data.xlsx',
    ]
    for path in alt_paths:
        if os.path.exists(path):
            print(f"Found at: {path}")
            break



