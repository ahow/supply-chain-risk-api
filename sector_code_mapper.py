"""
Sector Code Mapping (FIXED VERSION)

Maps between different sector classification systems:
- Risk data uses D-prefixed codes (D01T03, D10T12, etc.) - 34 aggregated sectors
- OECD ICIO uses ISIC Rev. 4 codes (A01, C10T12, etc.) - 56 detailed sectors

This fixed version includes ALL 56 OECD ICIO sectors with appropriate mappings.
"""

# Mapping from risk data codes (D-prefix) to OECD ICIO codes (ISIC)
RISK_TO_OECD_SECTOR = {
    'D01T03': 'A01',  # Agriculture (simplified - OECD splits into A01/A02/A03)
    'D05T06': 'B05',  # Mining of coal (simplified - OECD splits into B05/B06)
    'D07T08': 'B07',  # Mining of metal ores (simplified - OECD splits into B07/B08)
    'D09': 'B09',     # Mining support services
    'D10T12': 'C10T12',  # Food, beverages, tobacco
    'D13T15': 'C13T15',  # Textiles, apparel, leather
    'D16': 'C16',     # Wood products
    'D17T18': 'C17_18',  # Paper and printing (FIXED: was C17T18, should be C17_18)
    'D19': 'C19',     # Coke and petroleum
    'D20T21': 'C20',  # Chemicals (FIXED: split into C20 and C21)
    'D22': 'C22',     # Rubber and plastics
    'D23': 'C23',     # Non-metallic minerals
    'D24T25': 'C24A',  # Basic metals (OECD splits into C24A/C24B)
    'D26T27': 'C26',  # Electronics (FIXED: split into C26 and C27)
    'D28': 'C28',     # Machinery and equipment
    'D29T30': 'C29',  # Transport equipment (FIXED: split into C29, C301, C302T309)
    'D31T33': 'C31T33',  # Other manufacturing
    'D35': 'D',       # Electricity, gas (FIXED: was D35, OECD uses single letter D)
    'D36T39': 'E',    # Water, sewerage (FIXED: was D36T39, OECD uses single letter E)
    'D41T43': 'F',    # Construction
    'D45T47': 'G',    # Wholesale and retail trade
    'D49T53': 'H49',  # Transport (simplified - OECD splits)
    'D55T56': 'I',    # Accommodation and food
    'D58T60': 'J58T60',  # Publishing, media
    'D61': 'J61',     # Telecommunications
    'D62T63': 'J62_63',  # IT and information services (FIXED: was J62T63, should be J62_63)
    'D64T66': 'K64',  # Financial services (simplified - OECD splits into K64/K65/K66 and single K)
    'D68': 'L',       # Real estate (FIXED: was L68A, OECD uses single letter L)
    'D69T82': 'M69T70',  # Professional services (simplified - OECD splits, also single M)
    'D84': 'O',       # Public administration
    'D85': 'P',       # Education
    'D86T88': 'Q86',  # Health (simplified - OECD splits into Q86/Q87T88 and single Q)
    'D90T96': 'R90T92',  # Arts, entertainment (simplified - also single R and S)
    'D97T98': 'T',    # Household activities
}

