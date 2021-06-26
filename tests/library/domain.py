"""Tests for `bubblebox/library/domain`."""

import bubblebox.library as library
import unittest

class TestDomain(unittest.TestCase):
    """bubblebox unit test for domain"""

    def test_empty_objects(self):
        """test if empty domain objects can be created """

        library.domain.Data()
        library.domain.Block()
        library.domain.Region()
        library.domain.Slice()

        print("Empty domain objects can be created\n")
   
if __name__ == '__main__':
    unittest.main()

