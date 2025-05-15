# Model_test.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

import unittest
from typing import List

from puremvc.core import Model
from puremvc.interfaces import IModel
from puremvc.patterns.proxy import Proxy


class ModelTest(unittest.TestCase):
    """Test the PureMVC Model class."""

    def test_get_instance(self):
        """Tests the Model Multiton Factory Method"""
        # Test Factory Method
        model = Model.get_instance("ModelTestKey1", lambda k: Model(k))

        # test assertions
        self.assertIsNotNone(model, "Expecting instance not None")
        self.assertIsInstance(model, IModel, "Expecting instance implements IModel")
        self.assertEqual(model, Model.get_instance("ModelTestKey1", lambda k: Model(k)))
        self.assertNotEqual(model, Model.get_instance("Key123", lambda k: Model(k)))

    def test_register_and_retrieve_proxy(self):
        """
        Tests the proxy registration and retrieval methods.
        Tests `register_proxy` and `retrieve_proxy` in the same test.
        These methods cannot currently be tested separately
        in any meaningful way other than to show that the
        methods do not throw exception when called.

        :return:
        """
        # register a proxy and retrieve it.
        model = Model.get_instance("ModelTestKey2", lambda k: Model(k))
        model.register_proxy(Proxy("colors", ["red", "green", "blue"]))
        proxy = model.retrieve_proxy("colors")
        data: List[str] = proxy.data

        # test assertions
        self.assertIsNotNone(data, "Expecting data not None")
        self.assertTrue(isinstance(data, List), "")
        self.assertTrue(len(data) == 3, "Expecting len(data) == 3")
        self.assertTrue(data[0] == "red", "Expecting data[0] == 'red'")
        self.assertTrue(data[1] == "green", "Expecting data[1] == 'green'")
        self.assertTrue(data[2] == "blue", "Expecting data[2] == 'blue'")

    def test_register_and_remove_proxy(self):
        """Tests the proxy removal method."""
        # register a proxy, remove it, then try to retrieve it
        model = Model.get_instance("ModelTestKey3", lambda k: Model(k))
        proxy = Proxy("sizes", ["7", "13", "21"])
        model.register_proxy(proxy)

        # remove the proxy
        removed_proxy = model.remove_proxy("sizes")

        # assert that we removed the appropriate proxy
        self.assertTrue(removed_proxy.proxy_name == "sizes", "Expecting removed_proxy.proxy_name == 'sizes'")

        # ensure that the proxy is no longer retrievable from the model
        proxy = model.retrieve_proxy("colors")

        # test assertions
        self.assertIsNone(proxy, "Expecting proxy is None")

    def test_has_proxy(self):
        """Tests the hasProxy Method"""
        # register a proxy
        model = Model.get_instance("ModelTestKey4", lambda k: Model(k))
        proxy = Proxy("aces", ["clubs", "spades", "hearts", "diamonds"])
        model.register_proxy(proxy)

        # assert that the model.hasProxy method returns true
        # for that proxy name
        self.assertTrue(model.has_proxy("aces"), "Expecting model.has_proxy('aces') == true")

        # remove the proxy
        model.remove_proxy("aces")

        # assert that the model.hasProxy method returns false
        # for that proxy name
        self.assertFalse(model.has_proxy("aces"), "Expecting model.has_proxy('aces') == false")

    def test_on_register_and_on_Remove(self):
        """Tests that the Model calls the on_register and on_remove methods"""
        # Get a Multiton View instance
        model = Model.get_instance("ModelTestKey5", lambda k: Model(k))

        # Create and register the test mediator
        proxy = ModelTestProxy()
        model.register_proxy(proxy)

        # assert that on_register was called, and the proxy responded by setting its data accordingly
        self.assertTrue(proxy.data == ModelTestProxy.ON_REGISTER_CALLED,
                        "Expecting proxy.data == ModelTestProxy.ON_REGISTER_CALLED")

        # Remove the component
        model.remove_proxy(ModelTestProxy.NAME)

        # assert that onRemove was called, and the proxy responded by setting its data accordingly
        self.assertTrue(proxy.data == ModelTestProxy.ON_REMOVE_CALLED,
                        "Expecting proxy.data == ModelTestProxy.ON_REMOVE_CALLED")


class ModelTestProxy(Proxy):
    NAME = "ModelTestProxy"
    ON_REGISTER_CALLED = "onRegister Called"
    ON_REMOVE_CALLED = "onRemove Called"

    def __init__(self):
        super().__init__(ModelTestProxy.NAME)

    def on_register(self):
        self.data = ModelTestProxy.ON_REGISTER_CALLED

    def on_remove(self):
        self.data = ModelTestProxy.ON_REMOVE_CALLED


if __name__ == '__main__':
    unittest.main()
