"""
Cache Manager for Supply Chain Risk API

Implements in-memory LRU caching to optimize performance of:
- Risk assessments (multi-tier calculations)
- Coefficient lookups
- Supplier queries

Target: Reduce assessment time from 2-5s to <500ms for cached results
"""

from functools import lru_cache, wraps
from typing import Dict, Any, Tuple, Optional
import hashlib
import json
import time

# Cache statistics
cache_stats = {
    'hits': 0,
    'misses': 0,
    'total_requests': 0,
    'cache_size': 0
}

# In-memory cache for risk assessments
# Key: (country, sector, model) -> Value: assessment result
assessment_cache: Dict[str, Tuple[Any, float]] = {}

# Cache TTL (time-to-live) in seconds
ASSESSMENT_CACHE_TTL = 3600  # 1 hour
MAX_CACHE_SIZE = 1000  # Maximum number of cached assessments


def get_cache_key(country: str, sector: str, model: str) -> str:
    """Generate cache key for assessment"""
    return f"{model}:{country}:{sector}"


def get_assessment_from_cache(country: str, sector: str, model: str) -> Optional[Any]:
    """
    Retrieve assessment from cache if available and not expired
    
    Returns:
        Assessment result if found and valid, None otherwise
    """
    global cache_stats
    
    cache_key = get_cache_key(country, sector, model)
    cache_stats['total_requests'] += 1
    
    if cache_key in assessment_cache:
        result, timestamp = assessment_cache[cache_key]
        
        # Check if cache entry is still valid
        if time.time() - timestamp < ASSESSMENT_CACHE_TTL:
            cache_stats['hits'] += 1
            return result
        else:
            # Remove expired entry
            del assessment_cache[cache_key]
    
    cache_stats['misses'] += 1
    return None


def save_assessment_to_cache(country: str, sector: str, model: str, result: Any):
    """
    Save assessment result to cache
    
    Implements LRU eviction if cache is full
    """
    global cache_stats
    
    cache_key = get_cache_key(country, sector, model)
    
    # If cache is full, remove oldest entry (simple FIFO for now)
    if len(assessment_cache) >= MAX_CACHE_SIZE:
        # Find and remove oldest entry
        oldest_key = min(assessment_cache.keys(), 
                        key=lambda k: assessment_cache[k][1])
        del assessment_cache[oldest_key]
    
    # Save to cache with current timestamp
    assessment_cache[cache_key] = (result, time.time())
    cache_stats['cache_size'] = len(assessment_cache)


def clear_cache():
    """Clear all cached assessments"""
    global cache_stats
    assessment_cache.clear()
    cache_stats['cache_size'] = 0


def get_cache_stats() -> Dict[str, Any]:
    """
    Get cache statistics
    
    Returns:
        Dictionary with cache performance metrics
    """
    total = cache_stats['total_requests']
    hit_rate = (cache_stats['hits'] / total * 100) if total > 0 else 0
    
    return {
        'hits': cache_stats['hits'],
        'misses': cache_stats['misses'],
        'total_requests': total,
        'hit_rate_percent': round(hit_rate, 2),
        'cache_size': cache_stats['cache_size'],
        'max_cache_size': MAX_CACHE_SIZE,
        'ttl_seconds': ASSESSMENT_CACHE_TTL
    }


# Decorator for caching coefficient lookups
def cache_coefficients(maxsize=10000):
    """
    Decorator to cache coefficient lookups
    
    Args:
        maxsize: Maximum number of cached coefficients
    """
    def decorator(func):
        # Use functools.lru_cache for efficient caching
        cached_func = lru_cache(maxsize=maxsize)(func)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            return cached_func(*args, **kwargs)
        
        # Expose cache_info for monitoring
        wrapper.cache_info = cached_func.cache_info
        wrapper.cache_clear = cached_func.cache_clear
        
        return wrapper
    return decorator


# Decorator for caching supplier queries
def cache_suppliers(maxsize=5000):
    """
    Decorator to cache supplier queries
    
    Args:
        maxsize: Maximum number of cached supplier lists
    """
    def decorator(func):
        cached_func = lru_cache(maxsize=maxsize)(func)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Convert top_n to hashable type for caching
            return cached_func(*args, **kwargs)
        
        wrapper.cache_info = cached_func.cache_info
        wrapper.cache_clear = cached_func.cache_clear
        
        return wrapper
    return decorator


def warm_cache(model, common_assessments):
    """
    Pre-populate cache with common assessments
    
    Args:
        model: IOModel instance
        common_assessments: List of (country, sector) tuples to pre-compute
    """
    print(f"Warming cache with {len(common_assessments)} common assessments...")
    
    from risk_calculator import calculate_risk
    
    for country, sector in common_assessments:
        try:
            result = calculate_risk(country, sector, model)
            save_assessment_to_cache(country, sector, model.name.lower(), result)
        except Exception as e:
            print(f"Failed to warm cache for {country} {sector}: {e}")
    
    print(f"Cache warmed. Size: {len(assessment_cache)}")


# Common country-sector pairs for cache warming
COMMON_ASSESSMENTS = [
    ('USA', 'C10T12'),  # USA Food
    ('CHN', 'C10T12'),  # China Food
    ('DEU', 'C10T12'),  # Germany Food
    ('USA', 'C26T27'),  # USA Electronics
    ('CHN', 'C26T27'),  # China Electronics
    ('JPN', 'C26T27'),  # Japan Electronics
    ('USA', 'C29'),     # USA Motor vehicles
    ('DEU', 'C29'),     # Germany Motor vehicles
    ('CHN', 'C29'),     # China Motor vehicles
    ('USA', 'C13T15'),  # USA Textiles
    ('CHN', 'C13T15'),  # China Textiles
    ('IND', 'C13T15'),  # India Textiles
]
