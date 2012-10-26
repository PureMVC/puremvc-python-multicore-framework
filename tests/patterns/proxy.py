# -*- coding: utf-8 -*-

from puremvc.patterns.proxy import Proxy
import unittest


class ProxyTest(unittest.TestCase):
    """ProxyTest: Test Proxy Pattern"""

    def testNameAccessor(self):
        """ProxyTest: Test Name Accessor"""

        prxy = Proxy('TestProxy')
        self.assertEqual(True, prxy.getProxyName() == 'TestProxy')

    def testDataAccessors(self):
        """ProxyTest: Test Data Accessors"""

        prxy = Proxy('colors')
        prxy.setData(['red', 'green', 'blue'])
        data = prxy.getData()

        self.assertEqual(True, len(data) == 3)
        self.assertEqual(True, data[0] == 'red')
        self.assertEqual(True, data[1] == 'green')
        self.assertEqual(True, data[2] == 'blue')

    def testConstructor(self):
        """ProxyTest: Test Constructor"""

        prxy = Proxy('colors', ['red', 'green', 'blue'])
        data = prxy.getData()

        self.assertEqual(True, prxy is not None)
        self.assertEqual(True, prxy.getProxyName() == 'colors')
        self.assertEqual(True, len(data) == 3)
        self.assertEqual(True, data[0] == 'red')
        self.assertEqual(True, data[1] == 'green')
        self.assertEqual(True, data[2] == 'blue')

    def testHasMultitonKey(self):
        """ProxyTest: has multiton key"""
        prxy = Proxy("multitonKey")

        self.assertTrue(hasattr(prxy, "multitonKey"))

    def testEmptyData(self):
        """ProxyTest: Test Constructor with not-null empty data"""

        values = ["", (), []]

        for value in values:
            proxy = Proxy("empty", value)

            self.assertEqual(proxy.data, value)
