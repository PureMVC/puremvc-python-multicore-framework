# Proxy_test.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

import unittest

from puremvc.patterns.proxy import Proxy


class ProxyTest(unittest.TestCase):
    """Test the PureMVC Proxy class."""

    def test_name_accessor(self):
        """Tests getting the name using Proxy class accessor method. Setting can only be done in constructor."""
        # Create a new Proxy and use accessors to set the proxy name
        proxy = Proxy("TestProxy")

        # test assertions
        self.assertEqual(True, proxy.proxy_name == "TestProxy", "Expecting proxy.proxy_name == 'TestProxy'")

    def test_data_accessor(self):
        """Tests setting and getting the data using Proxy class accessor methods."""
        # Create a new Proxy and use accessors to set the data
        proxy = Proxy("colors")
        proxy.data = ["red", "green", "blue"]
        data = proxy.data

        # test assertions
        self.assertEqual(True, len(data) == 3, "Expecting len(data) == 3")
        self.assertEqual(True, data[0] == "red", "Expecting data[0] == 'red'")
        self.assertEqual(True, data[1] == "green", "Expecting data[1] == 'green'")
        self.assertEqual(True, data[2] == "blue", "Expecting data[2] == 'blue'")

    def test_constructor(self):
        """Tests setting the name and body using the Notification class Constructor."""
        # Create a new Proxy using the Constructor to set the name and data
        proxy = Proxy("colors", ["red", "green", "blue"])
        data = proxy.data

        # test assertions
        self.assertIsNotNone(proxy, "Expecting proxy not None")
        self.assertEqual(True, len(data) == 3, "Expecting len(data) == 3")
        self.assertEqual(True, data[0] == "red", "Expecting data[0] == 'red'")
        self.assertEqual(True, data[1] == "green", "Expecting data[1] == 'green'")
        self.assertEqual(True, data[2] == "blue", "Expecting data[2] == 'blue'")


if __name__ == '__main__':
    unittest.main()
