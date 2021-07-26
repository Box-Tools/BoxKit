"""Tests for `bubblebox/utilities/decorators`."""

import os
from bubblebox.utilities import serial, parallel
import unittest

class TestDecorators(unittest.TestCase):
    """bubblebox unit test for create"""

    def test_parallel(self):
        """  """

        @parallel(backend='boxlib')
        def target(value,fac1,fac2):
            return value**fac1*fac2

        os.environ['BUBBLEBOX_NTASKS_PARALLEL']='2'

        listvalues = [1,2,3,4]
        listresult = target(listvalues,2,1)    

        del os.environ['BUBBLEBOX_NTASKS_PARALLEL']

        self.assertEqual(listresult,[1,4,9,16])

if __name__ == '__main__':
    unittest.main()

