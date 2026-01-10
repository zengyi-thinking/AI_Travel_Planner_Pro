"""
Over-Engineered Cache System Module
====================================

This module provides an over-engineered caching system with multiple eviction policies,
automatic expiration, statistics tracking, and thread-safe operations.

Key Features:
    - Abstract base classes for extensibility
    - Support for multiple eviction policies (LRU, FIFO, LFU)
    - Cache statistics and monitoring
    - Thread-safe operations
    - Comprehensive type annotations
    - Detailed docstrings
"""

from abc import ABC, abstractmethod
from typing import Any, Optional, Dict, List, Tuple, Callable, Union, Generic
from dataclasses import dataclass, field
from enum import Enum
from collections import OrderedDict, defaultdict
import time
import threading
import hashlib


class CacheEvictionPolicy(Enum):
    """Enumeration of available cache eviction policies."""
    LRU = "lru"  # Least Recently Used
    FIFO = "fifo"  # First-In, First-Out
    LFU = "lfu"  # Least Frequently Used
    LIFO = "lifo"  # Last-In, First-Out
    RANDOM = "random"  # Random eviction


class CacheEventType(Enum):
    """Enumeration of cache event types for logging."""
    HIT = "hit"
    MISS = "miss"
    EVICTION = "eviction"
    EXPIRATION = "expiration"
    PUT = "put"
    DELETE = "delete"
    CLEAR = "clear"


@dataclass
class CacheEntry:
    """
    A data class representing a cache entry with metadata.
    
    Attributes:
        key: The cache key
        value: The cached value
        created_at: Timestamp when the entry was created
        last_accessed_at: Timestamp when the entry was last accessed
        access_count: Number of times the entry has been accessed
        ttl: Time-to-live in seconds (None means no expiration)
        size: Estimated size of the entry in bytes
        metadata: Additional custom metadata
    """
    key: str
    value: Any
    created_at: float = field(default_factory=time.time)
    last_accessed_at: float = field(default_factory=time.time)
    access_count: int = 0
    ttl: Optional[float] = None
    size: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_expired(self) -> bool:
        """
        Check if the cache entry has expired.
        
        Returns:
            bool: True if the entry has expired
        """
        if self.ttl is None:
            return False
        return time.time() > self.created_at + self.ttl
    
    def touch(self) -> None:
        """Update the last accessed timestamp and increment access count."""
        self.last_accessed_at = time.time()
        self.access_count += 1
    
    def get_age(self) -> float:
        """
        Get the age of the cache entry in seconds.
        
        Returns:
            float: Age in seconds
        """
        return time.time() - self.created_at
    
    def get_time_since_access(self) -> float:
        """
        Get the time since the cache entry was last accessed.
        
        Returns:
            float: Time since last access in seconds
        """
        return time.time() - self.last_accessed_at
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the cache entry to a dictionary representation.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the entry
        """
        return {
            "key": self.key,
            "value": str(self.value) if not isinstance(self.value, (dict, list)) else self.value,
            "created_at": self.created_at,
            "last_accessed_at": self.last_accessed_at,
            "access_count": self.access_count,
            "ttl": self.ttl,
            "size": self.size,
            "metadata": self.metadata
        }


@dataclass
class CacheEvent:
    """
    A data class representing a cache event for logging and monitoring.
    
    Attributes:
        event_type: The type of cache event
        key: The cache key involved
        timestamp: When the event occurred
        value: The value (if applicable)
        metadata: Additional event metadata
    """
    event_type: CacheEventType
    key: Optional[str]
    timestamp: float = field(default_factory=time.time)
    value: Optional[Any] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the cache event to a dictionary representation.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the event
        """
        return {
            "event_type": self.event_type.value,
            "key": self.key,
            "timestamp": self.timestamp,
            "value": str(self.value) if self.value is not None else None,
            "metadata": self.metadata
        }


