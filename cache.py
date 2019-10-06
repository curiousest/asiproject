from typing import Callable, List

class CacheLine():
    def __init__(self, cache_line_length: int, replacement_algorithm: Callable[[int, List[int], List[int]],int]):
        self.cache_line_length = cache_line_length
        self.unused_indexes = list(range(cache_line_length))
        self.last_unique_indexes_accessed = list(range(cache_line_length))
        self.keys = [None for _ in range(cache_line_length)]
        self.values = [None for _ in range(cache_line_length)]
        self.replacement_algorithm = replacement_algorithm
    
    def read(self, key):
        # if None is to be a valid key, some refactoring would be required
        assert(key is not None, "None is not a valid key for this cache.")

        # This statement will raise a ValueError if key doesn't exist in the cache line
        index = self.keys.index(key)
        self.last_unique_indexes_accessed.remove(index)
        self.last_unique_indexes_accessed.append(index)
        return self.values[index]

    def write(self, key, value) -> None:
        try:
            self.read(key)
        except ValueError:
            pass
        else:
            # Don't put the same value in two places in the cache
            # in current implementation of SetAssociativeCache, this is not possible
            return
        index_to_change = self.replacement_algorithm(
            self.cache_line_length, self.last_unique_indexes_accessed, self.unused_indexes
        )
        self.keys[index_to_change] = key
        # "value" could be serialized with pickle.dumps, should we choose to use a different cache persistence.
        # With the current implementation, the value can be modified outside of the cache, because it's
        # a pointer to an object in memory, and others have access to the same pointer to the object in memory.  
        self.values[index_to_change] = value
        self.last_unique_indexes_accessed.remove(index_to_change)
        self.last_unique_indexes_accessed.append(index_to_change)

def lru_replacement(cache_line_length: int, last_unique_indexes_accessed: List[int], unused_indexes: List[int]) -> int:
    if unused_indexes:
        return unused_indexes.pop()
    return last_unique_indexes_accessed[0]

def mru_replacement(cache_line_length: int, last_unique_indexes_accessed: List[int], unused_indexes: List[int]) -> int:
    if unused_indexes:
        return unused_indexes.pop()
    return last_unique_indexes_accessed[-1]

class SetAssociativeCache():
    def __init__(self, 
                cache_line_length: int, 
                cache_line_count: int, 
                key_type: type, 
                value_type: type,
                datastore_read_function: Callable,
                replacement_algorithm: Callable[[int, List[int], List[int]],int]):
        if cache_line_length <= 0:
            raise ValueError("cache_line_length must be greater than 0")
        if cache_line_count <= 0:
            raise ValueError("cache_line_count must be greater than 0")
        
        self.cache_line_length = cache_line_length
        self.cache_line_count = cache_line_count
        self.key_type = key_type
        self.value_type = value_type
        self.datastore_read_function = datastore_read_function

        self.cache_lines = [CacheLine(cache_line_length, replacement_algorithm) for _ in range(cache_line_length)]

    def __get_cache_line__(self, key) -> int:
        return hash(key) % self.cache_line_length

    def read(self, key):
        if type(key) is not self.key_type:
            raise TypeError('Incorrect type used for key. Expected {}, got {}.'.format(self.key_type, key))
        cache_line = self.cache_lines[self.__get_cache_line__(key)]
        try:
            return cache_line.read(key)
        except ValueError:
            # cache miss
            value = self.datastore_read_function(key)
            cache_line.write(key, value)
            return value
