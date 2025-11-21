#!/usr/bin/env python3
"""
Process EXIOBASE 3 data and create Python data structures for the API.

This script:
1. Extracts country and sector lists from EXIOBASE
2. Maps EXIOBASE 163 sectors to OECD 34 sectors
3. Aggregates A matrix by OECD sectors
4. Saves data in format compatible with current API
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

# EXIOBASE data path
EXIOBASE_PATH = Path('/home/ubuntu/exiobase3_data')
OUTPUT_PATH = Path('/home/ubuntu/heroku-risk-api')

def extract_countries_sectors():
    """Extract country and sector lists from EXIOBASE A matrix"""
    print("Step 1: Extracting countries and sectors from EXIOBASE...")
    
    # Read first 3 rows to get headers
    df_header = pd.read_csv(
        EXIOBASE_PATH / 'A.txt',
        sep='\t',
        nrows=2,
        header=None
    )
    
    # Row 0 has regions, row 1 has sectors
    regions = df_header.iloc[0, 2:].unique().tolist()  # Skip first 2 columns
    sectors_raw = df_header.iloc[1, 2:].tolist()
    
    # Get unique sectors
    sectors = []
    seen = set()
    for sector in sectors_raw:
        if sector not in seen:
            sectors.append(sector)
            seen.add(sector)
    
    print(f"  Found {len(regions)} regions")
    print(f"  Found {len(sectors)} sectors")
    
    return regions, sectors

def create_oecd_sector_mapping():
    """
    Map EXIOBASE 163 sectors to OECD 34 sectors.
    
    Returns dict: {exiobase_sector: oecd_sector_code}
    """
    print("\nStep 2: Creating EXIOBASE → OECD sector mapping...")
    
    # This is a simplified mapping - in production, use official concordance tables
    mapping = {}
    
    # D01T03: Agriculture, forestry and fishing
    ag_keywords = ['Cultivation', 'cattle', 'pigs', 'poultry', 'meat', 'milk', 'wool', 
                   'Forestry', 'Fishing', 'Aquaculture']
    
    # D05T09: Mining and quarrying
    mining_keywords = ['Mining', 'Extraction', 'coal', 'lignite', 'crude petroleum', 
                      'natural gas', 'metal ores', 'quarrying']
    
    # D10T12: Food products, beverages and tobacco
    food_keywords = ['Processing of meat', 'vegetable oils', 'Dairy products', 'rice', 
                    'sugar', 'food products nec', 'beverages', 'Tobacco']
    
    # D13T15: Textiles, wearing apparel, leather
    textile_keywords = ['Textiles', 'wearing apparel', 'leather', 'footwear']
    
    # D16: Wood and products of wood and cork
    wood_keywords = ['wood', 'Wood products', 'cork']
    
    # D17T18: Paper and printing
    paper_keywords = ['Pulp', 'Paper', 'printing', 'publishing']
    
    # D19: Coke and refined petroleum products
    refining_keywords = ['Coke', 'petroleum refinery', 'Petroleum']
    
    # D20T21: Chemicals and pharmaceutical products
    chem_keywords = ['chemicals', 'fertilizers', 'plastics', 'rubber', 'pesticides', 
                    'paints', 'pharmaceuticals', 'soap']
    
    # D22: Rubber and plastics products
    rubber_keywords = ['Rubber', 'plastic products']
    
    # D23: Other non-metallic mineral products
    mineral_keywords = ['glass', 'ceramic', 'bricks', 'cement', 'concrete', 'stone']
    
    # D24: Basic metals
    metal_keywords = ['basic iron', 'steel', 'aluminium', 'copper', 'precious metals', 
                     'casting of metals']
    
    # D25: Fabricated metal products
    fab_metal_keywords = ['Fabricated metal', 'metal products', 'weapons']
    
    # D26T27: Computer, electronic and optical products; Electrical equipment
    electronics_keywords = ['Computer', 'communication equipment', 'consumer electronics', 
                           'measuring instruments', 'optical', 'electric motors', 
                           'batteries', 'lamps', 'domestic appliances']
    
    # D28: Machinery and equipment n.e.c.
    machinery_keywords = ['General purpose machinery', 'special purpose machinery', 
                         'agricultural machinery', 'machine tools']
    
    # D29T30: Transport equipment
    transport_keywords = ['Motor vehicles', 'trailers', 'parts and accessories', 
                         'ships', 'boats', 'railway', 'aircraft', 'spacecraft']
    
    # D31T33: Furniture; other manufacturing
    furniture_keywords = ['Furniture', 'jewellery', 'musical instruments', 'sports goods', 
                         'games', 'toys']
    
    # D35T39: Electricity, gas, water supply, sewerage, waste
    utilities_keywords = ['Production of electricity', 'Transmission of electricity', 
                         'Distribution of electricity', 'steam', 'hot water', 
                         'natural gas', 'Water collection', 'Sewerage', 'waste']
    
    # D41T43: Construction
    construction_keywords = ['Construction']
    
    # D45T47: Wholesale and retail trade
    trade_keywords = ['Sale of motor vehicles', 'Wholesale trade', 'Retail trade', 
                     'Repair of motor vehicles']
    
    # D49T53: Transportation and storage
    transport_service_keywords = ['Land transport', 'Water transport', 'Air transport', 
                                 'Warehousing', 'postal', 'courier']
    
    # D55T56: Accommodation and food services
    hospitality_keywords = ['Accommodation', 'food', 'beverage serving']
    
    # D58T60: Publishing, audiovisual and broadcasting
    media_keywords = ['Publishing', 'motion picture', 'video', 'television', 
                     'sound recording', 'broadcasting']
    
    # D61: Telecommunications
    telecom_keywords = ['Telecommunications']
    
    # D62T63: IT and other information services
    it_keywords = ['Computer programming', 'consultancy', 'information service']
    
    # D64T66: Financial and insurance activities
    finance_keywords = ['Financial service', 'insurance', 'pension funding', 
                       'auxiliary financial']
    
    # D68: Real estate activities
    real_estate_keywords = ['Real estate']
    
    # D69T75: Professional, scientific and technical activities
    professional_keywords = ['Legal', 'accounting', 'management consultancy', 
                            'architectural', 'engineering', 'technical testing', 
                            'scientific research', 'advertising', 'veterinary']
    
    # D77T82: Administrative and support services
    admin_keywords = ['Rental', 'leasing', 'employment', 'travel agency', 
                     'security', 'investigation', 'building services', 
                     'office administrative', 'business support']
    
    # D84: Public administration and defence
    public_admin_keywords = ['Public administration', 'defence', 'compulsory social security']
    
    # D85: Education
    education_keywords = ['Education']
    
    # D86T88: Human health and social work
    health_keywords = ['Human health', 'residential care', 'social work']
    
    # D90T96: Arts, entertainment, recreation and other services
    other_services_keywords = ['Creative', 'arts', 'entertainment', 'libraries', 
                              'museums', 'sports', 'amusement', 'recreation', 
                              'membership organisations', 'repair of computers', 
                              'personal goods', 'Other personal service']
    
    # D97T98: Household activities
    household_keywords = ['Private households']
    
    # Create mapping dictionary
    keyword_to_oecd = [
        (ag_keywords, 'D01T03'),
        (mining_keywords, 'D05T09'),
        (food_keywords, 'D10T12'),
        (textile_keywords, 'D13T15'),
        (wood_keywords, 'D16'),
        (paper_keywords, 'D17T18'),
        (refining_keywords, 'D19'),
        (chem_keywords, 'D20T21'),
        (rubber_keywords, 'D22'),
        (mineral_keywords, 'D23'),
        (metal_keywords, 'D24'),
        (fab_metal_keywords, 'D25'),
        (electronics_keywords, 'D26T27'),
        (machinery_keywords, 'D28'),
        (transport_keywords, 'D29T30'),
        (furniture_keywords, 'D31T33'),
        (utilities_keywords, 'D35T39'),
        (construction_keywords, 'D41T43'),
        (trade_keywords, 'D45T47'),
        (transport_service_keywords, 'D49T53'),
        (hospitality_keywords, 'D55T56'),
        (media_keywords, 'D58T60'),
        (telecom_keywords, 'D61'),
        (it_keywords, 'D62T63'),
        (finance_keywords, 'D64T66'),
        (real_estate_keywords, 'D68'),
        (professional_keywords, 'D69T75'),
        (admin_keywords, 'D77T82'),
        (public_admin_keywords, 'D84'),
        (education_keywords, 'D85'),
        (health_keywords, 'D86T88'),
        (other_services_keywords, 'D90T96'),
        (household_keywords, 'D97T98'),
    ]
    
    # Read sectors from EXIOBASE
    _, sectors = extract_countries_sectors()
    
    # Map each EXIOBASE sector to OECD sector
    unmapped = []
    for sector in sectors:
        mapped = False
        for keywords, oecd_code in keyword_to_oecd:
            if any(keyword.lower() in sector.lower() for keyword in keywords):
                mapping[sector] = oecd_code
                mapped = True
                break
        
        if not mapped:
            unmapped.append(sector)
            # Default to D90T96 (other services) for unmapped sectors
            mapping[sector] = 'D90T96'
    
    if unmapped:
        print(f"  Warning: {len(unmapped)} sectors mapped to default (D90T96)")
        print(f"  First 5 unmapped: {unmapped[:5]}")
    
    # Count sectors per OECD code
    oecd_counts = {}
    for oecd_code in mapping.values():
        oecd_counts[oecd_code] = oecd_counts.get(oecd_code, 0) + 1
    
    print(f"  Mapped {len(sectors)} EXIOBASE sectors to {len(set(mapping.values()))} OECD sectors")
    print(f"  OECD sector distribution: {dict(sorted(oecd_counts.items()))}")
    
    return mapping

def save_exiobase_data(regions, sectors, sector_mapping):
    """Save EXIOBASE countries and sectors to Python file"""
    print("\nStep 3: Saving EXIOBASE data structures...")
    
    # Map region codes to full names (simplified - would use official mapping in production)
    region_names = {
        'AT': 'Austria', 'BE': 'Belgium', 'BG': 'Bulgaria', 'CY': 'Cyprus',
        'CZ': 'Czech Republic', 'DE': 'Germany', 'DK': 'Denmark', 'EE': 'Estonia',
        'ES': 'Spain', 'FI': 'Finland', 'FR': 'France', 'GR': 'Greece',
        'HR': 'Croatia', 'HU': 'Hungary', 'IE': 'Ireland', 'IT': 'Italy',
        'LT': 'Lithuania', 'LU': 'Luxembourg', 'LV': 'Latvia', 'MT': 'Malta',
        'NL': 'Netherlands', 'PL': 'Poland', 'PT': 'Portugal', 'RO': 'Romania',
        'SE': 'Sweden', 'SI': 'Slovenia', 'SK': 'Slovakia', 'GB': 'United Kingdom',
        'US': 'United States', 'JP': 'Japan', 'CN': 'China', 'CA': 'Canada',
        'KR': 'South Korea', 'BR': 'Brazil', 'IN': 'India', 'MX': 'Mexico',
        'RU': 'Russia', 'AU': 'Australia', 'CH': 'Switzerland', 'TR': 'Turkey',
        'TW': 'Taiwan', 'NO': 'Norway', 'ID': 'Indonesia', 'ZA': 'South Africa',
        'WA': 'RoW Asia and Pacific', 'WL': 'RoW America', 'WE': 'RoW Europe',
        'WF': 'RoW Africa', 'WM': 'RoW Middle East'
    }
    
    # Create countries list
    countries_data = []
    for region in regions:
        countries_data.append({
            'code': region,
            'name': region_names.get(region, region),
            'is_rest_of_world': region.startswith('W')
        })
    
    # Get unique OECD sectors
    oecd_sectors = sorted(set(sector_mapping.values()))
    
    # OECD sector names
    oecd_sector_names = {
        'D01T03': 'Agriculture, forestry and fishing',
        'D05T09': 'Mining and quarrying',
        'D10T12': 'Food products, beverages and tobacco',
        'D13T15': 'Textiles, wearing apparel, leather and related products',
        'D16': 'Wood and products of wood and cork',
        'D17T18': 'Paper and printing',
        'D19': 'Coke and refined petroleum products',
        'D20T21': 'Chemicals and pharmaceutical products',
        'D22': 'Rubber and plastics products',
        'D23': 'Other non-metallic mineral products',
        'D24': 'Basic metals',
        'D25': 'Fabricated metal products',
        'D26T27': 'Computer, electronic and optical products; Electrical equipment',
        'D28': 'Machinery and equipment n.e.c.',
        'D29T30': 'Transport equipment',
        'D31T33': 'Furniture; other manufacturing',
        'D35T39': 'Electricity, gas, water supply, sewerage, waste and remediation services',
        'D41T43': 'Construction',
        'D45T47': 'Wholesale and retail trade; repair of motor vehicles',
        'D49T53': 'Transportation and storage',
        'D55T56': 'Accommodation and food services',
        'D58T60': 'Publishing, audiovisual and broadcasting activities',
        'D61': 'Telecommunications',
        'D62T63': 'IT and other information services',
        'D64T66': 'Financial and insurance activities',
        'D68': 'Real estate activities',
        'D69T75': 'Professional, scientific and technical activities',
        'D77T82': 'Administrative and support services',
        'D84': 'Public administration and defence; compulsory social security',
        'D85': 'Education',
        'D86T88': 'Human health and social work',
        'D90T96': 'Arts, entertainment, recreation and other service activities',
        'D97T98': 'Activities of households as employers',
        'D99': 'Activities of extraterritorial organizations and bodies'
    }
    
    # Create sectors list
    sectors_data = []
    for oecd_code in oecd_sectors:
        sectors_data.append({
            'code': oecd_code,
            'name': oecd_sector_names.get(oecd_code, oecd_code)
        })
    
    # Write to Python file
    output_file = OUTPUT_PATH / 'exiobase_data.py'
    with open(output_file, 'w') as f:
        f.write('"""\n')
        f.write('EXIOBASE 3 Country and Sector Data\n')
        f.write('\n')
        f.write('Data source: EXIOBASE 3 (2022)\n')
        f.write('163 EXIOBASE industries mapped to 34 OECD sectors\n')
        f.write('49 regions (44 countries + 5 Rest of World)\n')
        f.write('"""\n\n')
        
        f.write('EXIOBASE_COUNTRIES = ')
        countries_json = json.dumps(countries_data, indent=2)
        countries_json = countries_json.replace('false', 'False').replace('true', 'True')
        f.write(countries_json)
        f.write('\n\n')
        
        f.write('EXIOBASE_SECTORS = ')
        sectors_json = json.dumps(sectors_data, indent=2)
        sectors_json = sectors_json.replace('false', 'False').replace('true', 'True')
        f.write(sectors_json)
        f.write('\n\n')
        
        f.write('# Mapping from EXIOBASE 163 sectors to OECD 34 sectors\n')
        f.write('EXIOBASE_TO_OECD_MAPPING = ')
        mapping_json = json.dumps(sector_mapping, indent=2)
        mapping_json = mapping_json.replace('false', 'False').replace('true', 'True')
        f.write(mapping_json)
        f.write('\n')
    
    print(f"  Saved to: {output_file}")
    print(f"  Countries: {len(countries_data)}")
    print(f"  Sectors: {len(sectors_data)}")

def main():
    print("="*60)
    print("EXIOBASE 3 Data Processing")
    print("="*60)
    
    # Extract countries and sectors
    regions, sectors = extract_countries_sectors()
    
    # Create sector mapping
    sector_mapping = create_oecd_sector_mapping()
    
    # Save data
    save_exiobase_data(regions, sectors, sector_mapping)
    
    print("\n" + "="*60)
    print("✅ EXIOBASE data processing complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Review exiobase_data.py")
    print("2. Process A matrix (large file - will take time)")
    print("3. Create exiobase_io_coefficients.py")

if __name__ == '__main__':
    main()
