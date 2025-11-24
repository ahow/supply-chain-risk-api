"""
OECD Country Name to ISO-3 Code Mapping

Maps the 85 OECD ICIO country names to ISO 3166-1 alpha-3 codes
for use with the Climate Risk API V4.
"""

# OECD ICIO country names mapped to ISO-3 codes
OECD_COUNTRY_CODES = {
    # Individual OECD countries
    "Australia": "AUS",
    "Austria": "AUT",
    "Belgium": "BEL",
    "Canada": "CAN",
    "Chile": "CHL",
    "Colombia": "COL",
    "Costa Rica": "CRI",
    "Czech Republic": "CZE",
    "Denmark": "DNK",
    "Estonia": "EST",
    "Finland": "FIN",
    "France": "FRA",
    "Germany": "DEU",
    "Greece": "GRC",
    "Hungary": "HUN",
    "Iceland": "ISL",
    "Ireland": "IRL",
    "Israel": "ISR",
    "Italy": "ITA",
    "Japan": "JPN",
    "South Korea": "KOR",
    "Latvia": "LVA",
    "Lithuania": "LTU",
    "Luxembourg": "LUX",
    "Mexico": "MEX",
    "Netherlands": "NLD",
    "New Zealand": "NZL",
    "Norway": "NOR",
    "Poland": "POL",
    "Portugal": "PRT",
    "Slovakia": "SVK",
    "Slovenia": "SVN",
    "Spain": "ESP",
    "Sweden": "SWE",
    "Switzerland": "CHE",
    "Turkey": "TUR",
    "United Kingdom": "GBR",
    "United States": "USA",
    
    # G20 and other major economies
    "Argentina": "ARG",
    "Brazil": "BRA",
    "Brunei Darussalam": "BRN",
    "Bulgaria": "BGR",
    "Cambodia": "KHM",
    "China": "CHN",
    "Croatia": "HRV",
    "Cyprus": "CYP",
    "Hong Kong": "HKG",
    "India": "IND",
    "Indonesia": "IDN",
    "Kazakhstan": "KAZ",
    "Laos": "LAO",
    "Malaysia": "MYS",
    "Malta": "MLT",
    "Morocco": "MAR",
    "Myanmar": "MMR",
    "Peru": "PER",
    "Philippines": "PHL",
    "Romania": "ROU",
    "Russia": "RUS",
    "Saudi Arabia": "SAU",
    "Singapore": "SGP",
    "South Africa": "ZAF",
    "Taiwan": "TWN",
    "Thailand": "THA",
    "Tunisia": "TUN",
    "Vietnam": "VNM",
    
    # Missing countries
    "Côte d'Ivoire": "CIV",
    "Brunei": "BRN",
    "Belarus": "BLR",
    "United Arab Emirates": "ARE",
    "Jordan": "JOR",
    "Democratic Republic of Congo": "COD",
    "São Tomé and Príncipe": "STP",
    
    # Other OECD ICIO countries
    "Angola": "AGO",
    "Bangladesh": "BGD",
    "Benin": "BEN",
    "Bolivia": "BOL",
    "Botswana": "BWA",
    "Burkina Faso": "BFA",
    "Cameroon": "CMR",
    "Dominican Republic": "DOM",
    "Ecuador": "ECU",
    "Egypt": "EGY",
    "El Salvador": "SLV",
    "Ethiopia": "ETH",
    "Ghana": "GHA",
    "Guatemala": "GTM",
    "Honduras": "HND",
    "Kenya": "KEN",
    "Madagascar": "MDG",
    "Mauritius": "MUS",
    "Mongolia": "MNG",
    "Mozambique": "MOZ",
    "Namibia": "NAM",
    "Nicaragua": "NIC",
    "Nigeria": "NGA",
    "Pakistan": "PAK",
    "Panama": "PAN",
    "Paraguay": "PRY",
    "Senegal": "SEN",
    "Sri Lanka": "LKA",
    "Tanzania": "TZA",
    "Uganda": "UGA",
    "Ukraine": "UKR",
    "Uruguay": "URY",
    "Venezuela": "VEN",
    "Zambia": "ZMB",
    "Zimbabwe": "ZWE",
    
    # Regional aggregates - use largest economy's code as proxy
    "Rest of OECD": "USA",  # Use USA as proxy
    "Rest of World": "CHN",  # Use China as proxy
    "Rest of Asia": "CHN",
    "Rest of Europe": "DEU",
    "Rest of Africa": "ZAF",
    "Rest of Americas": "BRA",
}

# Firm heterogeneity splits - map to parent country
FIRM_SPLITS = {
    "CN1": "CHN",  # China domestic firms → China
    "CN2": "CHN",  # China multinational firms → China
    "MX1": "MEX",  # Mexico domestic firms → Mexico
    "MX2": "MEX",  # Mexico multinational firms → Mexico
}

# ISO-3 codes that appear as names in OECD data
ISO3_AS_NAMES = {
    "ARE": "ARE",  # United Arab Emirates
    "BGD": "BGD",  # Bangladesh
    "BLR": "BLR",  # Belarus
    "COD": "COD",  # Democratic Republic of Congo
    "JOR": "JOR",  # Jordan
    "PAK": "PAK",  # Pakistan
    "STP": "STP",  # São Tomé and Príncipe
    "UKR": "UKR",  # Ukraine
}

def get_country_code(country_name_or_code: str) -> str:
    """
    Get ISO-3 country code for an OECD country name or code.
    
    Args:
        country_name_or_code: OECD ICIO country name or ISO-3 code
    
    Returns:
        ISO-3 country code (e.g., "USA", "CHN", "DEU")
    
    Raises:
        KeyError: If country not found in mapping
    """
    # Check if it's a firm split first
    if country_name_or_code in FIRM_SPLITS:
        return FIRM_SPLITS[country_name_or_code]
    
    # Check if it's already an ISO-3 code used as name
    if country_name_or_code in ISO3_AS_NAMES:
        return ISO3_AS_NAMES[country_name_or_code]
    
    # Check if it's in the country name mapping
    if country_name_or_code in OECD_COUNTRY_CODES:
        return OECD_COUNTRY_CODES[country_name_or_code]
    
    # If it's a 3-character code, assume it's already ISO-3
    if len(country_name_or_code) == 3 and country_name_or_code.isupper():
        return country_name_or_code
    
    raise KeyError(f"Country '{country_name_or_code}' not found in OECD country code mapping")

def get_all_country_codes() -> dict:
    """Get all OECD country name to ISO-3 code mappings"""
    return OECD_COUNTRY_CODES.copy()
