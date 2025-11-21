"""
Multi-Tier Risk Calculator
Implements comprehensive supply chain risk assessment with I-O table analysis
"""

from typing import Dict, List, Optional
from oecd_data_full import OECD_COUNTRIES, OECD_SECTORS
from io_coefficients import get_suppliers, get_io_coefficient, get_io_coefficients

class MultiTierRiskCalculator:
    """
    Calculates supply chain risk exposure using multi-tier analysis
    
    Methodology:
    - Direct Risk: Inherent country-sector risk
    - Indirect Risk: Weighted average of supplier risks using I-O coefficients
    - Total Risk: 60% direct + 40% indirect
    
    Multi-tier weights:
    - Tier-1: 100% (direct suppliers)
    - Tier-2: 40% (suppliers' suppliers)
    - Tier-3: 16% (third-tier suppliers)
    """
    
    def __init__(self, max_tiers=3):
        self.max_tiers = max_tiers
        self.tier_weights = [1.0, 0.4, 0.16]  # 100%, 40%, 16%
    
    def get_countries(self) -> List[Dict]:
        """Get list of all supported countries"""
        return [
            {
                'code': c['code'],
                'name': c['name']
            }
            for c in OECD_COUNTRIES
        ]
    
    def get_sectors(self) -> List[Dict]:
        """Get list of all supported sectors"""
        return [
            {
                'code': s['code'],
                'name': s['name']
            }
            for s in OECD_SECTORS
        ]
    
    def calculate_direct_risk(self, country_code: str, sector_code: str) -> Optional[Dict]:
        """Calculate direct (inherent) risk for a country-sector"""
        country = next((c for c in OECD_COUNTRIES if c['code'] == country_code), None)
        sector = next((s for s in OECD_SECTORS if s['code'] == sector_code), None)
        
        if not country or not sector:
            return None
        
        # Calculate weighted combination of country and sector risk
        # Country weight: 70%, Sector weight: 30%
        direct_risk = {}
        for risk_type in ['climate', 'modern_slavery', 'political', 'water_stress', 'nature_loss']:
            country_risk = country['risk_scores'].get(risk_type, 0)
            sector_risk = sector['risk_scores'].get(risk_type, 0)
            direct_risk[risk_type] = round(0.7 * country_risk + 0.3 * sector_risk, 2)
        
        return direct_risk
    
    def calculate_indirect_risk(
        self,
        country_code: str,
        sector_code: str,
        current_tier: int = 1,
        visited: Optional[set] = None
    ) -> Dict:
        """
        Calculate indirect risk from suppliers using recursive multi-tier analysis
        
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
        
        # Get suppliers for this country-sector
        suppliers = get_suppliers(country_code, sector_code)
        
        if not suppliers:
            return {risk_type: 0.0 for risk_type in ['climate', 'modern_slavery', 'political', 'water_stress', 'nature_loss']}
        
        # Initialize weighted risk accumulator
        weighted_risk = {risk_type: 0.0 for risk_type in ['climate', 'modern_slavery', 'political', 'water_stress', 'nature_loss']}
        total_coefficient = 0.0
        
        # Calculate weighted average of supplier risks
        for supplier in suppliers:
            supplier_country = supplier.from_country
            supplier_sector = supplier.from_sector
            coefficient = supplier.coefficient
            
            # Get direct risk of supplier
            supplier_direct_risk = self.calculate_direct_risk(supplier_country, supplier_sector)
            
            if supplier_direct_risk:
                # Recursively get indirect risk from supplier's suppliers
                supplier_indirect_risk = self.calculate_indirect_risk(
                    supplier_country,
                    supplier_sector,
                    current_tier + 1,
                    visited.copy()
                )
                
                # Apply tier weight
                tier_weight = self.tier_weights[min(current_tier - 1, len(self.tier_weights) - 1)]
                
                # Combine supplier's direct and indirect risk
                for risk_type in weighted_risk.keys():
                    supplier_total = (
                        0.6 * supplier_direct_risk[risk_type] +
                        0.4 * supplier_indirect_risk.get(risk_type, 0)
                    )
                    weighted_risk[risk_type] += coefficient * tier_weight * supplier_total
                
                total_coefficient += coefficient * tier_weight
        
        # Normalize by total coefficient
        if total_coefficient > 0:
            for risk_type in weighted_risk.keys():
                weighted_risk[risk_type] = round(weighted_risk[risk_type] / total_coefficient, 2)
        
        return weighted_risk
    
    def calculate_risk(self, country_code: str, sector_code: str) -> Dict:
        """
        Calculate comprehensive risk assessment with direct, indirect, and total risk
        
        Returns:
            Complete risk assessment including:
            - direct_risk: Inherent country-sector risk
            - indirect_risk: Risk from suppliers
            - total_risk: Combined risk (60% direct + 40% indirect)
            - tier_breakdown: Supplier contributions by tier
        """
        # Validate inputs
        country = next((c for c in OECD_COUNTRIES if c['code'] == country_code), None)
        sector = next((s for s in OECD_SECTORS if s['code'] == sector_code), None)
        
        if not country:
            return {'error': f'Country code {country_code} not found'}
        
        if not sector:
            return {'error': f'Sector code {sector_code} not found'}
        
        # Calculate direct risk
        direct_risk = self.calculate_direct_risk(country_code, sector_code)
        
        # Calculate indirect risk
        indirect_risk = self.calculate_indirect_risk(country_code, sector_code)
        
        # Calculate total risk (60% direct + 40% indirect)
        total_risk = {}
        for risk_type in direct_risk.keys():
            total_risk[risk_type] = round(
                0.6 * direct_risk[risk_type] + 0.4 * indirect_risk[risk_type],
                2
            )
        
        # Get top suppliers for transparency
        suppliers = get_suppliers(country_code, sector_code)
        top_suppliers = sorted(suppliers, key=lambda x: x.coefficient, reverse=True)[:10]
        
        return {
            'country': country_code,
            'country_name': country['name'],
            'sector': sector_code,
            'sector_name': sector['name'],
            'direct_risk': direct_risk,
            'indirect_risk': indirect_risk,
            'total_risk': total_risk,
            'top_suppliers': [
                {
                    'country': s.from_country,
                    'sector': s.from_sector,
                    'coefficient': round(s.coefficient, 4),
                    'country_name': next((c['name'] for c in OECD_COUNTRIES if c['code'] == s.from_country), s.from_country),
                    'sector_name': next((sec['name'] for sec in OECD_SECTORS if sec['code'] == s.from_sector), s.from_sector)
                }
                for s in top_suppliers
            ],
            'methodology': {
                'direct_risk': '70% country risk + 30% sector risk',
                'indirect_risk': 'Weighted average of supplier risks using I-O coefficients',
                'total_risk': '60% direct risk + 40% indirect risk',
                'tier_weights': 'Tier-1: 100%, Tier-2: 40%, Tier-3: 16%'
            }
        }