# Complete mapping from OECD ICIO to risk data codes (ALL 56 sectors)
OECD_TO_RISK_SECTOR_EXTENDED = {
    # Agriculture (3 sectors → D01T03)
    'A01': 'D01T03',  # Crop and animal production
    'A02': 'D01T03',  # Forestry and logging
    'A03': 'D01T03',  # Fishing and aquaculture
    
    # Mining (5 sectors → D05T06, D07T08, D09)
    'B05': 'D05T06',  # Mining of coal
    'B06': 'D05T06',  # Oil and gas extraction
    'B07': 'D07T08',  # Mining of metal ores
    'B08': 'D07T08',  # Other mining
    'B09': 'D09',     # Mining support services
    
    # Manufacturing (23 sectors → various D-codes)
    'C10T12': 'D10T12',  # Food, beverages, tobacco
    'C13T15': 'D13T15',  # Textiles, apparel, leather
    'C16': 'D16',        # Wood products
    'C17_18': 'D17T18',  # Paper and printing (FIXED)
    'C19': 'D19',        # Coke and petroleum
    'C20': 'D20T21',     # Chemicals (FIXED: now mapped)
    'C21': 'D20T21',     # Pharmaceuticals (FIXED: now mapped)
    'C22': 'D22',        # Rubber and plastics
    'C23': 'D23',        # Non-metallic minerals
    'C24A': 'D24T25',    # Basic metals (iron/steel)
    'C24B': 'D24T25',    # Basic metals (non-ferrous)
    'C25': 'D24T25',     # Fabricated metal products
    'C26': 'D26T27',     # Electronics (FIXED: now mapped)
    'C27': 'D26T27',     # Electrical equipment (FIXED: now mapped)
    'C28': 'D28',        # Machinery and equipment
    'C29': 'D29T30',     # Motor vehicles (FIXED: now mapped)
    'C301': 'D29T30',    # Ships and boats (FIXED: now mapped)
    'C302T309': 'D29T30',  # Other transport equipment (FIXED: now mapped)
    'C31T33': 'D31T33',  # Other manufacturing
    
    # Utilities (3 sectors → D35, D36T39)
    'D': 'D35',          # Electricity, gas (FIXED: now mapped)
    'DPABR': 'D35',      # Electricity distribution (FIXED: now mapped)
    'E': 'D36T39',       # Water, sewerage (FIXED: now mapped)
    
    # Construction (1 sector → D41T43)
    'F': 'D41T43',       # Construction
    
    # Trade (1 sector → D45T47)
    'G': 'D45T47',       # Wholesale and retail trade
    
    # Transport (5 sectors → D49T53)
    'H49': 'D49T53',     # Land transport
    'H50': 'D49T53',     # Water transport
    'H51': 'D49T53',     # Air transport
    'H52': 'D49T53',     # Warehousing
    'H53': 'D49T53',     # Postal and courier
    
    # Accommodation (1 sector → D55T56)
    'I': 'D55T56',       # Accommodation and food
    
    # Information (6 sectors → D58T60, D61, D62T63)
    'J58': 'D58T60',     # Publishing
    'J58T60': 'D58T60',  # Publishing, audiovisual (FIXED: now mapped)
    'J59T60': 'D58T60',  # Audiovisual and broadcasting
    'J61': 'D61',        # Telecommunications
    'J62_63': 'D62T63',  # IT and information services (FIXED: now mapped)
    'J62T63': 'D62T63',  # Alternative format
    
    # Financial (4 sectors → D64T66)
    'K': 'D64T66',       # Financial services (single letter) (FIXED: now mapped)
    'K64': 'D64T66',     # Financial service activities
    'K65': 'D64T66',     # Insurance
    'K66': 'D64T66',     # Financial auxiliaries
    
    # Real estate (1 sector → D68)
    'L': 'D68',          # Real estate (FIXED: now mapped)
    
    # Professional services (5 sectors → D69T82)
    'M': 'D69T82',       # Professional services (single letter) (FIXED: now mapped)
    'M69T70': 'D69T82',  # Legal, accounting, management
    'M71': 'D69T82',     # Architecture and engineering
    'M72': 'D69T82',     # R&D
    'M73T75': 'D69T82',  # Advertising, market research
    
    # Administrative (5 sectors → D69T82)
    'N': 'D69T82',       # Administrative services (single letter) (FIXED: now mapped)
    'N77': 'D69T82',     # Rental and leasing
    'N78': 'D69T82',     # Employment activities
    'N79': 'D69T82',     # Travel agencies
    'N80T82': 'D69T82',  # Security, facilities
    
    # Public administration (1 sector → D84)
    'O': 'D84',          # Public administration
    
    # Education (1 sector → D85)
    'P': 'D85',          # Education
    
    # Health (3 sectors → D86T88)
    'Q': 'D86T88',       # Health services (single letter) (FIXED: now mapped)
    'Q86': 'D86T88',     # Human health activities
    'Q87T88': 'D86T88',  # Residential care
    
    # Arts and other services (6 sectors → D90T96)
    'R': 'D90T96',       # Arts and recreation (single letter) (FIXED: now mapped)
    'R90T92': 'D90T96',  # Creative, arts, entertainment
    'R93': 'D90T96',     # Sports, amusement
    'S': 'D90T96',       # Other services (single letter) (FIXED: now mapped)
    'S94': 'D90T96',     # Membership organizations
    'S95': 'D90T96',     # Repair services
    'S96': 'D90T96',     # Personal services
    
    # Households (1 sector → D97T98)
    'T': 'D97T98',       # Household activities
    
    # Extraterritorial (1 sector → no risk data equivalent, use D90T96)
    'U': 'D90T96',       # Extraterritorial organizations (FIXED: now mapped)
    
    # Final demand categories (map to closest service sectors)
    'HFCE': 'D90T96',    # Household final consumption (FIXED: now mapped)
    'NPISH': 'D90T96',   # Non-profit institutions (FIXED: now mapped)
    'GGFC': 'D84',       # Government final consumption (FIXED: now mapped)
    'GFCF': 'D41T43',    # Gross fixed capital formation (construction-related) (FIXED: now mapped)
    'INVNT': 'D45T47',   # Inventories (trade-related) (FIXED: now mapped)
}

