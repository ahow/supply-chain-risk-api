"""
Input-Output Coefficient Matrix

Simplified I-O coefficients representing key supply chain relationships
Based on OECD ICIO patterns and global trade flows

Format: {from_country}_{from_sector} → {to_country}_{to_sector}: coefficient
Coefficient represents the share of inputs from supplier in buyer's total inputs
"""

from typing import List, Dict, Optional


class IOCoefficient:
    """Represents a single input-output coefficient"""
    def __init__(self, from_country: str, from_sector: str, to_country: str, 
                 to_sector: str, coefficient: float, description: Optional[str] = None):
        self.from_country = from_country
        self.from_sector = from_sector
        self.to_country = to_country
        self.to_sector = to_sector
        self.coefficient = coefficient
        self.description = description
    
    def to_dict(self):
        return {
            'from_country': self.from_country,
            'from_sector': self.from_sector,
            'to_country': self.to_country,
            'to_sector': self.to_sector,
            'coefficient': self.coefficient,
            'description': self.description
        }


def get_io_coefficients(country: str, sector: str) -> List[IOCoefficient]:
    """
    Generate I-O coefficients for a given country-sector combination
    Returns top suppliers with their input coefficients
    """
    # Domestic self-supply coefficients (typical ranges by sector type)
    domestic_coefficients = {
        # Primary sectors - high domestic content
        'D01T03': 0.35,  # Agriculture
        'D05T06': 0.40,  # Energy mining
        'D07T08': 0.38,  # Non-energy mining
        
        # Manufacturing - moderate domestic content
        'D10T12': 0.30,  # Food
        'D13T15': 0.25,  # Textiles
        'D20T21': 0.28,  # Chemicals
        'D24T25': 0.32,  # Metals
        'D26T27': 0.20,  # Electronics (highly globalized)
        'D29T30': 0.28,  # Transport equipment
        
        # Services - high domestic content
        'D41T43': 0.45,  # Construction
        'D55T56': 0.40,  # Accommodation & food
        'D64T66': 0.50,  # Financial services
        'D85': 0.55,     # Education
        'D86T88': 0.50,  # Health
    }
    
    coefficients = []
    
    # Add domestic self-supply
    domestic_coef = domestic_coefficients.get(sector, 0.30)
    coefficients.append(IOCoefficient(
        from_country=country,
        from_sector=sector,
        to_country=country,
        to_sector=sector,
        coefficient=domestic_coef,
        description='Domestic self-supply'
    ))
    
    # Add cross-sector domestic dependencies
    add_domestic_dependencies(country, sector, coefficients)
    
    # Add international suppliers
    add_international_suppliers(country, sector, coefficients)
    
    # Normalize coefficients to sum to ~0.80 (remaining 0.20 is value-added)
    normalize_coefficients(coefficients, 0.80)
    
    return coefficients


def add_domestic_dependencies(country: str, sector: str, coefficients: List[IOCoefficient]):
    """Add cross-sector domestic input dependencies"""
    # Sector-specific domestic input patterns
    domestic_inputs = {
        # Food manufacturing depends on agriculture
        'D10T12': [
            {'sector': 'D01T03', 'coef': 0.15},  # Agriculture
            {'sector': 'D22', 'coef': 0.05},     # Packaging (plastics)
            {'sector': 'D20T21', 'coef': 0.04}   # Chemicals (preservatives)
        ],
        
        # Textiles depend on agriculture and chemicals
        'D13T15': [
            {'sector': 'D01T03', 'coef': 0.08},  # Cotton, wool
            {'sector': 'D20T21', 'coef': 0.12}   # Dyes, chemicals
        ],
        
        # Electronics depend on metals and chemicals
        'D26T27': [
            {'sector': 'D24T25', 'coef': 0.10},  # Metals
            {'sector': 'D20T21', 'coef': 0.08},  # Chemicals
            {'sector': 'D22', 'coef': 0.06}      # Plastics
        ],
        
        # Transport equipment depends on metals and electronics
        'D29T30': [
            {'sector': 'D24T25', 'coef': 0.18},  # Metals
            {'sector': 'D26T27', 'coef': 0.12},  # Electronics
            {'sector': 'D22', 'coef': 0.08}      # Rubber & plastics
        ],
        
        # Construction depends on non-metallic minerals and metals
        'D41T43': [
            {'sector': 'D23', 'coef': 0.15},     # Cement, glass
            {'sector': 'D24T25', 'coef': 0.12},  # Metals
            {'sector': 'D16', 'coef': 0.08}      # Wood products
        ],
        
        # Chemicals depend on petroleum and mining
        'D20T21': [
            {'sector': 'D19', 'coef': 0.14},     # Petroleum
            {'sector': 'D07T08', 'coef': 0.06}   # Mining
        ]
    }
    
    inputs = domestic_inputs.get(sector, [])
    for input_data in inputs:
        coefficients.append(IOCoefficient(
            from_country=country,
            from_sector=input_data['sector'],
            to_country=country,
            to_sector=sector,
            coefficient=input_data['coef'],
            description=f"Domestic input from {input_data['sector']}"
        ))