class BaseEvictionPolicy(ABC):
    """
    Abstract base class defining the contract for cache eviction policies.
    
    This class implements the Strategy Pattern, allowing different
    eviction policies to be interchangeable.
    
    Attributes:
        policy_type: The type of eviction policy
    """
    
    def __init__(self, policy_type: CacheEvictionPolicy):
        """
        Initialize the eviction policy.
        
        Args:
            policy_type: The type of eviction policy
        """
        self.policy_type = policy_type
    
    @abstractmethod
    def record_access(self, key: str, entry: CacheEntry) -> None:
        """
        Record an access to a cache entry.
        
        Args:
            key: The cache key
            entry: The cache entry
        """
        pass
    
    @abstractmethod
    def record_insertion(self, key: str, entry: CacheEntry) -> None:
        """
        Record the insertion of a cache entry.
        
        Args:
            key: The cache key
            entry: The cache entry
        """
        pass
    
    @abstractmethod
    def get_eviction_key(self, cache: Dict[str, CacheEntry]) -> Optional[str]:
        """
        Get the key of the entry to evict.
        
        Args:
            cache: The current cache state
            
        Returns:
            Optional[str]: The key to evict, or None if no eviction needed
        """
        pass
    
    @abstractmethod
    def remove_key(self, key: str) -> None:
        """
        Remove a key from the eviction policy's tracking.
        
        Args:
            key: The cache key
        """
        pass


class LRUEvictionPolicy(BaseEvictionPolicy):
    """
    Least Recently Used (LRU) eviction policy.
    
    Evicts the cache entry that has not been accessed for the longest time.
    """
    
    def __init__(self):
        """Initialize the LRU eviction policy."""
        super().__init__(CacheEvictionPolicy.LRU)
        self._access_order: OrderedDict = OrderedDict()
        self._lock = threading.RLock()
    
    def record_access(self, key: str, entry: CacheEntry) -> None:
        """
        Record an access to a cache entry (move to end of order).
        
        Args:
            key: The cache key
            entry: The cache entry
        """
        with self._lock:
            if key in self._access_order:
                del self._access_order[key]
            self._access_order[key] = time.time()
    
    def record_insertion(self, key: str, entry: CacheEntry) -> None:
        """
        Record the insertion of a cache entry (add to end of order).
        
        Args:
            key: The cache key
            entry: The cache entry
        """
        with self._lock:
            if key in self._access_order:
                del self._access_order[key]
            self._access_order[key] = time.time()
    
    def get_eviction_key(self, cache: Dict[str, CacheEntry]) -> Optional[str]:
        """
        Get the key of the least recently used entry.
        
        Args:
            cache: The current cache state
            
        Returns:
            Optional[str]: The key to evict
        """
        with self._lock:
            if not self._access_order:
                return None
            # Return the first key (least recently used)
            return next(iter(self._access_order.keys()))
    
    def remove_key(self, key: str) -> None:
        """
        Remove a key from the tracking.
        
        Args:
            key: The cache key
        """
        with self._lock:
            if key in self._access_order:
                del self._access_order[key]


class FIFOEvictionPolicy(BaseEvictionPolicy):
    """
    First-In, First-Out (FIFO) eviction policy.
    
    Evicts the cache entry that has been in the cache the longest.
    """
    
    def __init__(self):
        """Initialize the FIFO eviction policy."""
        super().__init__(CacheEvictionPolicy.FIFO)
        self._insertion_order: List[str] = []
        self._lock = threading.RLock()
    
    def record_access(self, key: str, entry: CacheEntry) -> None:
        """
        Record an access to a cache entry (no effect on FIFO).
        
        Args:
            key: The cache key
            entry: The cache entry
        """
        # FIFO doesn't care about access order
        pass
    
    def record_insertion(self, key: str, entry: CacheEntry) -> None:
        """
        Record the insertion of a cache entry (add to end of order).
        
        Args:
            key: The cache key
            entry: The cache entry
        """
        with self._lock:
            if key not in self._insertion_order:
                self._insertion_order.append(key)
    
    def get_eviction_key(self, cache: Dict[str, CacheEntry]) -> Optional[str]:
        """
        Get the key of the first-in entry.
        
        Args:
            cache: The current cache state
            
        Returns:
            Optional[str]: The key to evict
        """
        with self._lock:
            if not self._insertion_order:
                return None
            return self._insertion_order[0]
    
    def remove_key(self, key: str) -> None:
        """
        Remove a key from the tracking.
        
        Args:
            key: The cache key
        """
        with self._lock:
            if key in self._insertion_order:
                self._insertion_order.remove(key)


