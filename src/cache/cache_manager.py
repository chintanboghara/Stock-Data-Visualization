"""
Cache management utilities for improving performance by caching API responses.
"""
import os
import time
import logging
import hashlib
import pickle
from functools import wraps
from pathlib import Path
import pandas as pd
from typing import Dict, Any, Callable, TypeVar, Optional

# Type variable for generic function return type
T = TypeVar('T')

# Cache directory configuration
CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

# Cache expiry in seconds (default: 1 hour)
CACHE_EXPIRY = 3600

# Logger
logger = logging.getLogger(__name__)

# In-memory cache
_memory_cache: Dict[str, Dict[str, Any]] = {}

def get_cache_key(func_name: str, *args: Any, **kwargs: Any) -> str:
    """
    Generate a cache key based on function name and arguments.
    
    Args:
        func_name: Name of the function being cached
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
        str: A hash string to use as cache key
    """
    # Create a string representation of the function call
    key_parts = [func_name]
    
    # Add positional arguments
    for arg in args:
        key_parts.append(str(arg))
    
    # Add keyword arguments (sorted to ensure consistency)
    for k in sorted(kwargs.keys()):
        key_parts.append(f"{k}={kwargs[k]}")
    
    # Join all parts and create a hash
    key_str = "_".join(key_parts)
    return hashlib.md5(key_str.encode()).hexdigest()

def cache_result(expires: int = CACHE_EXPIRY) -> Callable:
    """
    Decorator to cache function results.
    
    Args:
        expires: Time in seconds before cache expires
        
    Returns:
        Callable: Decorated function
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            # Generate cache key
            cache_key = get_cache_key(func.__name__, *args, **kwargs)
            
            # Check memory cache first
            if cache_key in _memory_cache:
                cache_entry = _memory_cache[cache_key]
                # Check if the cache entry is still valid
                if time.time() - cache_entry['timestamp'] < expires:
                    logger.debug(f"Cache hit for {func.__name__} ({cache_key})")
                    return cache_entry['result']
            
            # Check file cache
            cache_file = CACHE_DIR / f"{cache_key}.pkl"
            if cache_file.exists():
                try:
                    with open(cache_file, 'rb') as f:
                        cache_entry = pickle.load(f)
                    
                    # Check if the cache entry is still valid
                    if time.time() - cache_entry['timestamp'] < expires:
                        # Restore in memory cache
                        _memory_cache[cache_key] = cache_entry
                        logger.debug(f"File cache hit for {func.__name__} ({cache_key})")
                        return cache_entry['result']
                except Exception as e:
                    logger.warning(f"Failed to load cache for {func.__name__}: {str(e)}")
            
            # Cache miss - call the function
            logger.debug(f"Cache miss for {func.__name__} ({cache_key})")
            result = func(*args, **kwargs)
            
            # Cache the result
            cache_entry = {
                'result': result,
                'timestamp': time.time()
            }
            
            # Update memory cache
            _memory_cache[cache_key] = cache_entry
            
            # Update file cache
            try:
                with open(cache_file, 'wb') as f:
                    # Special handling for pandas DataFrames to avoid pickle issues
                    if isinstance(result, pd.DataFrame):
                        # Store as dict to preserve column types
                        temp_entry = cache_entry.copy()
                        temp_entry['result'] = result.to_dict()
                        temp_entry['type'] = 'dataframe'
                        pickle.dump(temp_entry, f)
                    else:
                        pickle.dump(cache_entry, f)
            except Exception as e:
                logger.warning(f"Failed to write cache for {func.__name__}: {str(e)}")
            
            return result
        
        return wrapper
    
    return decorator

def clear_cache() -> None:
    """Clear all cached data."""
    # Clear memory cache
    _memory_cache.clear()
    
    # Clear file cache
    for cache_file in CACHE_DIR.glob("*.pkl"):
        try:
            os.remove(cache_file)
        except Exception as e:
            logger.warning(f"Failed to remove cache file {cache_file}: {str(e)}")
    
    logger.info("Cache cleared successfully")

def clear_expired_cache(expires: int = CACHE_EXPIRY) -> None:
    """
    Clear only expired cache entries.
    
    Args:
        expires: Time in seconds before cache expires
    """
    current_time = time.time()
    
    # Clear expired entries from memory cache
    keys_to_remove = []
    for key, entry in _memory_cache.items():
        if current_time - entry['timestamp'] >= expires:
            keys_to_remove.append(key)
    
    for key in keys_to_remove:
        _memory_cache.pop(key, None)
    
    # Clear expired entries from file cache
    for cache_file in CACHE_DIR.glob("*.pkl"):
        try:
            # Check if the file is old enough to be expired
            file_timestamp = os.path.getmtime(cache_file)
            if current_time - file_timestamp >= expires:
                os.remove(cache_file)
        except Exception as e:
            logger.warning(f"Failed to process cache file {cache_file}: {str(e)}")
    
    logger.info(f"Cleared {len(keys_to_remove)} expired cache entries")