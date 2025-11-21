#!/usr/bin/env python3
"""
Test script for I-O model architecture.

Tests the unified model interface with both OECD ICIO and EXIOBASE models.
"""

from io_model_factory import IOModelFactory, create_io_model


def test_model_factory():
    """Test the model factory"""
    print("="*60)
    print("Testing I-O Model Factory")
    print("="*60)
    
    # Test getting available models
    print("\n1. Available Models:")
    models = IOModelFactory.get_available_models()
    for model in models:
        print(f"\n  {model['id'].upper()}: {model['name']}")
        print(f"    Description: {model['description']}")
        print(f"    Status: {model.get('status', 'Available')}")
        print(f"    Strengths:")
        for strength in model['strengths']:
            print(f"      - {strength}")
    
    # Test model recommendation
    print("\n2. Model Recommendations:")
    print(f"  For environmental analysis: {IOModelFactory.recommend_model(needs_environmental_data=True)}")
    print(f"  For sector detail: {IOModelFactory.recommend_model(needs_sector_detail=True)}")
    print(f"  For country CHN: {IOModelFactory.recommend_model(country='CHN')}")
    print(f"  Default: {IOModelFactory.recommend_model()}")


def test_oecd_model():
    """Test OECD ICIO model"""
    print("\n" + "="*60)
    print("Testing OECD ICIO Model")
    print("="*60)
    
    # Create model
    print("\n1. Creating OECD ICIO model...")
    model = create_io_model('oecd')
    print(f"  Model: {model}")
    print(f"  Version: {model.version}")
    print(f"  Description: {model.description}")
    
    # Test countries
    print("\n2. Countries:")
    countries = model.get_countries()
    print(f"  Total countries: {len(countries)}")
    print(f"  First 10: {[c.code for c in countries[:10]]}")
    print(f"  Last 10: {[c.code for c in countries[-10:]]}")
    
    # Test sectors
    print("\n3. Sectors:")
    sectors = model.get_sectors()
    print(f"  Total sectors: {len(sectors)}")
    print(f"  First 10: {[s.code for s in sectors[:10]]}")
    
    # Test specific country/sector lookup
    print("\n4. Specific Lookups:")
    usa = model.get_country('USA')
    if usa:
        print(f"  USA: {usa.name}")
    
    chn = model.get_country('CHN')
    if chn:
        print(f"  CHN: {chn.name}")
    
    sector = model.get_sector('C10T12')
    if sector:
        print(f"  C10T12: {sector.name}")
    
    # Test validation
    print("\n5. Validation:")
    is_valid, error = model.validate_country_sector('USA', 'C10T12')
    print(f"  USA + C10T12: Valid={is_valid}, Error={error}")
    
    is_valid, error = model.validate_country_sector('XXX', 'C10T12')
    print(f"  XXX + C10T12: Valid={is_valid}, Error={error}")
    
    # Test model info
    print("\n6. Model Info:")
    info = model.get_model_info()
    print(f"  Name: {info['name']}")
    print(f"  Countries: {info['country_count']}")
    print(f"  Sectors: {info['sector_count']}")
    print(f"  Has environmental data: {info['has_environmental_data']}")
    
    # Test statistics
    print("\n7. Model Statistics:")
    try:
        stats = model.get_statistics()
        for key, value in stats.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"  Statistics not available: {e}")
    
    # Test coefficient lookup
    print("\n8. Coefficient Lookup:")
    print("  Testing USA_C10T12 → CHN_C10T12...")
    try:
        coef = model.get_coefficient('USA', 'C10T12', 'CHN', 'C10T12')
        print(f"  Coefficient: {coef:.6f}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Test suppliers
    print("\n9. Top Suppliers:")
    print("  Getting top 5 suppliers for USA_C10T12...")
    try:
        suppliers = model.get_suppliers('USA', 'C10T12', top_n=5)
        for i, supplier in enumerate(suppliers, 1):
            print(f"  {i}. {supplier.country} ({supplier.country_name}) - "
                  f"{supplier.sector} ({supplier.sector_name}): {supplier.coefficient:.6f}")
    except Exception as e:
        print(f"  Error: {e}")


def test_exiobase_model():
    """Test EXIOBASE model"""
    print("\n" + "="*60)
    print("Testing EXIOBASE Model")
    print("="*60)
    
    # Create model
    print("\n1. Creating EXIOBASE model...")
    model = create_io_model('exiobase')
    print(f"  Model: {model}")
    print(f"  Version: {model.version}")
    print(f"  Description: {model.description}")
    
    # Test countries
    print("\n2. Countries:")
    countries = model.get_countries()
    print(f"  Total countries: {len(countries)}")
    print(f"  First 10: {[c.code for c in countries[:10]]}")
    
    # Test sectors
    print("\n3. Sectors:")
    sectors = model.get_sectors()
    print(f"  Total sectors: {len(sectors)}")
    print(f"  All sectors: {[s.code for s in sectors]}")
    
    # Test environmental data
    print("\n4. Environmental Data:")
    print(f"  Has environmental data: {model.has_environmental_data()}")
    if model.has_environmental_data():
        indicators = model.get_environmental_indicators()
        print(f"  Available indicators ({len(indicators)}):")
        for indicator in indicators:
            print(f"    - {indicator}")
    
    # Test statistics
    print("\n5. Model Statistics:")
    stats = model.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")


def test_model_comparison():
    """Compare OECD and EXIOBASE models"""
    print("\n" + "="*60)
    print("Model Comparison")
    print("="*60)
    
    oecd = create_io_model('oecd')
    exiobase = create_io_model('exiobase')
    
    print(f"\n{'Feature':<30} {'OECD ICIO':<20} {'EXIOBASE':<20}")
    print("-" * 70)
    print(f"{'Countries':<30} {len(oecd.get_countries()):<20} {len(exiobase.get_countries()):<20}")
    print(f"{'Sectors':<30} {len(oecd.get_sectors()):<20} {len(exiobase.get_sectors()):<20}")
    print(f"{'Environmental Data':<30} {str(oecd.has_environmental_data()):<20} {str(exiobase.has_environmental_data()):<20}")
    print(f"{'Version':<30} {oecd.version:<20} {exiobase.version:<20}")
    
    # Check common countries
    oecd_countries = set(c.code for c in oecd.get_countries())
    exio_countries = set(c.code for c in exiobase.get_countries())
    common = oecd_countries & exio_countries
    oecd_only = oecd_countries - exio_countries
    exio_only = exio_countries - oecd_countries
    
    print(f"\n{'Country Coverage':<30}")
    print(f"  Common countries: {len(common)}")
    print(f"  OECD only: {len(oecd_only)}")
    print(f"  EXIOBASE only: {len(exio_only)}")
    
    if oecd_only:
        print(f"  OECD exclusive (first 10): {sorted(list(oecd_only))[:10]}")
    if exio_only:
        print(f"  EXIOBASE exclusive (first 10): {sorted(list(exio_only))[:10]}")


def main():
    """Run all tests"""
    try:
        test_model_factory()
        test_oecd_model()
        test_exiobase_model()
        test_model_comparison()
        
        print("\n" + "="*60)
        print("✅ All tests completed!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