class LFUEvictionPolicy(BaseEvictionPolicy):
    """
    Least Frequently Used (LFU) eviction policy.
    
    Evicts the cache entry with the lowest access count.
    """
    
    def __init__(self):
        """Initialize the LFU eviction policy."""
        super().__init__(CacheEvictionPolicy.LFU)
        self._access_counts: Dict[str, int] = defaultdict(int)
        self._lock = threading.RLock()
    
    def record_access(self, key: str, entry: CacheEntry) -> None:
        """
        Record an access to a cache entry (increment access count).
        
        Args:
            key: The cache key
            entry: The cache entry
        """
        with self._lock:
            self._access_counts[key] += 1
    
    def record_insertion(self, key: str, entry: CacheEntry) -> None:
        """
        Record the insertion of a cache entry (initialize access count).
        
        Args:
            key: The cache key
            entry: The cache entry
        """
        with self._lock:
            self._access_counts[key] = 1
    
    def get_eviction_key(self, cache: Dict[str, CacheEntry]) -> Optional[str]:
        """
        Get the key of the least frequently used entry.
        
        Args:
            cache: The current cache state
            
        Returns:
            Optional[str]: The key to evict
        """
        with self._lock:
            if not self._access_counts:
                return None
            # Find the key with the minimum access count
            min_access = min(self._access_counts.values())
            for key, count in self._access_counts.items():
                if count == min_access:
                    return key
            return None
    
    def remove_key(self, key: str) -> None:
        """
        Remove a key from the tracking.
        
        Args:
            key: The cache key
        """
        with self._lock:
            if key in self._access_counts:
                del self._access_counts[key]


