# -*- coding: utf-8 -*-

from puremvc import MultitonError
from puremvc.interfaces import IFacade, IProxy
from puremvc.patterns.facade import Facade
from puremvc.patterns.mediator import Mediator
from puremvc.patterns.proxy import Proxy
from utils.facade import (FacadeTestCommand, FacadeTestVO,
    FacadeInstanceTestCommand)
import unittest
import uuid


class FacadeTest(unittest.TestCase):
    """FacadeTest: Test Facade Pattern"""

    KEY1 = uuid.uuid4()
    KEY2 = uuid.uuid4()

    def testErrorSameKey(self):
        """ModelTest: raise error if create controller with same key"""
        facade = Facade(self.KEY1)

        self.assertRaises(MultitonError, Facade, self.KEY1)

    def testNotNone(self):
        """FacadeTest: Test instance not null"""
        facade1 = Facade.getInstance(self.KEY1)
        facade2 = Facade.getInstance(self.KEY2)

        self.assertNotEqual(None, facade1)
        self.assertNotEqual(None, facade2)
        self.assertNotEqual(facade1, facade2)

    def testIsIFacade(self):
        """FacadeTest: Test instance implements IFacade"""
        fcde = Facade.getInstance(self.KEY1)

        self.assertEqual(True, isinstance(fcde, IFacade))

    def testRegisterCommandAndSendNotification(self):
        """FacadeTest: Test registerCommand() and sendNotification()"""

        fcde = Facade.getInstance(self.KEY1)
        fcde.registerCommand('FacadeTestNote', FacadeTestCommand)

        vo = FacadeTestVO(32)
        fcde.sendNotification('FacadeTestNote', vo)

        self.assertEqual(True, vo.result == 64)

    def testRegisterAndRemoveCommandAndSendNotification(self):
        """FacadeTest: Test removeCommand() and subsequent
        sendNotification()
        """
        fcde = Facade.getInstance(self.KEY1)
        fcde.registerCommand('FacadeTestNote', FacadeTestCommand)
        fcde.removeCommand('FacadeTestNote')

        vo = FacadeTestVO(32)
        fcde.sendNotification('FacadeTestNote', vo)

        self.assertEqual(True, vo.result != 64)

    def testRegisterAndRetrieveProxy(self):
        """FacadeTest: Test registerProxy() and retrieveProxy()"""
        fcde = Facade.getInstance(self.KEY1)
        fcde.registerProxy(Proxy('colors', ['red', 'green', 'blue']))
        pxy = fcde.retrieveProxy('colors')

        self.assertEqual(True, isinstance(pxy, IProxy))

        data = pxy.getData()

        self.assertEqual(True, data is not None)
        self.assertEqual(True, isinstance(data, list))
        self.assertEqual(True, len(data) == 3)
        self.assertEqual(True, data[0] == 'red')
        self.assertEqual(True, data[1] == 'green')
        self.assertEqual(True, data[2] == 'blue')

    def testRegisterAndRemoveProxy(self):
        """FacadeTest: Test registerProxy() and removeProxy()"""

        fcde = Facade.getInstance(self.KEY1)
        pxy = Proxy('sizes', ['7', '13', '21'])
        fcde.registerProxy(pxy)

        removedProxy = fcde.removeProxy('sizes')

        self.assertEqual(True, removedProxy.getProxyName() == 'sizes')

        pxy = fcde.retrieveProxy('sizes')

        self.assertEqual(True, pxy == None)

    def testRegisterRetrieveAndRemoveMediator(self):
        """FacadeTest: Test registerMediator() retrieveMediator() and
        removeMediator()
        """

        fcde = Facade.getInstance(self.KEY1)
        fcde.registerMediator(Mediator(Mediator.NAME, object()))

        self.assertEqual(
            True, fcde.retrieveMediator(Mediator.NAME) is not None)

        removedMediator = fcde.removeMediator(Mediator.NAME)

        self.assertEqual(
            True, removedMediator.getMediatorName() == Mediator.NAME)
        self.assertEqual(True, fcde.retrieveMediator(Mediator.NAME) == None)

    def testHasProxy(self):
        """FacadeTest: Test hasProxy()"""
        # Create facades
        facade1 = Facade.getInstance(self.KEY1)
        facade2 = Facade.getInstance(self.KEY2)

        # Register proxies
        proxy1 = Proxy('hasProxy1', [1, 2, 3])
        proxy2 = Proxy('hasProxy2', [10, 20, 30])

        facade1.registerProxy(proxy1)
        facade2.registerProxy(proxy2)

        self.assertEqual(True, facade1.hasProxy('hasProxy1'))
        self.assertEqual(False, facade2.hasProxy('hasProxy1'))

        self.assertEqual(True, facade2.hasProxy('hasProxy2'))
        self.assertEqual(False, facade1.hasProxy('hasProxy2'))

        # Remove proxies
        facade1.removeProxy('hasProxy1')
        facade2.removeProxy('hasProxy2')

        self.assertEqual(False, facade1.hasProxy('hasProxy1'))
        self.assertEqual(False, facade2.hasProxy('hasProxy2'))

    def testHasMediator(self):
        """FacadeTest: Test hasMediator()"""
        # Create facades
        facade1 = Facade.getInstance(self.KEY1)
        facade2 = Facade.getInstance(self.KEY2)

        # Register mediators
        mediator1 = Mediator('Mediator1', object())
        mediator2 = Mediator('Mediator2', object())

        facade1.registerMediator(mediator1)
        facade2.registerMediator(mediator2)

        self.assertEqual(True, facade1.hasMediator('Mediator1'))
        self.assertEqual(False, facade2.hasMediator('Mediator1'))

        self.assertEqual(False, facade1.hasMediator('Mediator2'))
        self.assertEqual(True, facade2.hasMediator('Mediator2'))

        # Remove mediators
        facade1.removeMediator('Mediator1')
        facade2.removeMediator('Mediator2')

        self.assertEqual(False, facade1.hasMediator('Mediator1'))
        self.assertEqual(False, facade2.hasMediator('Mediator2'))

    def testHasCommand(self):
        """FacadeTest: Test hasCommand()"""
        # Create facades
        facade1 = Facade.getInstance(self.KEY1)
        facade2 = Facade.getInstance(self.KEY2)

        # Register commands
        facade1.registerCommand('TestCommand', FacadeTestCommand)
        facade2.registerCommand('InstanceCommand', FacadeInstanceTestCommand)

        self.assertEqual(True, facade1.hasCommand('TestCommand'))
        self.assertEqual(False, facade2.hasCommand('TestCommand'))

        self.assertEqual(False, facade1.hasCommand('InstanceCommand'))
        self.assertEqual(True, facade2.hasCommand('InstanceCommand'))

        # Remove commands
        facade1.removeCommand('TestCommand')
        facade2.removeCommand('InstanceCommand')

        self.assertEqual(False, facade1.hasCommand('TestCommand'))
        self.assertEqual(False, facade2.hasCommand('InstanceCommand'))

    def testGetInstance(self):
        """FacadeTests: Get instance of the Facade implementation"""
        class MyFacade(Facade):
            pass

        self.assertIsInstance(MyFacade.getInstance("myFacade"), MyFacade)
