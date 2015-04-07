#! /usr/bin/env python
import unittest


loader = unittest.TestLoader()
tests = loader.discover('.', pattern="test_*.py")
runner = unittest.runner.TextTestRunner()
runner.run(tests)
