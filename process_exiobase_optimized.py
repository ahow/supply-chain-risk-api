#!/usr/bin/env python3
"""
Optimized EXIOBASE 3 A-matrix processor using chunked reading and sparse storage.
Processes the 602 MB A.txt file without loading entire matrix into memory.
"""

import gzip
import csv
from collections import defaultdict
from exiobase_data import EXIOBASE_TO_OECD_MAPPING

print("Starting optimized EXIOBASE coefficient processing...")
print("Reading A.txt in streaming mode (602 MB file)...")

# Read headers first
with open('/home/ubuntu/exiobase3_data/A.txt', 'r') as f:
    header_region = f.readline().strip().split('\t')[2:]  # Skip first two cols
    header_sector = f.readline().strip().split('\t')[2:]

print(f"Matrix dimensions: {len(header_region)} columns")

# Create column mapping (EXIOBASE sector -> OECD sector)
col_mapping = []
for region, sector in zip(header_region, header_sector):
    oecd_sector = None
    
    # Try to find mapping
    for exio_key, oecd_code in EXIOBASE_TO_OECD_MAPPING.items():
        if exio_key in sector or sector.startswith(exio_key):
            oecd_sector = oecd_code
            break
    
    # Default mappings
    if not oecd_sector:
        sector_lower = sector.lower()
        if any(word in sector_lower for word in ['crop', 'animal', 'fish', 'agriculture', 'forestry']):
            oecd_sector = 'D01T03'
        elif any(word in sector_lower for word in ['mining', 'extraction', 'quarrying']):
            oecd_sector = 'D05T09'
        elif any(word in sector_lower for word in ['food', 'beverage', 'tobacco']):
            oecd_sector = 'D10T12'
        elif any(word in sector_lower for word in ['textile', 'wearing', 'apparel', 'leather']):
            oecd_sector = 'D13T15'
        elif any(word in sector_lower for word in ['wood', 'paper', 'printing']):
            oecd_sector = 'D16T18'
        elif any(word in sector_lower for word in ['chemical', 'pharmaceutical']):
            oecd_sector = 'D19T23'
        elif any(word in sector_lower for word in ['metal', 'fabricated']):
            oecd_sector = 'D24T25'
        elif any(word in sector_lower for word in ['computer', 'electronic', 'optical']):
            oecd_sector = 'D26T27'
        elif any(word in sector_lower for word in ['machinery', 'equipment']):
            oecd_sector = 'D28'
        elif any(word in sector_lower for word in ['motor', 'vehicle', 'transport']):
            oecd_sector = 'D29T30'
        elif any(word in sector_lower for word in ['electricity', 'gas', 'steam']):
            oecd_sector = 'D35'
        elif any(word in sector_lower for word in ['water', 'sewerage', 'waste']):
            oecd_sector = 'D36T39'
        elif any(word in sector_lower for word in ['construction']):
            oecd_sector = 'D41T43'
        elif any(word in sector_lower for word in ['trade', 'retail', 'wholesale']):
            oecd_sector = 'D45T47'
        elif any(word in sector_lower for word in ['transport', 'storage']):
            oecd_sector = 'D49T53'
        elif any(word in sector_lower for word in ['accommodation', 'food service', 'hotel', 'restaurant']):
            oecd_sector = 'D55T56'
        elif any(word in sector_lower for word in ['publishing', 'broadcasting', 'telecom', 'information']):
            oecd_sector = 'D58T63'
        elif any(word in sector_lower for word in ['financial', 'insurance']):
            oecd_sector = 'D64T66'
        elif any(word in sector_lower for word in ['real estate']):
            oecd_sector = 'D68'
        elif any(word in sector_lower for word in ['professional', 'scientific', 'technical']):
            oecd_sector = 'D69T75'
        elif any(word in sector_lower for word in ['administrative', 'support']):
            oecd_sector = 'D77T82'
        elif any(word in sector_lower for word in ['public', 'administration', 'defence']):
            oecd_sector = 'D84'
        elif any(word in sector_lower for word in ['education']):
            oecd_sector = 'D85'
        elif any(word in sector_lower for word in ['health', 'social']):
            oecd_sector = 'D86T88'
        elif any(word in sector_lower for word in ['arts', 'entertainment', 'recreation']):
            oecd_sector = 'D90T93'
        else:
            oecd_sector = 'D94T98'  # Other services
    
    col_mapping.append((region, oecd_sector))

print(f"Column mapping created: {len(col_mapping)} columns")

# Process file line by line and aggregate
aggregated = defaultdict(float)
row_count = 0

print("\nProcessing matrix rows (this will take 5-10 minutes)...")

with open('/home/ubuntu/exiobase3_data/A.txt', 'r') as f:
    # Skip header rows
    f.readline()
    f.readline()
    
    for line in f:
        row_count += 1
        if row_count % 1000 == 0:
            print(f"  Processed {row_count} rows, aggregated coefficients: {len(aggregated)}")
        
        parts = line.strip().split('\t')
        if len(parts) < 3:
            continue
        
        from_region = parts[0]
        from_sector = parts[1]
        values = parts[2:]
        
        # Map from_sector to OECD
        from_oecd = None
        for exio_key, oecd_code in EXIOBASE_TO_OECD_MAPPING.items():
            if exio_key in from_sector or from_sector.startswith(exio_key):
                from_oecd = oecd_code
                break
        
        if not from_oecd:
            sector_lower = from_sector.lower()
            if any(word in sector_lower for word in ['crop', 'animal', 'fish']):
                from_oecd = 'D01T03'
            elif any(word in sector_lower for word in ['mining', 'extraction']):
                from_oecd = 'D05T09'
            else:
                from_oecd = 'D10T12'
        
        # Process each column value
        for col_idx, value_str in enumerate(values):
            if col_idx >= len(col_mapping):
                break
            
            try:
                value = float(value_str)
                if value != 0 and abs(value) > 1e-10:  # Skip near-zero values
                    to_region, to_oecd = col_mapping[col_idx]
                    key = f"{from_region}_{from_oecd}_{to_region}_{to_oecd}"
                    aggregated[key] += value
            except (ValueError, IndexError):
                continue

print(f"\n✅ Processing complete!")
print(f"Total rows processed: {row_count}")
print(f"Aggregated coefficients: {len(aggregated)}")

# Write to compressed CSV
output_file = '/home/ubuntu/heroku-risk-api/exiobase_io_coefficients.csv.gz'
print(f"\nWriting to {output_file}...")

with gzip.open(output_file, 'wt', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['from_country', 'from_sector', 'to_country', 'to_sector', 'coefficient'])
    
    for key, coef in aggregated.items():
        parts = key.split('_')
        if len(parts) == 4:
            writer.writerow([parts[0], parts[1], parts[2], parts[3], coef])

import os
file_size = os.path.getsize(output_file) / (1024 * 1024)
print(f"✅ Saved! File size: {file_size:.1f} MB")

# Calculate statistics
values = list(aggregated.values())
print(f"\nSummary Statistics:")
print(f"Total coefficients: {len(values):,}")
print(f"Mean coefficient: {sum(values)/len(values):.6f}")
print(f"Max coefficient: {max(values):.6f}")
print(f"Min coefficient: {min(values):.6f}")

print("\n✅ EXIOBASE coefficient processing complete!")
