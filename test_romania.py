#!/usr/bin/env python3
from risk_calculator_v2 import MultiTierRiskCalculator
from oecd_icio_model import OECDICIOModel

calc = MultiTierRiskCalculator(OECDICIOModel())
result = calc.assess_risk('ROU', 'B09')

if result and 'error' not in result:
    print("Success! Assessment completed")
    print(f"Country: {result['country']['name']}")
    print(f"Sector: {result['sector']['name']}")
    print(f"Total Climate Risk: {result['total_risk']['climate']:.2f}")
else:
    print(f"Error: {result.get('error', 'Unknown error')}")
