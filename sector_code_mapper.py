"""
Sector Code Mapping

Maps between different sector classification systems:
- Risk data uses D-prefixed codes (D01T03, D10T12, etc.)
- OECD ICIO uses ISIC Rev. 4 codes (A01, C10T12, etc.)
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
    'D17T18': 'C17T18',  # Paper and printing
    'D19': 'C19',     # Coke and petroleum
    'D20T21': 'C20T21',  # Chemicals and pharmaceuticals
    'D22': 'C22',     # Rubber and plastics
    'D23': 'C23',     # Non-metallic minerals
    'D24': 'C24A',    # Basic metals (OECD splits into C24A/C24B)
    'D25': 'C25',     # Fabricated metal products
    'D26T27': 'C26T27',  # Electronics and electrical equipment
    'D28': 'C28',     # Machinery and equipment
    'D29T30': 'C29T30',  # Transport equipment
    'D31T33': 'C31T33',  # Other manufacturing
    'D35T39': 'D35',  # Electricity, gas, water (simplified - OECD splits)
    'D41T43': 'F',    # Construction
    'D45T47': 'G',    # Wholesale and retail trade
    'D49T53': 'H49',  # Transport (simplified - OECD splits)
    'D55T56': 'I',    # Accommodation and food
    'D58T60': 'J58T60',  # Publishing, media, telecom
    'D61': 'J61',     # Telecommunications
    'D62T63': 'J62T63',  # IT and information services
    'D64T66': 'K64',  # Financial services (simplified - OECD splits)
    'D68': 'L68A',    # Real estate (OECD splits into L68A/L68B)
    'D69T75': 'M69T70',  # Professional services (simplified - OECD splits)
    'D77T82': 'N77',  # Administrative services (simplified - OECD splits)
    'D84': 'O',       # Public administration
    'D85': 'P',       # Education
    'D86T88': 'Q86',  # Health (simplified - OECD splits into Q86/Q87T88)
    'D90T96': 'R',    # Arts, entertainment, other services (simplified)
    'D97T98': 'T',    # Household activities
}

# Reverse mapping from OECD ICIO to risk data codes
OECD_TO_RISK_SECTOR = {v: k for k, v in RISK_TO_OECD_SECTOR.items()}

# Additional OECD sectors that map to the same risk sector
OECD_TO_RISK_SECTOR_EXTENDED = {
    **OECD_TO_RISK_SECTOR,
    # Agriculture split
    'A02': 'D01T03',  # Forestry → Agriculture
    'A03': 'D01T03',  # Fishing → Agriculture
    # Mining splits
    'B06': 'D05T06',  # Oil/gas → Mining energy
    'B08': 'D07T08',  # Other mining → Mining non-energy
    # Metals split
    'C24B': 'D24',    # Non-ferrous metals → Basic metals
    # Utilities split
    'D36': 'D35T39',  # Water supply → Utilities
    'E37T39': 'D35T39',  # Sewerage/waste → Utilities
    # Trade
    'G45': 'D45T47',  # Motor vehicles trade → Trade
    'G46': 'D45T47',  # Wholesale trade → Trade
    'G47': 'D45T47',  # Retail trade → Trade
    # Transport splits
    'H50': 'D49T53',  # Water transport → Transport
    'H51': 'D49T53',  # Air transport → Transport
    'H52': 'D49T53',  # Warehousing → Transport
    'H53': 'D49T53',  # Postal → Transport
    # Financial splits
    'K65': 'D64T66',  # Insurance → Financial
    'K66': 'D64T66',  # Financial auxiliaries → Financial
    # Real estate split
    'L68B': 'D68',    # Imputed rents → Real estate
    # Professional services splits
    'M71': 'D69T75',  # Architecture/engineering → Professional
    'M72': 'D69T75',  # R&D → Professional
    'M73T75': 'D69T75',  # Other professional → Professional
    # Administrative splits
    'N78': 'D77T82',  # Employment → Administrative
    'N79': 'D77T82',  # Travel agencies → Administrative
    'N80T82': 'D77T82',  # Security/facilities → Administrative
    # Health split
    'Q87T88': 'D86T88',  # Residential care → Health
    # Arts split
    'R90T92': 'D90T96',  # Arts/entertainment → Other services
    'R93': 'D90T96',  # Sports → Other services
    'S94': 'D90T96',  # Membership organizations → Other services
    'S95': 'D90T96',  # Repair → Other services
    'S96': 'D90T96',  # Personal services → Other services
}


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
