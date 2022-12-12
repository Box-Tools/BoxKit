"""Run the test suite."""

import sys
import unittest


def main():
    tests = ["mergeblocks"]

    suite = unittest.TestSuite()

    for test in tests:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(test))

    res = unittest.TextTestRunner().run(suite).wasSuccessful()
    rc = 0 if res else 1
    sys.exit(rc)


if __name__ == "__main__":
    main()
