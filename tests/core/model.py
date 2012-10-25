# -*- coding: utf-8 -*-

from puremvc import MultitonError
from puremvc.core import Model
from puremvc.interfaces import IModel
from puremvc.patterns.proxy import Proxy
from utils.model import ModelTestProxy
import unittest
import uuid


class ModelTest(unittest.TestCase):
    """ModelTest: Test Model Singleton"""

    KEY1 = uuid.uuid4()
    KEY2 = uuid.uuid4()

    def testErrorSameKey(self):
        """ModelTest: raise error if create controller with same key"""
        model = Model(self.KEY1)

        self.assertRaises(MultitonError, Model, self.KEY1)

    def testGetInstance(self):
        """ModelTest: Test get model instance"""
        model1 = Model.getInstance(self.KEY1)
        model2 = Model.getInstance(self.KEY2)

        self.assertNotEqual(None, model1)
        self.assertNotEqual(None, model2)
        self.assertNotEqual(model1, model2)

    def testIsIModel(self):
        """ModelTest: Test instance implements IModel"""
        model = Model.getInstance(self.KEY1)

        self.assertEqual(True, isinstance(model, IModel))

    def testRegisterAndRetrieveProxy(self):
        """ModelTest: Test registerProxy() and retrieveProxy()"""
        model = Model.getInstance(self.KEY1)
        model.registerProxy(Proxy('colors', ['red', 'green', 'blue']))

        testProxy = model.retrieveProxy('colors')
        data = testProxy.getData()

        self.assertNotEqual(None, data)
        self.assertEqual(True, isinstance(data, list))
        self.assertEqual(True, len(data) == 3)
        self.assertEqual(True, data[0] == 'red')
        self.assertEqual(True, data[1] == 'green')
        self.assertEqual(True, data[2] == 'blue')

    def testRegisterAndRemoveProxy(self):
        """ModelTest: Test registerProxy() and removeProxy()"""
        model = Model.getInstance(self.KEY1)
        testProxy = Proxy('sizes', ['7', '13', '21'])
        model.registerProxy(testProxy)

        removedProxy = model.removeProxy('sizes')

        self.assertEqual(True, removedProxy.getProxyName() == 'sizes')

        testProxy = model.retrieveProxy('sizes')

        self.assertEqual(None, testProxy)

    def testHasProxy(self):
        """ModelTest: Test hasProxy()"""
        # Create proxies
        model1 = Model.getInstance(self.KEY1)
        model2 = Model.getInstance(self.KEY2)

        proxy1 = Proxy("aces", ["clubs", "spades", "hearts", "diamonds"])
        proxy2 = Proxy("directions", ["north", "south", "east", "west"])

        # Register proxies
        model1.registerProxy(proxy1)
        model2.registerProxy(proxy2)

        self.assertEqual(True, model1.hasProxy('aces'))
        self.assertEqual(False, model2.hasProxy('aces'))

        self.assertEqual(True, model2.hasProxy('directions'))
        self.assertEqual(False, model1.hasProxy('directions'))

        # Remove proxies
        model1.removeProxy('aces')
        model2.removeProxy('directions')

        self.assertEqual(False, model1.hasProxy('aces'))
        self.assertEqual(False, model2.hasProxy('directions'))

    def testOnRegisterAndOnRemove(self):
        """ModelTest: Test onRegister() and onRemove()"""

        model = Model.getInstance(self.KEY1)

        testProxy = ModelTestProxy()
        model.registerProxy(testProxy)

        self.assertEqual(
            True, testProxy.getData() == ModelTestProxy.ON_REGISTER_CALLED)

        model.removeProxy(ModelTestProxy.NAME)

        self.assertEqual(
            True, testProxy.getData() == ModelTestProxy.ON_REMOVE_CALLED)