# Reverse mapping (for reference)
RISK_TO_OECD_SECTOR_REVERSE = {v: k for k, v in OECD_TO_RISK_SECTOR_EXTENDED.items()}


def map_sector_code(code: str, from_format: str = 'risk', to_format: str = 'oecd') -> str:
    """
    Map sector code between different classification systems.
    
    Args:
        code: Sector code to map
        from_format: Source format ('risk' or 'oecd')
        to_format: Target format ('risk' or 'oecd')
        
    Returns:
        Mapped sector code
        
    Raises:
        ValueError: If mapping not found
    """
    code = code.upper()
    from_format = from_format.lower()
    to_format = to_format.lower()
    
    if from_format == to_format:
        return code
    
    if from_format == 'risk' and to_format == 'oecd':
        if code in RISK_TO_OECD_SECTOR:
            return RISK_TO_OECD_SECTOR[code]
        else:
            raise ValueError(f"Cannot map risk sector '{code}' to OECD format")
    
    elif from_format == 'oecd' and to_format == 'risk':
        if code in OECD_TO_RISK_SECTOR_EXTENDED:
            return OECD_TO_RISK_SECTOR_EXTENDED[code]
        else:
            raise ValueError(f"Cannot map OECD sector '{code}' to risk format")
    
    else:
        raise ValueError(f"Invalid format combination: {from_format} → {to_format}")


def get_risk_sector_for_oecd(oecd_code: str) -> str:
    """
    Get the risk data sector code for an OECD ICIO sector.
    
    This is used by the risk calculator to look up risk scores.
    """
    return map_sector_code(oecd_code, from_format='oecd', to_format='risk')


def get_oecd_sector_for_risk(risk_code: str) -> str:
    """
    Get the OECD ICIO sector code for a risk data sector.
    
    Note: This may not be unique as risk data aggregates some OECD sectors.
    """
    return map_sector_code(risk_code, from_format='risk', to_format='oecd')


# Validation
if __name__ == '__main__':
    from oecd_icio_data import OECD_ICIO_SECTORS
    
    print("="*60)
    print("Sector Mapping Validation")
    print("="*60)
    
    oecd_sectors = [s['code'] for s in OECD_ICIO_SECTORS]
    mapped = 0
    unmapped = []
    
    for sector in oecd_sectors:
        if sector in OECD_TO_RISK_SECTOR_EXTENDED:
            mapped += 1
        else:
            unmapped.append(sector)
    
    print(f"\nTotal OECD ICIO sectors: {len(oecd_sectors)}")
    print(f"Mapped sectors: {mapped}")
    print(f"Unmapped sectors: {len(unmapped)}")
    
    if unmapped:
        print(f"\n⚠️  Unmapped sectors:")
        for s in unmapped:
            print(f"  - {s}")
    else:
        print(f"\n✅ All {len(oecd_sectors)} sectors are mapped!")
    
    print("\n" + "="*60)
