"""
EXIOBASE Model Implementation

This module implements the IOModel interface for EXIOBASE 3 data.
"""

from typing import List, Optional
import os
from pathlib import Path
from io_model_base import IOModel, Country, Sector, Supplier
from exiobase_data import EXIOBASE_COUNTRIES, EXIOBASE_SECTORS, EXIOBASE_TO_OECD_MAPPING


class EXIOBASEModel(IOModel):
    """
    EXIOBASE 3 model implementation.
    
    Uses EXIOBASE 3 data with 49 regions and 163 industries mapped to OECD sectors.
    Includes environmental satellite accounts.
    """
    
    def __init__(self, data_path: str = None):
        """
        Initialize the EXIOBASE model.
        
        Args:
            data_path: Path to directory containing EXIOBASE data files
        """
        if data_path is None:
            # Use directory where this file is located
            data_path = Path(__file__).parent
        self.data_path = str(data_path)
        self._countries_cache = None
        self._sectors_cache = None
        self._coefficients = None  # Lazy load
        self._load_data()
    
    def _load_data(self):
        """Load EXIOBASE data into memory"""
        # Load countries
        self._countries_cache = [
            Country(
                code=c['code'],
                name=c['name'],
                is_rest_of_world=c.get('is_rest_of_world', False)
            )
            for c in EXIOBASE_COUNTRIES
        ]
        
        # Load sectors (OECD mapped)
        self._sectors_cache = [
            Sector(code=s['code'], name=s['name'])
            for s in EXIOBASE_SECTORS
        ]
        
        # Note: EXIOBASE coefficient loading will be implemented
        # when we process the full A matrix from EXIOBASE
        # For now, this is a placeholder structure
    
    @property
    def name(self) -> str:
        return "EXIOBASE 3"
    
    @property
    def version(self) -> str:
        return "2022"
    
    @property
    def description(self) -> str:
        return ("EXIOBASE 3 (2022). Covers 49 regions (44 countries + 5 Rest of World) "
                "and 163 industries mapped to OECD sectors. "
                "Includes 2,720+ environmental indicators (CO2, water, land use). "
                "Best for: detailed sector analysis, environmental footprint, "
                "manufacturing supply chains.")
    
    def get_countries(self) -> List[Country]:
        return self._countries_cache
    
    def get_sectors(self) -> List[Sector]:
        return self._sectors_cache
    
    def get_country(self, code: str) -> Optional[Country]:
        for country in self._countries_cache:
            if country.code == code:
                return country
        return None
    
    def get_sector(self, code: str) -> Optional[Sector]:
        for sector in self._sectors_cache:
            if sector.code == code:
                return sector
        return None
    
    def _load_coefficients(self):
        """Load I-O coefficients from file (lazy loading)."""
        import pandas as pd
        import gzip
        
        coef_file = os.path.join(self.data_path, 'exiobase_io_coefficients.csv.gz')
        if not os.path.exists(coef_file):
            print(f"Warning: {coef_file} not found")
            return {}
        
        print(f"Loading EXIOBASE coefficients from {coef_file}...")
        df = pd.read_csv(coef_file, compression='gzip')
        
        coefficients = {}
        for _, row in df.iterrows():
            key = f"{row['from_country']}_{row['from_sector']}_{row['to_country']}_{row['to_sector']}"
            coefficients[key] = float(row['coefficient'])
        
        print(f"Loaded {len(coefficients)} EXIOBASE coefficients")
        return coefficients
    
    def get_coefficient(
        self,
        from_country: str,
        from_sector: str,
        to_country: str,
        to_sector: str
    ) -> float:
        """
        Get technical coefficient from EXIOBASE A matrix.
        """
        # Lazy load coefficients
        if self._coefficients is None:
            self._coefficients = self._load_coefficients()
        
        key = f"{from_country}_{from_sector}_{to_country}_{to_sector}"
        return self._coefficients.get(key, 0.0)
    
    def get_suppliers(
        self,
        country: str,
        sector: str,
        top_n: int = 10,
        min_coefficient: float = 0.0
    ) -> List[Supplier]:
        """
        Get top suppliers for a country-sector from EXIOBASE data.
        """
        # Lazy load coefficients
        if self._coefficients is None:
            self._coefficients = self._load_coefficients()
        
        suppliers = []
        
        # Find all coefficients where to_country and to_sector match
        for key, coef in self._coefficients.items():
            parts = key.split('_')
            if len(parts) == 4:
                from_c, from_s, to_c, to_s = parts
                if to_c == country and to_s == sector and coef >= min_coefficient:
                    from_country_obj = self.get_country(from_c)
                    from_sector_obj = self.get_sector(from_s)
                    
                    suppliers.append(Supplier(
                        country=from_c,
                        country_name=from_country_obj.name if from_country_obj else from_c,
                        sector=from_s,
                        sector_name=from_sector_obj.name if from_sector_obj else from_s,
                        coefficient=coef
                    ))
        
        # Sort by coefficient (descending) and return top N
        suppliers.sort(key=lambda s: s.coefficient, reverse=True)
        return suppliers[:top_n]
    
    def has_environmental_data(self) -> bool:
        """EXIOBASE includes comprehensive environmental satellite accounts"""
        return True
    
    def get_environmental_indicators(self) -> List[str]:
        """
        Get list of available environmental indicators in EXIOBASE.
        
        Returns:
            List of indicator names
        """
        # Major environmental indicator categories in EXIOBASE
        return [
            'CO2 emissions',
            'CH4 emissions',
            'N2O emissions',
            'GHG emissions (CO2 equivalent)',
            'Water consumption',
            'Water withdrawal',
            'Land occupation',
            'Energy use',
            'Material extraction',
            'Waste generation'
        ]
    
    def get_statistics(self) -> dict:
        """Get statistics about the EXIOBASE model"""
        return {
            'model': self.name,
            'version': self.version,
            'countries': len(self._countries_cache),
            'sectors': len(self._sectors_cache),
            'original_industries': 163,
            'mapped_to_oecd_sectors': len(self._sectors_cache),
            'environmental_indicators': len(self.get_environmental_indicators()),
            'has_environmental_data': True,
            'status': 'Available' if self._coefficients or os.path.exists(os.path.join(self.data_path, 'exiobase_io_coefficients.csv.gz')) else 'Coefficient matrix pending'
        }
