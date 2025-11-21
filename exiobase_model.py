"""
EXIOBASE Model Implementation

This module implements the IOModel interface for EXIOBASE 3 data.
"""

from typing import List, Optional
from io_model_base import IOModel, Country, Sector, Supplier
from exiobase_data import EXIOBASE_COUNTRIES, EXIOBASE_SECTORS, EXIOBASE_TO_OECD_MAPPING


class EXIOBASEModel(IOModel):
    """
    EXIOBASE 3 model implementation.
    
    Uses EXIOBASE 3 data with 49 regions and 163 industries mapped to OECD sectors.
    Includes environmental satellite accounts.
    """
    
    def __init__(self, data_path: str = '/home/ubuntu/heroku-risk-api'):
        """
        Initialize the EXIOBASE model.
        
        Args:
            data_path: Path to directory containing EXIOBASE data files
        """
        self.data_path = data_path
        self._countries_cache = None
        self._sectors_cache = None
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
    
    def get_coefficient(
        self,
        from_country: str,
        from_sector: str,
        to_country: str,
        to_sector: str
    ) -> float:
        """
        Get technical coefficient from EXIOBASE A matrix.
        
        TODO: Implement actual coefficient lookup from EXIOBASE A matrix.
        For now, returns 0.0 as placeholder.
        """
        # Placeholder - will be implemented when EXIOBASE A matrix is processed
        return 0.0
    
    def get_suppliers(
        self,
        country: str,
        sector: str,
        top_n: int = 10,
        min_coefficient: float = 0.0
    ) -> List[Supplier]:
        """
        Get top suppliers for a country-sector from EXIOBASE data.
        
        TODO: Implement actual supplier lookup from EXIOBASE A matrix.
        For now, returns empty list as placeholder.
        """
        # Placeholder - will be implemented when EXIOBASE A matrix is processed
        return []
    
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
            'status': 'Partially implemented - coefficient matrix pending'
        }
