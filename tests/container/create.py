"""Tests for `bubblebox/library/create`."""

import bubblebox.library as library
import unittest

class TestCreate(unittest.TestCase):
    """bubblebox unit test for create"""

    def test_empty_objects(self):
        """test if empty objects can be created """

        library.create.Data()
        library.create.Block()
        library.create.Region()
        library.create.Slice()
        library.create.Dataset()

        print("Empty objects can be created\n")
   
if __name__ == '__main__':
    unittest.main()