@dataclass
class CacheStatistics:
    """
    A data class representing cache statistics.
    
    Attributes:
        hits: Number of cache hits
        misses: Number of cache misses
        evictions: Number of cache evictions
        expirations: Number of cache expirations
        puts: Number of cache puts
        deletes: Number of cache deletes
        clears: Number of cache clears
        total_operations: Total number of cache operations
        hit_rate: Cache hit rate (hits / (hits + misses))
    """
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    expirations: int = 0
    puts: int = 0
    deletes: int = 0
    clears: int = 0
    total_operations: int = 0
    
    @property
    def hit_rate(self) -> float:
        """
        Calculate the cache hit rate.
        
        Returns:
            float: Hit rate between 0.0 and 1.0
        """
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return self.hits / total
    
    def reset(self) -> None:
        """Reset all statistics to zero."""
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.expirations = 0
        self.puts = 0
        self.deletes = 0
        self.clears = 0
        self.total_operations = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert statistics to a dictionary representation.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the statistics
        """
        return {
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
            "expirations": self.expirations,
            "puts": self.puts,
            "deletes": self.deletes,
            "clears": self.clears,
            "total_operations": self.total_operations,
            "hit_rate": self.hit_rate
        }


class OverEngineeredCache:
    """
    An over-engineered caching system with multiple eviction policies,
    automatic expiration, statistics tracking, and thread-safe operations.
    
    Example:
        >>> cache = OverEngineeredCache(max_size=100, ttl=3600)
        >>> cache.put("key1", "value1")
        >>> value = cache.get("key1")
        >>> print(value)
        "value1"
    """
    
    def __init__(
        self,
        max_size: int = 1000,
        ttl: Optional[float] = None,
        eviction_policy: Union[CacheEvictionPolicy, BaseEvictionPolicy, str] = CacheEvictionPolicy.LRU,
        enable_statistics: bool = True,
        enable_event_logging: bool = True,
        auto_cleanup_interval: Optional[float] = None
    ):
        """
        Initialize the over-engineered cache.
        
        Args:
            max_size: Maximum number of entries in the cache
            ttl: Default time-to-live for cache entries in seconds
            eviction_policy: The eviction policy to use
            enable_statistics: Whether to track cache statistics
            enable_event_logging: Whether to log cache events
            auto_cleanup_interval: Interval for automatic cleanup in seconds
        """
        self._cache: Dict[str, CacheEntry] = {}
        self._max_size = max_size
        self._default_ttl = ttl
        self._enable_statistics = enable_statistics
        self._enable_event_logging = enable_event_logging
        
        # Initialize eviction policy
        if isinstance(eviction_policy, str):
            eviction_policy = CacheEvictionPolicy(eviction_policy.lower())
        
        if isinstance(eviction_policy, CacheEvictionPolicy):
            if eviction_policy == CacheEvictionPolicy.LRU:
                self._eviction_policy = LRUEvictionPolicy()
            elif eviction_policy == CacheEvictionPolicy.FIFO:
                self._eviction_policy = FIFOEvictionPolicy()
            elif eviction_policy == CacheEvictionPolicy.LFU:
                self._eviction_policy = LFUEvictionPolicy()
            else:
                raise ValueError(f"Unsupported eviction policy: {eviction_policy}")
        else:
            self._eviction_policy = eviction_policy
        
        self._statistics = CacheStatistics()
        self._event_log: List[CacheEvent] = []
        self._lock = threading.RLock()
        
        # Auto-cleanup thread
        self._cleanup_thread: Optional[threading.Thread] = None
        self._cleanup_stop_event = threading.Event()
        
        if auto_cleanup_interval is not None:
            self._start_cleanup_thread(auto_cleanup_interval)
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.
        
        Args:
            key: The cache key
            
        Returns:
            Optional[Any]: The cached value, or None if not found or expired
        """
        with self._lock:
            if key not in self._cache:
                self._record_event(CacheEventType.MISS, key)
                if self._enable_statistics:
                    self._statistics.misses += 1
                    self._statistics.total_operations += 1
                return None
            
            entry = self._cache[key]
            
            # Check if entry has expired
            if entry.is_expired():
                del self._cache[key]
                self._eviction_policy.remove_key(key)
                self._record_event(CacheEventType.EXPIRATION, key, entry.value)
                if self._enable_statistics:
                    self._statistics.expirations += 1
                    self._statistics.misses += 1
                    self._statistics.total_operations += 1
                return None
            
            # Update access
            entry.touch()
            self._eviction_policy.record_access(key, entry)
            
            self._record_event(CacheEventType.HIT, key, entry.value)
            if self._enable_statistics:
                self._statistics.hits += 1
                self._statistics.total_operations += 1
            
            return entry.value
    
    def put(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """
        Put a value into the cache.
        
        Args:
            key: The cache key
            value: The value to cache
            ttl: Time-to-live in seconds (uses default if None)
        """
        with self._lock:
            # Remove existing entry if present
            if key in self._cache:
                del self._cache[key]
                self._eviction_policy.remove_key(key)
            
            # Evict if necessary
            while len(self._cache) >= self._max_size:
                eviction_key = self._eviction_policy.get_eviction_key(self._cache)
                if eviction_key is None:
                    break
                evicted_entry = self._cache[eviction_key]
                del self._cache[eviction_key]
                self._eviction_policy.remove_key(eviction_key)
                self._record_event(CacheEventType.EVICTION, eviction_key, evicted_entry.value)
                if self._enable_statistics:
                    self._statistics.evictions += 1
            
            # Create new entry
            actual_ttl = ttl if ttl is not None else self._default_ttl
            entry = CacheEntry(
                key=key,
                value=value,
                ttl=actual_ttl,
                size=self._estimate_size(value)
            )
            
            self._cache[key] = entry
            self._eviction_policy.record_insertion(key, entry)
            
            self._record_event(CacheEventType.PUT, key, value)
            if self._enable_statistics:
                self._statistics.puts += 1
                self._statistics.total_operations += 1
    
    def delete(self, key: str) -> bool:
        """
        Delete a value from the cache.
        
        Args:
            key: The cache key
            
        Returns:
            bool: True if the key was found and deleted
        """
        with self._lock:
            if key not in self._cache:
                return False
            
            entry = self._cache[key]
            del self._cache[key]
            self._eviction_policy.remove_key(key)
            
            self._record_event(CacheEventType.DELETE, key, entry.value)
            if self._enable_statistics:
                self._statistics.deletes += 1
                self._statistics.total_operations += 1
            
            return True
    
    def clear(self) -> None:
        """Clear all entries from the cache."""
        with self._lock:
            self._cache.clear()
            # Recreate the eviction policy
            if isinstance(self._eviction_policy, LRUEvictionPolicy):
                self._eviction_policy = LRUEvictionPolicy()
            elif isinstance(self._eviction_policy, FIFOEvictionPolicy):
                self._eviction_policy = FIFOEvictionPolicy()
            elif isinstance(self._eviction_policy, LFUEvictionPolicy):
                self._eviction_policy = LFUEvictionPolicy()
            
            self._record_event(CacheEventType.CLEAR, None)
            if self._enable_statistics:
                self._statistics.clears += 1
                self._statistics.total_operations += 1
    
    def contains(self, key: str) -> bool:
        """
        Check if a key exists in the cache and is not expired.
        
        Args:
            key: The cache key
            
        Returns:
            bool: True if the key exists and is not expired
        """
        with self._lock:
            if key not in self._cache:
                return False
            
            entry = self._cache[key]
            if entry.is_expired():
                del self._cache[key]
                self._eviction_policy.remove_key(key)
                return False
            
            return True
    
    def get_statistics(self) -> CacheStatistics:
        """
        Get the cache statistics.
        
        Returns:
            CacheStatistics: Current cache statistics
        """
        return self._statistics
    
    def reset_statistics(self) -> None:
        """Reset the cache statistics."""
        self._statistics.reset()
    
    def get_event_log(self) -> List[CacheEvent]:
        """
        Get the event log.
        
        Returns:
            List[CacheEvent]: List of cache events
        """
        with self._lock:
            return self._event_log.copy()
    
    def clear_event_log(self) -> None:
        """Clear the event log."""
        with self._lock:
            self._event_log.clear()
    
    def get_size(self) -> int:
        """
        Get the current number of entries in the cache.
        
        Returns:
            int: Number of entries
        """
        with self._lock:
            return len(self._cache)
    
    def get_keys(self) -> List[str]:
        """
        Get all keys in the cache.
        
        Returns:
            List[str]: List of cache keys
        """
        with self._lock:
            return list(self._cache.keys())
    
    def get_entries(self) -> List[CacheEntry]:
        """
        Get all entries in the cache.
        
        Returns:
            List[CacheEntry]: List of cache entries
        """
        with self._lock:
            return list(self._cache.values())
    
    def cleanup_expired(self) -> int:
        """
        Remove all expired entries from the cache.
        
        Returns:
            int: Number of entries removed
        """
        with self._lock:
            expired_keys = [
                key for key, entry in self._cache.items()
                if entry.is_expired()
            ]
            
            for key in expired_keys:
                entry = self._cache[key]
                del self._cache[key]
                self._eviction_policy.remove_key(key)
                self._record_event(CacheEventType.EXPIRATION, key, entry.value)
                if self._enable_statistics:
                    self._statistics.expirations += 1
            
            return len(expired_keys)
    
    def _record_event(self, event_type: CacheEventType, key: Optional[str], value: Optional[Any] = None) -> None:
        """
        Record a cache event.
        
        Args:
            event_type: The type of event
            key: The cache key (if applicable)
            value: The value (if applicable)
        """
        if not self._enable_event_logging:
            return
        
        event = CacheEvent(
            event_type=event_type,
            key=key,
            value=value
        )
        self._event_log.append(event)
    
    def _estimate_size(self, value: Any) -> int:
        """
        Estimate the size of a value in bytes.
        
        Args:
            value: The value to estimate
            
        Returns:
            int: Estimated size in bytes
        """
        return len(str(value).encode("utf-8"))
    
    def _start_cleanup_thread(self, interval: float) -> None:
        """
        Start the automatic cleanup thread.
        
        Args:
            interval: Cleanup interval in seconds
        """
        def cleanup_loop():
            while not self._cleanup_stop_event.is_set():
                self._cleanup_stop_event.wait(interval)
                if not self._cleanup_stop_event.is_set():
                    self.cleanup_expired()
        
        self._cleanup_thread = threading.Thread(target=cleanup_loop, daemon=True)
        self._cleanup_thread.start()
    
    def stop_cleanup_thread(self) -> None:
        """Stop the automatic cleanup thread."""
        if self._cleanup_thread is not None:
            self._cleanup_stop_event.set()
            self._cleanup_thread.join()
            self._cleanup_thread = None
    
    def __len__(self) -> int:
        """Return the current number of entries in the cache."""
        return self.get_size()
    
    def __contains__(self, key: str) -> bool:
        """Check if a key exists in the cache."""
        return self.contains(key)
    
    def __getitem__(self, key: str) -> Any:
        """Get a value from the cache using dictionary syntax."""
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Put a value into the cache using dictionary syntax."""
        self.put(key, value)
    
    def __delitem__(self, key: str) -> None:
        """Delete a value from the cache using dictionary syntax."""
        if not self.delete(key):
            raise KeyError(key)
    
    def __repr__(self) -> str:
        """Return a string representation of the cache."""
        stats = self._statistics
        hit_rate = stats.hit_rate * 100
        return (f"OverEngineeredCache(size={len(self)}, max_size={self._max_size}, "
                f"hit_rate={hit_rate:.1f}%, eviction={self._eviction_policy.policy_type.value})")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop_cleanup_thread()
