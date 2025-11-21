"""
Abstract base class for Input-Output models.

This module defines the interface that all I-O models must implement,
allowing the API to work with different databases (EXIOBASE, OECD ICIO, etc.)
through a unified interface.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class Country:
    """Represents a country or region in the I-O model"""
    code: str
    name: str
    is_rest_of_world: bool = False
    is_extended: bool = False  # For firm heterogeneity splits


@dataclass
class Sector:
    """Represents an economic sector in the I-O model"""
    code: str
    name: str


@dataclass
class IOCoefficient:
    """Represents a single I-O coefficient (technical coefficient)"""
    from_country: str
    from_sector: str
    to_country: str
    to_sector: str
    coefficient: float
    
    def __repr__(self):
        return (f"IOCoefficient({self.from_country}_{self.from_sector} → "
                f"{self.to_country}_{self.to_sector}: {self.coefficient:.6f})")


@dataclass
class Supplier:
    """Represents a supplier in the supply chain"""
    country: str
    sector: str
    coefficient: float
    country_name: str = ""
    sector_name: str = ""
    
    def to_dict(self) -> Dict:
        return {
            'country': self.country,
            'sector': self.sector,
            'coefficient': self.coefficient,
            'country_name': self.country_name,
            'sector_name': self.sector_name
        }


class IOModel(ABC):
    """
    Abstract base class for Input-Output models.
    
    All I-O database implementations (EXIOBASE, OECD ICIO, etc.) must
    inherit from this class and implement all abstract methods.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the I-O model (e.g., 'EXIOBASE 3', 'OECD ICIO')"""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Return the version/year of the data (e.g., '2022', '2020')"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Return a description of the model and its characteristics"""
        pass
    
    @abstractmethod
    def get_countries(self) -> List[Country]:
        """
        Get list of all countries/regions in the model.
        
        Returns:
            List of Country objects
        """
        pass
    
    @abstractmethod
    def get_sectors(self) -> List[Sector]:
        """
        Get list of all sectors in the model.
        
        Returns:
            List of Sector objects
        """
        pass
    
    @abstractmethod
    def get_country(self, code: str) -> Optional[Country]:
        """
        Get a specific country by code.
        
        Args:
            code: Country code (e.g., 'USA', 'CHN')
            
        Returns:
            Country object or None if not found
        """
        pass
    
    @abstractmethod
    def get_sector(self, code: str) -> Optional[Sector]:
        """
        Get a specific sector by code.
        
        Args:
            code: Sector code (e.g., 'D26T27', 'C10T12')
            
        Returns:
            Sector object or None if not found
        """
        pass
    
    @abstractmethod
    def get_coefficient(
        self,
        from_country: str,
        from_sector: str,
        to_country: str,
        to_sector: str
    ) -> float:
        """
        Get the technical coefficient (A matrix element) for a specific flow.
        
        The coefficient represents how much of the 'from' country-sector's output
        is required to produce one unit of the 'to' country-sector's output.
        
        Args:
            from_country: Source country code
            from_sector: Source sector code
            to_country: Destination country code
            to_sector: Destination sector code
            
        Returns:
            Technical coefficient (0.0 if no relationship exists)
        """
        pass
    
    @abstractmethod
    def get_suppliers(
        self,
        country: str,
        sector: str,
        top_n: int = 10,
        min_coefficient: float = 0.0
    ) -> List[Supplier]:
        """
        Get the top suppliers for a specific country-sector.
        
        Args:
            country: Country code
            sector: Sector code
            top_n: Number of top suppliers to return
            min_coefficient: Minimum coefficient threshold
            
        Returns:
            List of Supplier objects, sorted by coefficient (descending)
        """
        pass
    
    @abstractmethod
    def has_environmental_data(self) -> bool:
        """
        Check if the model includes environmental satellite accounts.
        
        Returns:
            True if environmental data is available, False otherwise
        """
        pass
    
    def get_model_info(self) -> Dict:
        """
        Get comprehensive information about the model.
        
        Returns:
            Dictionary with model metadata
        """
        countries = self.get_countries()
        sectors = self.get_sectors()
        
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'country_count': len(countries),
            'sector_count': len(sectors),
            'has_environmental_data': self.has_environmental_data(),
            'countries': [c.code for c in countries],
            'sectors': [s.code for s in sectors]
        }
    
    def validate_country_sector(
        self,
        country: str,
        sector: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate that a country-sector combination exists in the model.
        
        Args:
            country: Country code
            sector: Sector code
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        country_obj = self.get_country(country)
        if not country_obj:
            return False, f"Country '{country}' not found in {self.name}"
        
        sector_obj = self.get_sector(sector)
        if not sector_obj:
            return False, f"Sector '{sector}' not found in {self.name}"
        
        return True, None
    
    def __repr__(self):
        return f"{self.name} ({self.version})"
