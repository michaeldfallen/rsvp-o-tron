#! /usr/bin/env python
import unittest
from colour_runner.runner import ColourTextTestRunner

loader = unittest.TestLoader()
tests = loader.discover('.', pattern="test_*.py")
runner = ColourTextTestRunner()
runner.run(tests)