def add_international_suppliers(country: str, sector: str, coefficients: List[IOCoefficient]):
    """Add international supplier relationships"""
    # Major global supply chain patterns
    international_patterns = {
        # Electronics - highly globalized
        'D26T27': [
            {'country': 'CHN', 'sector': 'D26T27', 'coef': 0.15},
            {'country': 'TWN', 'sector': 'D26T27', 'coef': 0.08},
            {'country': 'KOR', 'sector': 'D26T27', 'coef': 0.07},
            {'country': 'JPN', 'sector': 'D26T27', 'coef': 0.06},
            {'country': 'MYS', 'sector': 'D26T27', 'coef': 0.04}
        ],
        
        # Textiles - concentrated in Asia
        'D13T15': [
            {'country': 'CHN', 'sector': 'D13T15', 'coef': 0.18},
            {'country': 'IND', 'sector': 'D13T15', 'coef': 0.10},
            {'country': 'VNM', 'sector': 'D13T15', 'coef': 0.08},
            {'country': 'BGD', 'sector': 'D13T15', 'coef': 0.06},
            {'country': 'TUR', 'sector': 'D13T15', 'coef': 0.04}
        ],
        
        # Chemicals - global trade
        'D20T21': [
            {'country': 'CHN', 'sector': 'D20T21', 'coef': 0.10},
            {'country': 'DEU', 'sector': 'D20T21', 'coef': 0.08},
            {'country': 'USA', 'sector': 'D20T21', 'coef': 0.07},
            {'country': 'JPN', 'sector': 'D20T21', 'coef': 0.05}
        ],
        
        # Metals - resource-dependent
        'D24T25': [
            {'country': 'CHN', 'sector': 'D24T25', 'coef': 0.14},
            {'country': 'JPN', 'sector': 'D24T25', 'coef': 0.06},
            {'country': 'DEU', 'sector': 'D24T25', 'coef': 0.05},
            {'country': 'KOR', 'sector': 'D24T25', 'coef': 0.04}
        ],
        
        # Transport equipment - regional supply chains
        'D29T30': [
            {'country': 'DEU', 'sector': 'D29T30', 'coef': 0.08},
            {'country': 'JPN', 'sector': 'D29T30', 'coef': 0.07},
            {'country': 'USA', 'sector': 'D29T30', 'coef': 0.06},
            {'country': 'CHN', 'sector': 'D29T30', 'coef': 0.05}
        ],
        
        # Food - regional + specialized imports
        'D10T12': [
            {'country': 'BRA', 'sector': 'D01T03', 'coef': 0.06},  # Agricultural imports
            {'country': 'ARG', 'sector': 'D01T03', 'coef': 0.04},
            {'country': 'USA', 'sector': 'D01T03', 'coef': 0.05},
            {'country': 'CHN', 'sector': 'D10T12', 'coef': 0.04}
        ]
    }
    
    # Get international suppliers for this sector
    suppliers = international_patterns.get(sector, [])
    
    # Filter out self-supply (if buyer country is in supplier list)
    suppliers = [s for s in suppliers if s['country'] != country]
    
    # Add China as default supplier for manufacturing sectors if not already included
    if sector.startswith('D') and len(sector) >= 3:
        try:
            sector_num = int(sector[1:3])
            if 10 <= sector_num <= 33:
                if not any(s['country'] == 'CHN' for s in suppliers):
                    suppliers.append({'country': 'CHN', 'sector': sector, 'coef': 0.08})
        except ValueError:
            pass
    
    for supplier in suppliers:
        coefficients.append(IOCoefficient(
            from_country=supplier['country'],
            from_sector=supplier['sector'],
            to_country=country,
            to_sector=sector,
            coefficient=supplier['coef'],
            description=f"International supply from {supplier['country']}"
        ))


def normalize_coefficients(coefficients: List[IOCoefficient], target: float):
    """Normalize coefficients to sum to target value"""
    total = sum(c.coefficient for c in coefficients)
    if total > 0 and total != target:
        factor = target / total
        for c in coefficients:
            c.coefficient = round(c.coefficient * factor, 4)


def get_suppliers(country: str, sector: str) -> List[IOCoefficient]:
    """
    Get all suppliers for a country-sector combination
    Returns suppliers sorted by coefficient (highest first)
    """
    coefficients = get_io_coefficients(country, sector)
    suppliers = [c for c in coefficients if c.to_country == country and c.to_sector == sector]
    suppliers.sort(key=lambda x: x.coefficient, reverse=True)
    return suppliers


def get_top_suppliers(country: str, sector: str, n: int = 10) -> List[IOCoefficient]:
    """Get top N suppliers by coefficient value"""
    return get_suppliers(country, sector)[:n]


def get_total_input_coverage(country: str, sector: str) -> float:
    """
    Calculate total input coefficient coverage
    (sum of all supplier coefficients)
    """
    suppliers = get_suppliers(country, sector)
    return sum(s.coefficient for s in suppliers)


# Legacy compatibility functions
def get_io_coefficient(from_country: str, from_sector: str, to_country: str, to_sector: str) -> float:
    """Get I-O coefficient between two country-sectors (legacy compatibility)"""
    suppliers = get_suppliers(to_country, to_sector)
    for supplier in suppliers:
        if supplier.from_country == from_country and supplier.from_sector == from_sector:
            return supplier.coefficient
    return 0.0
