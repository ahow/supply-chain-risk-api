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
                timeout=10  # Reduced timeout to fit within Heroku 30s limit
            )
            
            if response.status_code == 200:
                data = response.json()
                self.cache[country_name] = data
                return data
            else:
                return {"error": f"API returned status {response.status_code}"}
        
        except requests.exceptions.Timeout:
            print(f"Climate API timeout for {country_name}")
            return None  # Return None instead of error dict
        except Exception as e:
            print(f"Climate API error for {country_name}: {str(e)}")
            return None
