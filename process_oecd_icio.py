#!/usr/bin/env python3
"""
Process OECD ICIO Extended data and create Python data structures for the API.

This script:
1. Extracts country and sector lists from OECD ICIO
2. Calculates technical coefficients (A matrix) from Z matrix
3. Saves data in format compatible with current API
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

# OECD ICIO data path
OECD_PATH = Path('/home/ubuntu/oecd_icio_data')
OUTPUT_PATH = Path('/home/ubuntu/heroku-risk-api')

# Use 2020 data (most recent pre-COVID year with complete data)
DATA_YEAR = 2020

def extract_countries_sectors():
    """Extract country and sector lists from OECD ICIO"""
    print(f"Step 1: Extracting countries and sectors from OECD ICIO {DATA_YEAR}...")
    
    # Read header row only
    df_header = pd.read_csv(
        OECD_PATH / f'{DATA_YEAR}.csv',
        nrows=0
    )
    
    # Get column names (country-sector codes)
    columns = df_header.columns.tolist()[1:]  # Skip 'V1' column
    
    # Parse country and sector codes
    countries_set = set()
    sectors_set = set()
    
    for col in columns:
        if '_' in col:
            country, sector = col.split('_', 1)
            countries_set.add(country)
            sectors_set.add(sector)
    
    countries = sorted(list(countries_set))
    sectors = sorted(list(sectors_set))
    
    print(f"  Found {len(countries)} countries/regions")
    print(f"  Found {len(sectors)} sectors")
    print(f"  First 10 countries: {countries[:10]}")
    print(f"  First 10 sectors: {sectors[:10]}")
    
    return countries, sectors

def get_country_name(code):
    """Map country code to full name"""
    # Comprehensive country code mapping
    country_names = {
        # OECD members
        'AUS': 'Australia', 'AUT': 'Austria', 'BEL': 'Belgium', 'CAN': 'Canada',
        'CHL': 'Chile', 'COL': 'Colombia', 'CRI': 'Costa Rica', 'CZE': 'Czech Republic',
        'DNK': 'Denmark', 'EST': 'Estonia', 'FIN': 'Finland', 'FRA': 'France',
        'DEU': 'Germany', 'GRC': 'Greece', 'HUN': 'Hungary', 'ISL': 'Iceland',
        'IRL': 'Ireland', 'ISR': 'Israel', 'ITA': 'Italy', 'JPN': 'Japan',
        'KOR': 'South Korea', 'LVA': 'Latvia', 'LTU': 'Lithuania', 'LUX': 'Luxembourg',
        'MEX': 'Mexico', 'NLD': 'Netherlands', 'NZL': 'New Zealand', 'NOR': 'Norway',
        'POL': 'Poland', 'PRT': 'Portugal', 'SVK': 'Slovakia', 'SVN': 'Slovenia',
        'ESP': 'Spain', 'SWE': 'Sweden', 'CHE': 'Switzerland', 'TUR': 'Turkey',
        'GBR': 'United Kingdom', 'USA': 'United States',
        
        # Key partners
        'ARG': 'Argentina', 'BRA': 'Brazil', 'BRN': 'Brunei', 'BGR': 'Bulgaria',
        'KHM': 'Cambodia', 'CHN': 'China', 'HRV': 'Croatia', 'CYP': 'Cyprus',
        'HKG': 'Hong Kong', 'IND': 'India', 'IDN': 'Indonesia', 'KAZ': 'Kazakhstan',
        'LAO': 'Laos', 'MYS': 'Malaysia', 'MLT': 'Malta', 'MAR': 'Morocco',
        'MMR': 'Myanmar', 'PER': 'Peru', 'PHL': 'Philippines', 'ROU': 'Romania',
        'RUS': 'Russia', 'SAU': 'Saudi Arabia', 'SGP': 'Singapore', 'ZAF': 'South Africa',
        'TWN': 'Taiwan', 'THA': 'Thailand', 'TUN': 'Tunisia', 'VNM': 'Vietnam',
        
        # Extended ICIO specific (firm heterogeneity)
        'CHNDOM': 'China (Domestic firms)', 'CHNMNE': 'China (Foreign-invested firms)',
        'MEXDOM': 'Mexico (Domestic firms)', 'MEXMNE': 'Mexico (Foreign-invested firms)',
        
        # Africa
        'AGO': 'Angola', 'BEN': 'Benin', 'BWA': 'Botswana', 'BFA': 'Burkina Faso',
        'CMR': 'Cameroon', 'CIV': "Côte d'Ivoire", 'EGY': 'Egypt', 'ETH': 'Ethiopia',
        'GHA': 'Ghana', 'KEN': 'Kenya', 'MDG': 'Madagascar', 'MWI': 'Malawi',
        'MLI': 'Mali', 'MUS': 'Mauritius', 'MOZ': 'Mozambique', 'NAM': 'Namibia',
        'NGA': 'Nigeria', 'RWA': 'Rwanda', 'SEN': 'Senegal', 'TZA': 'Tanzania',
        'UGA': 'Uganda', 'ZMB': 'Zambia', 'ZWE': 'Zimbabwe',
        
        # Rest of World
        'ROW': 'Rest of World'
    }
    
    return country_names.get(code, code)

def get_sector_name(code):
    """Map sector code to full name"""
    # ISIC Rev. 4 sector names
    sector_names = {
        'A01': 'Crop and animal production, hunting',
        'A02': 'Forestry and logging',
        'A03': 'Fishing and aquaculture',
        'B05': 'Mining of coal and lignite',
        'B06': 'Extraction of crude petroleum and natural gas',
        'B07': 'Mining of metal ores',
        'B08': 'Other mining and quarrying',
        'B09': 'Mining support service activities',
        'C10T12': 'Food products, beverages and tobacco',
        'C13T15': 'Textiles, wearing apparel, leather',
        'C16': 'Wood and products of wood',
        'C17_18': 'Paper and printing',
        'C19': 'Coke and refined petroleum products',
        'C20': 'Chemicals and chemical products',
        'C21': 'Pharmaceuticals',
        'C22': 'Rubber and plastics products',
        'C23': 'Other non-metallic mineral products',
        'C24A': 'Basic metals (iron and steel)',
        'C24B': 'Basic metals (non-ferrous)',
        'C25': 'Fabricated metal products',
        'C26': 'Computer, electronic and optical products',
        'C27': 'Electrical equipment',
        'C28': 'Machinery and equipment n.e.c.',
        'C29': 'Motor vehicles',
        'C301': 'Ships and boats',
        'C302T309': 'Other transport equipment',
        'C31T33': 'Furniture; other manufacturing',
        'D': 'Electricity, gas, steam and air conditioning',
        'E': 'Water supply; sewerage, waste management',
        'F': 'Construction',
        'G': 'Wholesale and retail trade',
        'H49': 'Land transport',
        'H50': 'Water transport',
        'H51': 'Air transport',
        'H52': 'Warehousing and support activities',
        'H53': 'Postal and courier activities',
        'I': 'Accommodation and food services',
        'J58': 'Publishing activities',
        'J59T60': 'Audiovisual and broadcasting',
        'J61': 'Telecommunications',
        'J62T63': 'IT and other information services',
        'K64': 'Financial service activities',
        'K65': 'Insurance and pension funding',
        'K66': 'Auxiliary financial activities',
        'L': 'Real estate activities',
        'M69T70': 'Legal, accounting, management consultancy',
        'M71': 'Architectural and engineering activities',
        'M72': 'Scientific research and development',
        'M73T75': 'Advertising, market research, other professional',
        'N77': 'Rental and leasing activities',
        'N78': 'Employment activities',
        'N79': 'Travel agency and tour operator',
        'N80T82': 'Security, investigation, business support',
        'O': 'Public administration and defence',
        'P': 'Education',
        'Q86': 'Human health activities',
        'Q87T88': 'Residential care and social work',
        'R90T92': 'Creative, arts and entertainment',
        'R93': 'Sports, amusement and recreation',
        'S94': 'Activities of membership organisations',
        'S95': 'Repair of computers and personal goods',
        'S96': 'Other personal service activities',
        'T': 'Household activities',
        'U': 'Extraterritorial organizations'
    }
    
    return sector_names.get(code, code)

def save_oecd_data(countries, sectors):
    """Save OECD ICIO countries and sectors to Python file"""
    print("\nStep 2: Saving OECD ICIO data structures...")
    
    # Create countries list
    countries_data = []
    for country in countries:
        countries_data.append({
            'code': country,
            'name': get_country_name(country),
            'is_extended': country.endswith('DOM') or country.endswith('MNE')
        })
    
    # Create sectors list
    sectors_data = []
    for sector in sectors:
        sectors_data.append({
            'code': sector,
            'name': get_sector_name(sector)
        })
    
     # Write to Python file
    output_file = OUTPUT_PATH / 'oecd_icio_data.py'
    with open(output_file, 'w') as f:
        f.write('"""\n')
        f.write('OECD ICIO Extended Country and Sector Data\n')
        f.write('\n')
        f.write(f'Data source: OECD ICIO Extended Edition ({DATA_YEAR})\n')
        f.write(f'{len(countries)} countries/regions (including firm heterogeneity splits)\n')
        f.write(f'{len(sectors)} sectors (ISIC Rev. 4 classification)\n')
        f.write('"""\n\n')
        
        f.write('OECD_ICIO_COUNTRIES = ')
        countries_json = json.dumps(countries_data, indent=2)
        # Convert JSON booleans to Python booleans
        countries_json = countries_json.replace('false', 'False').replace('true', 'True')
        f.write(countries_json)
        f.write('\n\n')
        
        f.write('OECD_ICIO_SECTORS = ')
        sectors_json = json.dumps(sectors_data, indent=2)
        sectors_json = sectors_json.replace('false', 'False').replace('true', 'True')
        f.write(sectors_json)
        f.write('\n')
    
    print(f"  Saved to: {output_file}")
    print(f"  Countries: {len(countries_data)}")
    print(f"  Sectors: {len(sectors_data)}")

