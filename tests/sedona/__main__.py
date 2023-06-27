"""Run the test suite."""

import os
import io
import sys
import contextlib
import unittest
from datetime import date


def main():
    tests = ["boiling", "heater", "application", "astrophysics"]

    suite = unittest.TestSuite()

    for test in tests:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(test))

    with io.StringIO() as buf:
        with contextlib.redirect_stdout(buf):
            res = unittest.TextTestRunner(stream=buf).run(suite).wasSuccessful()

        print(buf.getvalue())

        with open(
            f"{os.path.dirname(__file__)}/archive/{str(date.today())}.log", "w"
        ) as bufOut:
            print(buf.getvalue(), file=bufOut)

    rc = 0 if res else 1
    sys.exit(rc)


if __name__ == "__main__":
    main()
