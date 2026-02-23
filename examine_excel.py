"""Script to examine the Excel file structure"""
import pandas as pd
import os

excel_path = os.path.join('data', 'trendlyne_data.xlsx')

if os.path.exists(excel_path):
    df = pd.read_excel(excel_path)
    print(f"Total columns: {len(df.columns)}")
    print(f"Total rows: {len(df)}")
    print("\n" + "="*80)
    print("ALL COLUMN NAMES:")
    print("="*80)
    for i, col in enumerate(df.columns, 1):
        print(f"{i:3d}. {col}")
    
    print("\n" + "="*80)
    print("SAMPLE DATA (First row):")
    print("="*80)
    if len(df) > 0:
        first_row = df.iloc[0]
        for col in df.columns[:20]:  # First 20 columns
            val = first_row[col]
            print(f"{col}: {val}")
else:
    print(f"File not found: {excel_path}")