def calculate_sample_coefficients():
    """
    Calculate a sample of technical coefficients from Z matrix.
    
    For the full matrix (4254 x 4738), we'll calculate coefficients on-demand
    rather than storing all 20+ million values in memory.
    """
    print("\nStep 3: Calculating sample technical coefficients...")
    
    # Read the Z matrix
    print(f"  Loading Z matrix from {DATA_YEAR}.csv...")
    df_z = pd.read_csv(
        OECD_PATH / f'{DATA_YEAR}.csv',
        index_col=0
    )
    
    print(f"  Z matrix shape: {df_z.shape}")
    print(f"  Total elements: {df_z.shape[0] * df_z.shape[1]:,}")
    
    # Calculate total output (x vector) - sum of each column
    x = df_z.sum(axis=0)
    
    # Calculate A matrix = Z / x (element-wise division by column totals)
    # A[i,j] = Z[i,j] / x[j] (how much of j's output is used by i)
    print("  Calculating A matrix (technical coefficients)...")
    
    # Avoid division by zero
    x_safe = x.replace(0, np.nan)
    df_a = df_z.div(x_safe, axis=1)
    df_a = df_a.fillna(0)
    
    print(f"  A matrix calculated")
    print(f"  Non-zero coefficients: {(df_a > 0).sum().sum():,}")
    print(f"  Sparsity: {((df_a == 0).sum().sum() / (df_a.shape[0] * df_a.shape[1]) * 100):.1f}%")
    
    # Save a sample for testing (first 100x100 block)
    sample_size = 100
    df_a_sample = df_a.iloc[:sample_size, :sample_size]
    
    sample_file = OUTPUT_PATH / 'oecd_icio_coefficients_sample.csv'
    df_a_sample.to_csv(sample_file)
    print(f"  Saved sample ({sample_size}x{sample_size}) to: {sample_file}")
    
    # Save full A matrix in compressed format
    print("  Saving full A matrix (this may take a few minutes)...")
    full_file = OUTPUT_PATH / 'oecd_icio_coefficients_full.csv.gz'
    df_a.to_csv(full_file, compression='gzip')
    print(f"  Saved full A matrix (compressed) to: {full_file}")
    
    # Get some statistics
    print("\n  Statistics:")
    print(f"    Mean coefficient: {df_a[df_a > 0].mean().mean():.6f}")
    print(f"    Max coefficient: {df_a.max().max():.6f}")
    print(f"    Min non-zero coefficient: {df_a[df_a > 0].min().min():.10f}")
    
    return df_a

def main():
    print("="*60)
    print("OECD ICIO Extended Data Processing")
    print("="*60)
    
    # Extract countries and sectors
    countries, sectors = extract_countries_sectors()
    
    # Save data
    save_oecd_data(countries, sectors)
    
    # Calculate coefficients
    df_a = calculate_sample_coefficients()
    
    print("\n" + "="*60)
    print("✅ OECD ICIO data processing complete!")
    print("="*60)
    print("\nFiles created:")
    print("1. oecd_icio_data.py - Countries and sectors")
    print("2. oecd_icio_coefficients_sample.csv - Sample A matrix (100x100)")
    print("3. oecd_icio_coefficients_full.csv.gz - Full A matrix (compressed)")
    print("\nNext steps:")
    print("1. Review oecd_icio_data.py")
    print("2. Test coefficient lookup")
    print("3. Integrate with API (dual-model support)")

if __name__ == '__main__':
    main()
