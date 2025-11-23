"""Populate Expected Loss Cache for All OECD Countries

Run this script to pre-compute expected loss data for all 85 OECD countries.
This enables fast supplier-level expected loss calculations without repeated Climate API calls.

Usage:
    python populate_cache.py [--refresh]
    
Options:
    --refresh: Force refresh all countries (re-fetch even if cached)
"""
import sys
from io_model_factory import IOModelFactory
from expected_loss_cache import get_cache


def main():
    refresh = '--refresh' in sys.argv
    
    print("=" * 60)
    print("Expected Loss Cache Population Script")
    print("=" * 60)
    
    # Get OECD model to get list of countries
    print("\n[1/3] Loading OECD model...")
    io_model = IOModelFactory.get_model('oecd')
    countries = io_model.get_countries()
    country_names = [c.name for c in countries]
    
    print(f"Found {len(country_names)} countries in OECD model")
    
    # Get cache instance
    print("\n[2/3] Initializing cache...")
    cache = get_cache()
    
    if refresh:
        print("Refresh mode: Will re-fetch all countries")
    
    # Populate cache
    print(f"\n[3/3] {'Refreshing' if refresh else 'Populating'} cache...")
    print("This will take approximately 15-20 minutes (85 countries × 12 seconds each)")
    print("Press Ctrl+C to cancel\n")
    
    try:
        if refresh:
            results = cache.refresh_all(country_names)
        else:
            results = cache.populate_all(country_names)
        
        print("\n" + "=" * 60)
        print("Cache Population Complete!")
        print("=" * 60)
        print(f"Total countries: {results['total']}")
        print(f"Successfully cached: {results['success']}")
        print(f"Skipped (already cached): {results['skipped']}")
        print(f"Failed: {len(results['failed'])}")
        
        if results['failed']:
            print("\nFailed countries:")
            for country in results['failed']:
                print(f"  - {country}")
        
        # Show cache stats
        stats = cache.get_cache_stats()
        print(f"\nCache now contains {stats['cached_countries']} countries")
        
    except KeyboardInterrupt:
        print("\n\nCache population cancelled by user")
        print("Partial cache has been saved")
        stats = cache.get_cache_stats()
        print(f"Cache contains {stats['cached_countries']} countries")
        sys.exit(1)


if __name__ == '__main__':
    main()
