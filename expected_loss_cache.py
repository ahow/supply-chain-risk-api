"""Expected Loss Cache

Pre-computes and caches expected loss data for all countries to enable
fast supplier-level expected loss calculations without repeated Climate API calls.
"""
import json
import os
from typing import Dict, Optional
from climate_api_client import ClimateRiskAPIClient
from country_codes import get_country_code


class ExpectedLossCache:
    """Manages cached expected loss data for countries"""
    
    def __init__(self, cache_file: str = "expected_loss_cache.json"):
        self.cache_file = cache_file
        self.cache: Dict[str, Dict] = {}
        self.climate_client = ClimateRiskAPIClient()
        self.load_cache()
    
    def load_cache(self):
        """Load cache from file if it exists"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    self.cache = json.load(f)
                print(f"[ExpectedLossCache] Loaded {len(self.cache)} countries from cache")
            except Exception as e:
                print(f"[ExpectedLossCache] Error loading cache: {e}")
                self.cache = {}
        else:
            print(f"[ExpectedLossCache] No cache file found, starting empty")
            self.cache = {}
    
    def save_cache(self):
        """Save cache to file"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
            print(f"[ExpectedLossCache] Saved {len(self.cache)} countries to cache")
        except Exception as e:
            print(f"[ExpectedLossCache] Error saving cache: {e}")
    
    def get(self, country_name: str) -> Optional[Dict]:
        """Get expected loss data for a country from cache"""
        return self.cache.get(country_name)
    
    def set(self, country_name: str, expected_loss_data: Dict):
        """Set expected loss data for a country in cache"""
        self.cache[country_name] = expected_loss_data
        self.save_cache()
    
    def populate_country(self, country_name: str) -> str:
        """Fetch and cache expected loss data for a single country
        
        Args:
            country_name: OECD country name (e.g., "United States")
        
        Returns:
            'success' - Data fetched and cached
            'skipped' - Country not supported by Climate API
            'failed' - API error or timeout
        """
        print(f"[ExpectedLossCache] Fetching data for {country_name}...")
        
        # Convert country name to ISO-3 code
        try:
            country_code = get_country_code(country_name)
            print(f"[ExpectedLossCache] Using ISO-3 code: {country_code}")
        except KeyError:
            print(f"[ExpectedLossCache] No ISO-3 code mapping for {country_name}")
            return 'failed'
        
        # Fetch data using ISO-3 code
        data = self.climate_client.get_country_risk(country_code)
        
        if data and 'error' not in data:
            # Success - cache the data
            self.cache[country_name] = data
            return 'success'
        elif data and data.get('error') == 'unsupported':
            # Country not supported by Climate API - skip
            print(f"[ExpectedLossCache] {country_name} not supported by Climate API")
            return 'skipped'
        else:
            # Actual failure (timeout, network error, API error)
            print(f"[ExpectedLossCache] Failed to fetch data for {country_name}")
            return 'failed'
    
    def populate_all(self, country_list: list) -> Dict:
        """Populate cache for all countries in the list
        
        Returns:
            Dictionary with success/failure counts
        """
        results = {
            'total': len(country_list),
            'success': 0,
            'failed': [],
            'skipped': 0
        }
        
        for i, country_name in enumerate(country_list, 1):
            print(f"[ExpectedLossCache] Processing {i}/{len(country_list)}: {country_name}")
            
            # Skip if already in cache
            if country_name in self.cache:
                print(f"[ExpectedLossCache] Skipping {country_name} (already cached)")
                results['skipped'] += 1
                continue
            
            if self.populate_country(country_name):
                results['success'] += 1
            else:
                results['failed'].append(country_name)
        
        # Save cache after populating all countries
        self.save_cache()
        
        return results
    
    def refresh_all(self, country_list: list) -> Dict:
        """Refresh cache for all countries (force re-fetch)
        
        Returns:
            Dictionary with success/failure counts
        """
        self.cache = {}  # Clear existing cache
        return self.populate_all(country_list)
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        return {
            'cached_countries': len(self.cache),
            'countries': list(self.cache.keys())
        }


# Global cache instance
_cache_instance = None

def get_cache() -> ExpectedLossCache:
    """Get or create global cache instance"""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = ExpectedLossCache()
    return _cache_instance
