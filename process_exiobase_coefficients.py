#!/usr/bin/env python3
"""
Process EXIOBASE 3 A-matrix (technical coefficients) and create compressed coefficient file.
The A.txt file contains a 7,161 × 7,161 matrix (163 sectors × 49 regions).
We'll aggregate this to OECD 34-sector classification for consistency.
"""
import os

import pandas as pd
import gzip
import json
from exiobase_data import EXIOBASE_COUNTRIES, EXIOBASE_SECTORS, EXIOBASE_TO_OECD_MAPPING

print("Loading EXIOBASE A-matrix...")
print("This is a 602 MB file with 7,161 × 7,161 = 51.3 million elements")
print("Processing may take 5-10 minutes...")

# Load A.txt - skip first 2 header rows
df = pd.read_csv(
    '/home/ubuntu/exiobase3_data/A.txt',
    sep='\t',
    skiprows=2,
    index_col=[0, 1],  # region and sector as multi-index
    low_memory=False
)

print(f"Loaded matrix shape: {df.shape}")
print(f"Matrix size: {df.shape[0]} × {df.shape[1]}")

# Get column headers (also region-sector pairs)
# The columns are in the first two rows
with open('/home/ubuntu/exiobase3_data/A.txt', 'r') as f:
    header_region = f.readline().strip().split('\t')[2:]  # Skip first two cols
    header_sector = f.readline().strip().split('\t')[2:]

print(f"Number of columns: {len(header_region)}")

# Create aggregation mapping for EXIOBASE sectors to OECD sectors
print("\nAggregating EXIOBASE 163 sectors to OECD 34 sectors...")

# Map each EXIOBASE sector to OECD sector
row_mapping = {}
for idx, (region, sector) in enumerate(df.index):
    oecd_sector = None
    for exio_sect, oecd_sect in EXIOBASE_TO_OECD_MAPPING.items():
        if sector.startswith(exio_sect) or exio_sect in sector:
            oecd_sector = oecd_sect
            break
    
    if not oecd_sector:
        # Default mapping for unmapped sectors
        if 'crop' in sector.lower() or 'animal' in sector.lower() or 'fish' in sector.lower():
            oecd_sector = 'D01T03'
        elif 'mining' in sector.lower() or 'extraction' in sector.lower():
            oecd_sector = 'D05T09'
        else:
            oecd_sector = 'D10T12'  # Default to food/manufacturing
    
    row_mapping[idx] = (region, oecd_sector)

col_mapping = {}
for idx, (region, sector) in enumerate(zip(header_region, header_sector)):
    oecd_sector = None
    for exio_sect, oecd_sect in EXIOBASE_TO_OECD_MAPPING.items():
        if sector.startswith(exio_sect) or exio_sect in sector:
            oecd_sector = oecd_sect
            break
    
    if not oecd_sector:
        if 'crop' in sector.lower() or 'animal' in sector.lower() or 'fish' in sector.lower():
            oecd_sector = 'D01T03'
        elif 'mining' in sector.lower() or 'extraction' in sector.lower():
            oecd_sector = 'D05T09'
        else:
            oecd_sector = 'D10T12'
    
    col_mapping[idx] = (region, oecd_sector)

print(f"Mapped {len(row_mapping)} rows and {len(col_mapping)} columns")

# Create aggregated matrix
print("\nAggregating matrix by OECD sectors...")
aggregated_data = {}

for row_idx, (from_region, from_sector) in row_mapping.items():
    for col_idx, (to_region, to_sector) in col_mapping.items():
        key = f"{from_region}_{from_sector}_{to_region}_{to_sector}"
        value = df.iloc[row_idx, col_idx]
        
        if pd.notna(value) and value != 0:
            if key in aggregated_data:
                aggregated_data[key] += float(value)
            else:
                aggregated_data[key] = float(value)

print(f"Aggregated to {len(aggregated_data)} non-zero coefficients")

# Convert to DataFrame for easier saving
print("\nCreating coefficient DataFrame...")
rows = []
for key, coef in aggregated_data.items():
    parts = key.split('_')
    if len(parts) == 4:
        from_region, from_sector, to_region, to_sector = parts
        rows.append({
            'from_country': from_region,
            'from_sector': from_sector,
            'to_country': to_region,
            'to_sector': to_sector,
            'coefficient': coef
        })

coef_df = pd.DataFrame(rows)

print(f"Created DataFrame with {len(coef_df)} rows")
print("\nSample coefficients:")
print(coef_df.head(10))

# Save as compressed CSV
output_file = '/home/ubuntu/heroku-risk-api/exiobase_io_coefficients.csv.gz'
print(f"\nSaving to {output_file}...")
coef_df.to_csv(output_file, index=False, compression='gzip')

file_size = os.path.getsize(output_file) / (1024 * 1024)
print(f"Saved! File size: {file_size:.1f} MB")

# Create summary statistics
print("\nSummary Statistics:")
print(f"Total coefficients: {len(coef_df):,}")
print(f"Mean coefficient: {coef_df['coefficient'].mean():.6f}")
print(f"Median coefficient: {coef_df['coefficient'].median():.6f}")
print(f"Max coefficient: {coef_df['coefficient'].max():.6f}")
print(f"Min coefficient: {coef_df['coefficient'].min():.6f}")

# Count unique country-sector pairs
unique_from = coef_df[['from_country', 'from_sector']].drop_duplicates()
unique_to = coef_df[['to_country', 'to_sector']].drop_duplicates()
print(f"\nUnique source country-sectors: {len(unique_from)}")
print(f"Unique destination country-sectors: {len(unique_to)}")

print("\n✅ EXIOBASE coefficient processing complete!")
