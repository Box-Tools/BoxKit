"""Tests for `bubblebox/library/create`."""

import bubblebox.library as bubblebox
import unittest

class TestCreate(unittest.TestCase):
    """bubblebox unit test for create"""

    def test_empty_objects(self):
        """test if empty objects can be created """

        bubblebox.Data()
        bubblebox.Block()
        bubblebox.Region()
        bubblebox.Slice()
        bubblebox.Dataset()

        print("Empty objects can be created\n")
   
if __name__ == '__main__':
    unittest.main()

