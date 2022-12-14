"""Tests for `boxkit/library/create`."""

import boxkit.library as boxkit
import unittest


class TestCreate(unittest.TestCase):
    """boxkit unit test for create"""

    def test_empty_objects(self):
        """test if empty objects can be created"""

        boxkit.Data()
        boxkit.Block()
        boxkit.Dataset()

        print("Empty objects can be created\n")


if __name__ == "__main__":
    unittest.main()
