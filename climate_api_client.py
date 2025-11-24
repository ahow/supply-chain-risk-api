"""Climate Risk API Client"""
import requests
from typing import Dict, Optional

class ClimateRiskAPIClient:
    """Client for Climate Risk Country Assessment API V4.1"""
    
    def __init__(self):
        # Updated to V4.1 with 162 country support and ISO-3 codes
        self.base_url = "https://climate-risk-api-v4-7da6992dc867.herokuapp.com"
        self.cache = {}
    
    def get_country_risk(self, country_identifier: str) -> Optional[Dict]:
        """Get climate risk assessment for a country
        
        Args:
            country_identifier: Country name or ISO-3 code (e.g., "Bangladesh" or "BGD")
        
        Returns:
            Climate risk assessment data or error dict
        """
        if country_identifier in self.cache:
            return self.cache[country_identifier]
        
        try:
            response = requests.post(
                f"{self.base_url}/assess/country",
                json={"country": country_identifier},
                timeout=35  # Increased timeout for V4.1 (11-20s typical, 30s cold start)
            )
            
            if response.status_code == 200:
                data = response.json()
                self.cache[country_identifier] = data
                return data
            elif response.status_code == 404:
                # Country not supported by Climate API (should not happen with V4.1)
                return {"error": "unsupported", "status_code": 404}
            else:
                # Other API errors (500, 503, etc.)
                return {"error": f"API returned status {response.status_code}", "status_code": response.status_code}
        
        except requests.exceptions.Timeout:
            print(f"Climate API timeout for {country_identifier}")
            return {"error": "timeout", "message": "Request exceeded 35 seconds"}
        except Exception as e:
            print(f"Climate API error for {country_identifier}: {str(e)}")
            return {"error": "exception", "message": str(e)}
