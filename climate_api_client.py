"""Climate Risk API Client"""
import requests
from typing import Dict, Optional

class ClimateRiskAPIClient:
    """Client for Climate Risk Country Assessment API V4"""
    
    def __init__(self):
        self.base_url = "https://climate-risk-country-v4-fdee3b254d49.herokuapp.com"
        self.cache = {}
    
    def get_country_risk(self, country_name: str) -> Optional[Dict]:
        """Get climate risk assessment for a country"""
        if country_name in self.cache:
            return self.cache[country_name]
        
        try:
            response = requests.post(
                f"{self.base_url}/assess/country",
                json={"country": country_name},
                timeout=15  # Allow enough time for Climate API to respond (~12s typical)
            )
            
            if response.status_code == 200:
                data = response.json()
                self.cache[country_name] = data
                return data
            elif response.status_code == 404:
                # Country not supported by Climate API
                return {"error": "unsupported", "status_code": 404}
            else:
                # Other API errors (500, 503, etc.)
                return {"error": f"API returned status {response.status_code}", "status_code": response.status_code}
        
        except requests.exceptions.Timeout:
            print(f"Climate API timeout for {country_name}")
            return None  # Return None instead of error dict
        except Exception as e:
            print(f"Climate API error for {country_name}: {str(e)}")
            return None
