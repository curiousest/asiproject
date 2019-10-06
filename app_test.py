from set_associative_cache import (
    SetAssociativeCache,
    CacheLine,
    mru_replacement,
    lru_replacement
)

import unittest
import sys
from functools import partial

class MRUTestCase(unittest.TestCase):
    def setUp(self):
        # arbitrary number chosen for test
        self.cache_line_length = 3
        self.cache_line = CacheLine(self.cache_line_length, mru_replacement)

    def test_cache_line_fills_up(self):
        for i in range(self.cache_line_length):
            self.cache_line.write(i, i)
        
        for i in range(self.cache_line_length):
            self.cache_line.read(i)

    def test_most_recent_overwritten(self):
        for i in range(self.cache_line_length):
            self.cache_line.write(i, i)
        
        self.cache_line.read(self.cache_line_length - 1)
        self.cache_line.write(self.cache_line_length, 0)
        
        try:
            self.cache_line.read(self.cache_line_length - 1)
        except ValueError:
            pass
        else:
            raise AssertionError()

class LRUTestCase(unittest.TestCase):
    def setUp(self):
        # arbitrary number chosen for test
        self.cache_line_length = 3
        self.cache_line = CacheLine(self.cache_line_length, lru_replacement)

    def test_cache_line_fills_up(self):
        for i in range(self.cache_line_length):
            self.cache_line.write(i, i)
        
        for i in range(self.cache_line_length):
            self.cache_line.read(i)

    def test_least_recent_overwritten(self):
        for i in range(self.cache_line_length):
            self.cache_line.write(i, i)

        for i in range(self.cache_line_length):
            self.cache_line.read(i)
        
        self.cache_line.write(self.cache_line_length, 0)
        
        try:
            self.cache_line.read(0)
        except ValueError:
            pass
        else:
            raise AssertionError()

class CacheLineTestCase(unittest.TestCase):

    def setUp(self):
        # arbitrary number chosen for test
        self.cache_line_length = 3
        self.cache_line = CacheLine(self.cache_line_length, lru_replacement)

    def test_single_write_read(self):
        self.cache_line.write(1, 2)
        self.assertEqual(self.cache_line.read(1), 2)

    def test_multiple_writes_reads(self):
        for i in range(self.cache_line_length):
            self.cache_line.write(i, i+1)
        
        for i in range(self.cache_line_length):
            self.assertEqual(self.cache_line.read(i), i+1)

    def test_read_key_not_found(self):
        try:
            self.cache_line.read(1)
        except ValueError:
            pass
        else:
            raise AssertionError()

    def test_lru_writes_overwritten(self):
        for i in range(self.cache_line_length * 2):
            self.cache_line.write(i, i+1)
        
        for i in range(self.cache_line_length):
            try:
                self.cache_line.read(i)
            except ValueError:
                pass
            else:
                raise AssertionError()
        
    def test_memory_ballooning_on_write(self):
        for i in range(10):
            self.cache_line.write(i, i)
        
        base_case = sys.getsizeof(self.cache_line)

        for i in range(10000):
            self.cache_line.write(i, i)

        heavy_write_case = sys.getsizeof(self.cache_line)

        # there shouldn't be much more memory allocated between 10->10k writes
        self.assertGreater(base_case * 1.1, heavy_write_case)

    def test_memory_ballooning_on_read(self):
        for i in range(self.cache_line_length):
            self.cache_line.write(i, i)
        
        for i in range(3):
            for j in range(self.cache_line_length):
                self.cache_line.read(j)

        base_case = sys.getsizeof(self.cache_line)

        for i in range(3000):
            for j in range(self.cache_line_length):
                self.cache_line.read(j)

        heavy_read_case = sys.getsizeof(self.cache_line)

        # there shouldn't be much more memory allocated between 9->9k writes
        self.assertGreater(base_case * 1.1, heavy_read_case)

class SetAssociativeCacheTestCase(unittest.TestCase):

    def datastore_read(self, key):
        self.read_call_list.append(key)
        return key

    def setUp(self):
        # arbitrary number chosen for test
        self.cache_line_length = 3
        self.cache_line_count = 3
        self.read_call_list = []
        
        self.cache = SetAssociativeCache(
            self.cache_line_length,
            self.cache_line_count,
            int,
            int,
            self.datastore_read,
            lru_replacement
        )

    def test_types_validated(self):
        try:
            self.cache.read('asdf')
        except TypeError:
            pass
        else:
            raise AssertionError()

    def test_datastore_hit_on_cache_miss(self):
        self.cache.read(1)
        self.assertEqual(len(self.read_call_list), 1)

    def test_datastore_not_used_on_cache_hit(self):
        self.cache.read(1)
        self.cache.read(1)
        self.assertEqual(len(self.read_call_list), 1)


if __name__ == '__main__':
    unittest.main()
