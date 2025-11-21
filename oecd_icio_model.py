"""
OECD ICIO Model Implementation

This module implements the IOModel interface for OECD Inter-Country Input-Output tables.
"""

import pandas as pd
import gzip
from pathlib import Path
from typing import List, Optional
from io_model_base import IOModel, Country, Sector, Supplier
from oecd_icio_data import OECD_ICIO_COUNTRIES, OECD_ICIO_SECTORS
from functools import lru_cache


class OECDICIOModel(IOModel):
    """
    OECD ICIO (Inter-Country Input-Output) model implementation.
    
    Uses OECD ICIO Extended Edition data with 85 countries and 56 sectors.
    """
    
    def __init__(self, data_path: str = None):
        """
        Initialize the OECD ICIO model.
        
        Args:
            data_path: Path to directory containing OECD ICIO data files
        """
        if data_path is None:
            # Use directory where this file is located
            data_path = Path(__file__).parent
        self.data_path = Path(data_path)
        self._countries_cache = None
        self._sectors_cache = None
        self._coefficients_df = None
        self._coefficient_cache = {}
        self._load_data()
    
    def _load_data(self):
        """Load OECD ICIO data into memory"""
        # Load countries
        self._countries_cache = [
            Country(
                code=c['code'],
                name=c['name'],
                is_extended=c.get('is_extended', False)
            )
            for c in OECD_ICIO_COUNTRIES
        ]
        
        # Load sectors
        self._sectors_cache = [
            Sector(code=s['code'], name=s['name'])
            for s in OECD_ICIO_SECTORS
        ]
        
        # Load coefficients (lazy loading - only when needed)
        # The full matrix is 103 MB compressed, so we load it on first access
        self._coefficients_file = self.data_path / 'oecd_icio_coefficients_full.csv.gz'
    
    def _ensure_coefficients_loaded(self):
        """Lazy load the coefficients matrix"""
        if self._coefficients_df is None:
            print(f"Loading OECD ICIO coefficients from {self._coefficients_file}...")
            self._coefficients_df = pd.read_csv(
                self._coefficients_file,
                compression='gzip',
                index_col=0
            )
            print(f"  Loaded {self._coefficients_df.shape[0]} x {self._coefficients_df.shape[1]} matrix")
    
    @property
    def name(self) -> str:
        return "OECD ICIO Extended"
    
    @property
    def version(self) -> str:
        return "2020"
    
    @property
    def description(self) -> str:
        return ("OECD Inter-Country Input-Output tables (Extended Edition, 2020). "
                "Covers 85 countries/regions and 56 sectors (ISIC Rev. 4). "
                "Includes firm heterogeneity for China and Mexico. "
                "Best for: broad geographic coverage, developing countries, "
                "country-specific risk analysis.")
    
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
        Get technical coefficient from OECD ICIO A matrix.
        
        The coefficient represents how much of 'from_country_from_sector' output
        is needed to produce one unit of 'to_country_to_sector' output.
        
        Uses in-memory caching to speed up repeated lookups.
        """
        # Check cache first
        cache_key = (from_country, from_sector, to_country, to_sector)
        if cache_key in self._coefficient_cache:
            return self._coefficient_cache[cache_key]
        
        self._ensure_coefficients_loaded()
        
        # Construct row and column labels
        row_label = f"{from_country}_{from_sector}"
        col_label = f"{to_country}_{to_sector}"
        
        try:
            coefficient = self._coefficients_df.loc[row_label, col_label]
            result = float(coefficient) if pd.notna(coefficient) else 0.0
        except (KeyError, IndexError):
            result = 0.0
        
        # Save to cache (limit cache size to prevent memory issues)
        if len(self._coefficient_cache) < 100000:
            self._coefficient_cache[cache_key] = result
        
        return result
    
    def get_suppliers(
        self,
        country: str,
        sector: str,
        top_n: int = 10,
        min_coefficient: float = 0.0
    ) -> List[Supplier]:
        """
        Get top suppliers for a country-sector from OECD ICIO data.
        
        Returns suppliers sorted by coefficient (descending).
        """
        self._ensure_coefficients_loaded()
        
        # Get the column for this country-sector (who supplies to it)
        col_label = f"{country}_{sector}"
        
        try:
            # Get all coefficients for this country-sector
            coefficients = self._coefficients_df[col_label]
            
            # Filter by minimum coefficient
            coefficients = coefficients[coefficients > min_coefficient]
            
            # Sort descending and take top N
            top_coefficients = coefficients.nlargest(top_n)
            
            # Convert to Supplier objects
            suppliers = []
            for row_label, coef in top_coefficients.items():
                # Parse row label (format: COUNTRY_SECTOR)
                if '_' in row_label:
                    parts = row_label.split('_', 1)
                    if len(parts) == 2:
                        supplier_country, supplier_sector = parts
                        
                        # Get country and sector names
                        country_obj = self.get_country(supplier_country)
                        sector_obj = self.get_sector(supplier_sector)
                        
                        suppliers.append(Supplier(
                            country=supplier_country,
                            sector=supplier_sector,
                            coefficient=float(coef),
                            country_name=country_obj.name if country_obj else supplier_country,
                            sector_name=sector_obj.name if sector_obj else supplier_sector
                        ))
            
            return suppliers
            
        except KeyError:
            return []
    
    def has_environmental_data(self) -> bool:
        """OECD ICIO does not include environmental satellite accounts"""
        return False
    
    def get_statistics(self) -> dict:
        """Get statistics about the OECD ICIO model"""
        self._ensure_coefficients_loaded()
        
        total_elements = self._coefficients_df.shape[0] * self._coefficients_df.shape[1]
        non_zero = (self._coefficients_df > 0).sum().sum()
        
        return {
            'model': self.name,
            'version': self.version,
            'countries': len(self._countries_cache),
            'sectors': len(self._sectors_cache),
            'matrix_size': f"{self._coefficients_df.shape[0]} x {self._coefficients_df.shape[1]}",
            'total_relationships': total_elements,
            'non_zero_relationships': int(non_zero),
            'sparsity': f"{((total_elements - non_zero) / total_elements * 100):.1f}%",
            'mean_coefficient': float(self._coefficients_df[self._coefficients_df > 0].mean().mean()),
            'max_coefficient': float(self._coefficients_df.max().max())
        }
