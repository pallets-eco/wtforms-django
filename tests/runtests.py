#!/usr/bin/env python
import os
import sys
from unittest import defaultTestLoader, TextTestRunner, TestSuite

try:
    from importlib import import_module
except ImportError:

    def import_module(path):
        x = path.rsplit(".", 1)
        basemod = __import__(x[0], None, None, [x[-1]], 0)
        if len(x) > 1:
            try:
                return getattr(basemod, x[1])
            except AttributeError:
                raise ImportError(
                    "module '%s' does not have component '%s'" % (x[0], x[1])
                )
        else:
            return basemod


TESTS = ("test_basic", "test_timezone")


def make_suite(prefix="tests.", extra=(), force_all=False):
    tests = TESTS + extra
    test_names = list(prefix + x for x in tests)
    suite = TestSuite()
    for name in test_names:
        module = import_module(name)
        suite.addTest(defaultTestLoader.loadTestsFromModule(module))
    return suite


def additional_tests():
    """
    This is called automatically by setup.py test
    """
    return make_suite("tests.")


def main():
    my_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.abspath(os.path.join(my_dir, "..")))

    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option(
        "--force-all", action="store_true", dest="force_all", default=False
    )
    parser.add_option("-v", "--verbose", action="count", dest="verbosity", default=0)
    parser.add_option("-q", "--quiet", action="count", dest="quietness", default=0)
    options, extra_args = parser.parse_args()

    suite = make_suite("tests.", tuple(extra_args), options.force_all)
    runner = TextTestRunner(verbosity=options.verbosity - options.quietness + 1)
    result = runner.run(suite)
    sys.exit(not result.wasSuccessful())


if __name__ == "__main__":
    main()
