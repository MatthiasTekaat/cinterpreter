import unittest
from unittests import TestSuite1
from unittestcompare import TestAddition
from badunittests2 import TestCrucial


def create_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(TestSuite1())
    suite.addTest(TestAddition())
    suite.addTest(TestCrucial())
    return suite

if __name__ == '__main__':
    all_tests=create_test_suite()
    unittest.main()