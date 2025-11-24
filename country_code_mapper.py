"""
Country Code Normalization

Handles mapping between different country code standards:
- OECD ICIO uses 3-letter codes (USA, CHN, GBR)
- EXIOBASE uses 2-letter ISO codes (US, CN, GB)
- Some regions use custom codes (WLD, ROW, etc.)
"""

# Mapping from 2-letter ISO to 3-letter OECD codes
ISO2_TO_OECD = {
    'AT': 'AUT', 'AU': 'AUS', 'BE': 'BEL', 'BG': 'BGR', 'BR': 'BRA',
    'CA': 'CAN', 'CH': 'CHE', 'CN': 'CHN', 'CY': 'CYP', 'CZ': 'CZE',
    'DE': 'DEU', 'DK': 'DNK', 'EE': 'EST', 'ES': 'ESP', 'FI': 'FIN',
    'FR': 'FRA', 'GB': 'GBR', 'GR': 'GRC', 'HR': 'HRV', 'HU': 'HUN',
    'ID': 'IDN', 'IE': 'IRL', 'IN': 'IND', 'IT': 'ITA', 'JP': 'JPN',
    'KR': 'KOR', 'LT': 'LTU', 'LU': 'LUX', 'LV': 'LVA', 'MT': 'MLT',
    'MX': 'MEX', 'NL': 'NLD', 'NO': 'NOR', 'PL': 'POL', 'PT': 'PRT',
    'RO': 'ROU', 'RU': 'RUS', 'SE': 'SWE', 'SI': 'SVN', 'SK': 'SVK',
    'TR': 'TUR', 'TW': 'TWN', 'US': 'USA', 'ZA': 'ZAF',
    # Rest of World regions in EXIOBASE
    'WA': 'ROW',  # Rest of Asia
    'WE': 'ROW',  # Rest of Europe
    'WF': 'ROW',  # Rest of Africa
    'WL': 'ROW',  # Rest of Americas
    'WM': 'ROW',  # Rest of Middle East
}

# Reverse mapping from 3-letter OECD to 2-letter ISO
OECD_TO_ISO2 = {v: k for k, v in ISO2_TO_OECD.items() if v != 'ROW'}

# Additional OECD-specific codes not in EXIOBASE
OECD_ONLY = {
    'AGO', 'ARE', 'ARG', 'BGD', 'BLR', 'BRN', 'CHL', 'CMR', 'COL',
    'CRI', 'ETH', 'GHA', 'HKG', 'ISL', 'ISR', 'KAZ', 'KEN', 'KHM',
    'LAO', 'MAR', 'MDG', 'MLI', 'MMR', 'MOZ', 'MUS', 'MWI', 'MYS',
    'NAM', 'NGA', 'NZL', 'PAK', 'PER', 'PHL', 'SAU', 'SEN', 'SGP',
    'THA', 'TUN', 'TZA', 'UGA', 'UKR', 'VNM', 'ZMB', 'ZWE'
}


# Country name to code mapping for OECD ICIO
from oecd_icio_data import OECD_ICIO_COUNTRIES

# Build reverse lookup: name -> code
OECD_NAME_TO_CODE = {country['name']: country['code'] for country in OECD_ICIO_COUNTRIES}

def country_name_to_code(name: str) -> str:
    """
    Convert country name to OECD 3-letter code.
    
    Args:
        name: Country name (e.g., "United States", "China")
        
    Returns:
        3-letter OECD code (e.g., "USA", "CHN")
        
    Raises:
        ValueError: If country name not found
    """
    if name in OECD_NAME_TO_CODE:
        return OECD_NAME_TO_CODE[name]
    else:
        raise ValueError(f"Country name '{name}' not found in OECD ICIO")

def normalize_country_code(code: str, target_format: str = 'oecd') -> str:
    """
    Normalize country code to target format.
    
    Args:
        code: Country code in any format (2-letter or 3-letter)
        target_format: Target format ('oecd' for 3-letter, 'iso2' for 2-letter)
        
    Returns:
        Normalized country code
        
    Raises:
        ValueError: If code cannot be normalized to target format
    """
    code = code.upper()
    target_format = target_format.lower()
    
    if target_format == 'oecd':
        # Convert to 3-letter OECD format
        if len(code) == 3:
            return code  # Already in OECD format
        elif len(code) == 2:
            if code in ISO2_TO_OECD:
                return ISO2_TO_OECD[code]
            else:
                raise ValueError(f"Cannot convert ISO2 code '{code}' to OECD format")
        else:
            raise ValueError(f"Invalid country code: '{code}'")
    
    elif target_format == 'iso2':
        # Convert to 2-letter ISO format
        if len(code) == 2:
            return code  # Already in ISO2 format
        elif len(code) == 3:
            if code in OECD_TO_ISO2:
                return OECD_TO_ISO2[code]
            elif code in OECD_ONLY:
                raise ValueError(f"OECD code '{code}' not available in EXIOBASE (ISO2)")
            else:
                raise ValueError(f"Cannot convert OECD code '{code}' to ISO2 format")
        else:
            raise ValueError(f"Invalid country code: '{code}'")
    
    else:
        raise ValueError(f"Invalid target format: '{target_format}'. Use 'oecd' or 'iso2'")


def is_valid_for_model(code: str, model_type: str) -> bool:
    """
    Check if a country code is valid for a specific model.
    
    Args:
        code: Country code (any format)
        model_type: Model type ('oecd' or 'exiobase')
        
    Returns:
        True if code is valid for the model, False otherwise
    """
    code = code.upper()
    model_type = model_type.lower()
    
    if model_type == 'oecd':
        # OECD accepts 3-letter codes
        if len(code) == 3:
            return True
        elif len(code) == 2:
            # Check if can be converted to OECD
            return code in ISO2_TO_OECD
        return False
    
    elif model_type == 'exiobase':
        # EXIOBASE accepts 2-letter codes
        if len(code) == 2:
            return True
        elif len(code) == 3:
            # Check if can be converted to ISO2
            return code in OECD_TO_ISO2
        return False
    
    else:
        return False


def get_common_countries():
    """
    Get list of countries available in both OECD and EXIOBASE.
    
    Returns:
        List of tuples (oecd_code, iso2_code, name)
    """
    common = []
    for iso2, oecd in ISO2_TO_OECD.items():
        if oecd != 'ROW':  # Exclude Rest of World
            common.append((oecd, iso2))
    return sorted(common)


def get_model_specific_countries(model_type: str):
    """
    Get countries that are only available in a specific model.
    
    Args:
        model_type: Model type ('oecd' or 'exiobase')
        
    Returns:
        List of country codes
    """
    if model_type.lower() == 'oecd':
        return sorted(list(OECD_ONLY))
    elif model_type.lower() == 'exiobase':
        # EXIOBASE has Rest of World regions not in OECD
        return ['WA', 'WE', 'WF', 'WL', 'WM']
    else:
        return []
