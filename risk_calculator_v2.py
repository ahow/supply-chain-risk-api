"""
Multi-Tier Risk Calculator (Version 2)
Implements comprehensive supply chain risk assessment using IOModel interface
"""

from typing import Dict, List, Optional
from io_model_base import IOModel
from oecd_data_full import OECD_COUNTRIES, OECD_SECTORS
from sector_code_mapper import get_risk_sector_for_oecd
from climate_api_client import ClimateRiskAPIClient


class MultiTierRiskCalculator:
    """
    Calculates supply chain risk exposure using multi-tier analysis with real I-O data
    
    Methodology:
    - Direct Risk: Inherent country-sector risk (70% country + 30% sector)
    - Indirect Risk: Weighted average of supplier risks using I-O coefficients
    - Total Risk: 60% direct + 40% indirect
    
    Multi-tier weights:
    - Tier-1: 100% (direct suppliers)
    - Tier-2: 40% (suppliers' suppliers)
    - Tier-3: 16% (third-tier suppliers)
    """
    
    def __init__(self, io_model: IOModel, max_tiers: int = 3):
        """
        Initialize risk calculator with an I-O model.
        
        Args:
            io_model: IOModel instance (OECD ICIO, EXIOBASE, etc.)
            max_tiers: Maximum number of supply chain tiers to analyze
        """
        self.io_model = io_model
        self.max_tiers = max_tiers
        self.tier_weights = [1.0, 0.4, 0.16]  # 100%, 40%, 16%
        self.climate_api = ClimateRiskAPIClient()
    
    def get_countries(self) -> List[Dict]:
        """Get list of all supported countries from the I-O model"""
        countries = self.io_model.get_countries()
        return [
            {
                'code': c.code,
                'name': c.name,
                'is_rest_of_world': getattr(c, 'is_rest_of_world', False),
                'is_extended': getattr(c, 'is_extended', False)
            }
            for c in countries
        ]
    
    def get_sectors(self) -> List[Dict]:
        """Get list of all supported sectors from the I-O model"""
        sectors = self.io_model.get_sectors()
        return [
            {
                'code': s.code,
                'name': s.name
            }
            for s in sectors
        ]
    
    def calculate_direct_risk(self, country_code: str, sector_code: str) -> Optional[Dict]:
        """
        Calculate direct (inherent) risk for a country-sector.
        
        Uses risk scores from OECD_COUNTRIES and OECD_SECTORS data.
        Maps OECD ICIO sector codes to risk data sector codes if needed.
        """
        # Find country in the risk data
        country = next((c for c in OECD_COUNTRIES if c['code'] == country_code), None)
        
        # Try to map OECD ICIO sector code to risk data sector code
        try:
            risk_sector_code = get_risk_sector_for_oecd(sector_code)
        except ValueError:
            # If mapping fails, try using the code directly
            risk_sector_code = sector_code
        
        sector = next((s for s in OECD_SECTORS if s['code'] == risk_sector_code), None)
        
        if not country or not sector:
            return None
        
        # Calculate weighted combination of country and sector risk
        # Country weight: 70%, Sector weight: 30%
        direct_risk = {}
        for risk_type in ['climate', 'modern_slavery', 'political', 'water_stress', 'nature_loss']:
            country_risk = country['risk_scores'].get(risk_type, 0)
            sector_risk = sector['risk_scores'].get(risk_type, 0)
            direct_risk[risk_type] = round(0.7 * country_risk + 0.3 * sector_risk, 2)
        
        # Expected loss will be added separately if not skipped
        direct_risk['expected_loss'] = None
        
        return direct_risk
    
    def _add_climate_data(self, direct_risk: Dict, country_name: str) -> None:
        """
        Add Climate API expected loss data to direct risk.
        Called only when skip_climate=False.
        """
        climate_data = self.climate_api.get_country_risk(country_name)
        if climate_data and 'risk_breakdown' in climate_data:
            direct_risk['expected_loss'] = {
                'total_annual_loss': climate_data.get('expected_annual_loss', 0),
                'total_annual_loss_pct': climate_data.get('expected_annual_loss_pct', 0),
                'present_value_30yr': climate_data.get('present_value_30yr', 0),
                'present_value_30yr_pct': climate_data.get('present_value_30yr_pct', 0),
                'breakdown': {}
            }
            
            # Add individual hazard breakdowns
            for hazard, data in climate_data['risk_breakdown'].items():
                direct_risk['expected_loss']['breakdown'][hazard] = {
                    'annual_loss': data.get('annual_loss', 0),
                    'annual_loss_pct': data.get('annual_loss_pct', 0),
                    'confidence': data.get('confidence', 'Unknown'),
                    'details': data.get('details', '')
                }
    
    def calculate_indirect_risk(
        self,
        country_code: str,
        sector_code: str,
        current_tier: int = 1,
        visited: Optional[set] = None
    ) -> Dict:
        """
        Calculate indirect risk from suppliers using recursive multi-tier analysis.
        
        Uses real I-O coefficients from the IOModel to weight supplier contributions.
        
        Args:
            country_code: Target country
            sector_code: Target sector
            current_tier: Current tier level (1, 2, or 3)
            visited: Set of visited country-sectors to avoid cycles
        
        Returns:
            Dictionary of risk scores by type
        """
        if visited is None:
            visited = set()
        
        # Base case: max tier reached
        if current_tier > self.max_tiers:
            return {risk_type: 0.0 for risk_type in ['climate', 'modern_slavery', 'political', 'water_stress', 'nature_loss']}
        
        # Mark current node as visited
        node_id = f"{country_code}_{sector_code}"
        if node_id in visited:
            return {risk_type: 0.0 for risk_type in ['climate', 'modern_slavery', 'political', 'water_stress', 'nature_loss']}
        visited.add(node_id)
        
        # Get suppliers using real I-O coefficients from the model
        suppliers = self.io_model.get_suppliers(
            country_code,
            sector_code,
            top_n=20,  # Get top 20 suppliers
            min_coefficient=0.001  # Filter out very small coefficients
        )
        
        if not suppliers:
            return {risk_type: 0.0 for risk_type in ['climate', 'modern_slavery', 'political', 'water_stress', 'nature_loss']}
        
        # Calculate weighted risk from suppliers
        indirect_risk = {risk_type: 0.0 for risk_type in ['climate', 'modern_slavery', 'political', 'water_stress', 'nature_loss']}
        total_coefficient = sum(s.coefficient for s in suppliers)
        
        if total_coefficient == 0:
            return indirect_risk
        
        # Get tier weight for current tier
        tier_weight = self.tier_weights[current_tier - 1] if current_tier <= len(self.tier_weights) else 0.0
        
        for supplier in suppliers:
            # Calculate supplier's total risk (60% direct + 40% indirect)
            supplier_direct = self.calculate_direct_risk(supplier.country, supplier.sector)
            if not supplier_direct:
                continue
            
            # Recursive call for supplier's indirect risk (next tier)
            supplier_indirect = self.calculate_indirect_risk(
                supplier.country,
                supplier.sector,
                current_tier + 1,
                visited.copy()  # Pass a copy to avoid affecting other branches
            )
            
            # Combine direct and indirect for supplier's total risk
            supplier_total = {}
            for risk_type in ['climate', 'modern_slavery', 'political', 'water_stress', 'nature_loss']:
                supplier_total[risk_type] = (
                    0.6 * supplier_direct[risk_type] +
                    0.4 * supplier_indirect[risk_type]
                )
            
            # Weight by I-O coefficient and tier weight
            weight = (supplier.coefficient / total_coefficient) * tier_weight
            
            for risk_type in ['climate', 'modern_slavery', 'political', 'water_stress', 'nature_loss']:
                indirect_risk[risk_type] += weight * supplier_total[risk_type]
        
        # Round to 2 decimal places
        for risk_type in indirect_risk:
            indirect_risk[risk_type] = round(indirect_risk[risk_type], 2)
        
        return indirect_risk
    
    def calculate_total_risk(self, country_code: str, sector_code: str) -> Optional[Dict]:
        """
        Calculate total risk (direct + indirect) for a country-sector.
        
        Total risk = 60% direct risk + 40% indirect risk
        """
        # Validate country-sector exists in model
        is_valid, error = self.io_model.validate_country_sector(country_code, sector_code)
        if not is_valid:
            return None
        
        direct_risk = self.calculate_direct_risk(country_code, sector_code)
        if not direct_risk:
            return None
        
        indirect_risk = self.calculate_indirect_risk(country_code, sector_code)
        
        total_risk = {}
        for risk_type in ['climate', 'modern_slavery', 'political', 'water_stress', 'nature_loss']:
            total_risk[risk_type] = round(
                0.6 * direct_risk[risk_type] + 0.4 * indirect_risk[risk_type],
                2
            )
        
        return total_risk
    
    def assess_risk(self, country_code: str, sector_code: str, skip_climate: bool = False) -> Optional[Dict]:
        """
        Comprehensive risk assessment for a country-sector.
        
        Args:
            country_code: ISO country code
            sector_code: Sector code
            skip_climate: If True, skip Climate API call for faster response
        
        Returns complete assessment including:
        - Direct risk scores
        - Indirect risk scores (by tier)
        - Total risk scores
        - Top suppliers with coefficients
        - Methodology details
        """
        # Validate inputs
        is_valid, error = self.io_model.validate_country_sector(country_code, sector_code)
        if not is_valid:
            return {
                'error': error,
                'country': country_code,
                'sector': sector_code
            }
        
        # Get country and sector info
        country_obj = self.io_model.get_country(country_code)
        sector_obj = self.io_model.get_sector(sector_code)
        
        # Calculate risks
        direct_risk = self.calculate_direct_risk(country_code, sector_code)
        
        # Add Climate API data if not skipped
        if not skip_climate and direct_risk:
            self._add_climate_data(direct_risk, country_obj.name if country_obj else country_code)
        if not direct_risk:
            return {
                'error': f'Risk data not available for {country_code}_{sector_code}',
                'country': country_code,
                'sector': sector_code
            }
        
        indirect_risk = self.calculate_indirect_risk(country_code, sector_code)
        total_risk = self.calculate_total_risk(country_code, sector_code)
        
        # Get top suppliers
        suppliers = self.io_model.get_suppliers(country_code, sector_code, top_n=10)
        
        return {
            'country': {
                'code': country_code,
                'name': country_obj.name if country_obj else country_code
            },
            'sector': {
                'code': sector_code,
                'name': sector_obj.name if sector_obj else sector_code
            },
            'model': {
                'name': self.io_model.name,
                'version': self.io_model.version
            },
            'direct_risk': direct_risk,
            'indirect_risk': indirect_risk,
            'total_risk': total_risk,
            'top_suppliers': [s.to_dict() for s in suppliers],
            'methodology': {
                'direct_risk_formula': '70% country risk + 30% sector risk',
                'indirect_risk_formula': 'Weighted average of supplier total risks using I-O coefficients',
                'total_risk_formula': '60% direct risk + 40% indirect risk',
                'tier_weights': {
                    'tier_1': '100%',
                    'tier_2': '40%',
                    'tier_3': '16%'
                },
                'max_tiers': self.max_tiers
            }
        }
    
    def get_model_info(self) -> Dict:
        """Get information about the underlying I-O model"""
        return self.io_model.get_model_info()
