"""OECD Countries and Sectors data"""

OECD_COUNTRIES = [
  {
    "code": "USA",
    "name": "United States",
    "region": "Americas",
    "oecd_member": True,
    "risk_scores": {
      "climate": 2.8,
      "modern_slavery": 2.1,
      "political": 2.3,
      "water_stress": 2.9,
      "nature_loss": 2.7
    }
  },
  {
    "code": "CHN",
    "name": "China",
    "region": "Asia",
    "oecd_member": False,
    "risk_scores": {
      "climate": 3.5,
      "modern_slavery": 3.8,
      "political": 3.6,
      "water_stress": 3.7,
      "nature_loss": 3.6
    }
  },
  {
    "code": "DEU",
    "name": "Germany",
    "region": "Europe",
    "oecd_member": True,
    "risk_scores": {
      "climate": 2.4,
      "modern_slavery": 1.7,
      "political": 1.8,
      "water_stress": 2.3,
      "nature_loss": 2.2
    }
  },
  {
    "code": "JPN",
    "name": "Japan",
    "region": "Asia",
    "oecd_member": True,
    "risk_scores": {
      "climate": 3.2,
      "modern_slavery": 2.0,
      "political": 1.9,
      "water_stress": 2.8,
      "nature_loss": 2.6
    }
  },
  {
    "code": "IND",
    "name": "India",
    "region": "Asia",
    "oecd_member": False,
    "risk_scores": {
      "climate": 4.1,
      "modern_slavery": 4.2,
      "political": 3.4,
      "water_stress": 4.5,
      "nature_loss": 4.0
    }
  }
]

OECD_SECTORS = [
  {
    "code": "D01T02",
    "name": "Agriculture, forestry and fishing",
    "risk_scores": {
      "climate": 4.2,
      "modern_slavery": 3.8,
      "political": 2.5,
      "water_stress": 4.5,
      "nature_loss": 4.3
    }
  },
  {
    "code": "D26T27",
    "name": "Computer, electronic and optical products",
    "risk_scores": {
      "climate": 2.8,
      "modern_slavery": 3.5,
      "political": 2.3,
      "water_stress": 2.9,
      "nature_loss": 2.7
    }
  },
  {
    "code": "D10T12",
    "name": "Food products, beverages and tobacco",
    "risk_scores": {
      "climate": 3.8,
      "modern_slavery": 3.6,
      "political": 2.4,
      "water_stress": 4.2,
      "nature_loss": 3.9
    }
  }
]
