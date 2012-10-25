# -*- coding: utf-8 -*-

from puremvc import MultitonError
from puremvc.core import View
from puremvc.interfaces import IView
from puremvc.patterns.mediator import Mediator
from puremvc.patterns.observer import Observer, Notification
from utils.view import (ViewTestMediator, ViewTestMediator2, ViewTestMediator3,
    ViewTestMediator4, ViewTestMediator5, ViewTestNote)
import unittest
import uuid


class ViewTest(unittest.TestCase):
    """ViewTest: Test View Singleton"""

    lastNotification = None
    onRegisterCalled = False
    onRemoveCalled = False
    counter = 0

    KEY1 = uuid.uuid4()
    KEY2 = uuid.uuid4()

    NOTE1 = "note1"
    NOTE2 = "note2"
    NOTE3 = "note3"
    NOTE5 = "note5"

    def tearDown(self):
        View.getInstance(self.KEY1).removeMediator(ViewTestMediator.NAME)
        View.getInstance(self.KEY1).removeMediator(ViewTestMediator2.NAME)
        View.getInstance(self.KEY1).removeMediator(ViewTestMediator3.NAME)
        View.getInstance(self.KEY1).removeMediator(ViewTestMediator4.NAME)
        View.getInstance(self.KEY1).removeMediator(ViewTestMediator5.NAME)

    def testErrorSameKey(self):
        """ModelTest: raise error if create controller with same key"""
        model = View(self.KEY1)

        self.assertRaises(MultitonError, View, self.KEY1)

    def testGetInstance(self):
        """ViewTest: Test get view instance"""
        view1 = View.getInstance(self.KEY1)
        view2 = View.getInstance(self.KEY2)

        self.assertNotEqual(None, view1)
        self.assertNotEqual(None, view2)
        self.assertNotEqual(view1, view2)

    def testIsIView(self):
        """ViewTest: Test instance implements IView"""
        view = View.getInstance(self.KEY1)

        self.assertEqual(True, isinstance(view, IView))

    def testRegisterAndNotifyObserver(self):
        """ViewTest: Test registerObserver() and notifyObservers()"""
        def viewTestMethod(note):
            self.viewTestVar = note.getBody()

        self.viewTestVar = 0

        view = View.getInstance(self.KEY1)
        obsvr = Observer(viewTestMethod, self)
        view.registerObserver(ViewTestNote.NAME, obsvr)

        note = ViewTestNote.create(10)
        view.notifyObservers(note)

        self.assertEqual(True, self.viewTestVar == 10)

    def testRegisterAndRetrieveMediator(self):
        """ViewTest: Test registerMediator() and retrieveMediator()"""
        view = View.getInstance(self.KEY1)

        viewTestMediator = ViewTestMediator(self)
        view.registerMediator(viewTestMediator)

        mediator = view.retrieveMediator(ViewTestMediator.NAME)

        self.assertEqual(True, isinstance(mediator, ViewTestMediator))

    def testHasMediator(self):
        """ViewTest: Test hasMediator()"""
        # Create views
        view1 = View.getInstance(self.KEY1)
        view2 = View.getInstance(self.KEY2)

        # Create mediators
        mediator1 = Mediator('hasMediator1', self)
        mediator2 = Mediator('hasMediator2', self)

        # Register mediators
        view1.registerMediator(mediator1)
        view2.registerMediator(mediator2)

        self.assertEqual(True, view1.hasMediator('hasMediator1'))
        self.assertEqual(True, view2.hasMediator('hasMediator2'))

        # Remove mediators
        view1.removeMediator('hasMediator1')
        view2.removeMediator('hasMediator2')

        self.assertEqual(False, view1.hasMediator('hasMediator1'))
        self.assertEqual(False, view2.hasMediator('hasMediator2'))

    def testRegisterAndRemoveMediator(self):
        """ViewTest: Test registerMediator() and removeMediator()"""
        view = View.getInstance(self.KEY1)

        meditr = Mediator('testing', self)
        view.registerMediator(meditr)

        removedMediator = view.removeMediator('testing')

        self.assertEqual(True, removedMediator.getMediatorName() == 'testing')

        self.assertEqual(True, view.retrieveMediator('testing') == None)

    def testOnRegisterAndOnRemove(self):
        """ViewTest: Test onRegsiter() and onRemove()"""
        view = View.getInstance(self.KEY1)

        mediator = ViewTestMediator4(self)
        view.registerMediator(mediator)

        self.assertEqual(True, self.onRegisterCalled)

        view.removeMediator(ViewTestMediator4.NAME)

        self.assertEqual(True, self.onRemoveCalled)

    def testSuccessiveRegisterAndRemoveMediator(self):
        """ViewTest: Test Successive registerMediator() and removeMediator()"""
        view = View.getInstance(self.KEY1)

        view.registerMediator(ViewTestMediator(self))

        self.assertTrue(isinstance(
            view.retrieveMediator(ViewTestMediator.NAME), ViewTestMediator))

        view.removeMediator(ViewTestMediator.NAME)

        self.assertEqual(view.retrieveMediator(ViewTestMediator.NAME), None)

        self.assertEqual(view.removeMediator(ViewTestMediator.NAME), None)

        view.registerMediator(ViewTestMediator(self))

        self.assertTrue(isinstance(
            view.retrieveMediator(ViewTestMediator.NAME), ViewTestMediator))

        view.removeMediator(ViewTestMediator.NAME)

        self.assertEqual(view.retrieveMediator(ViewTestMediator.NAME), None)

    def testRemoveMediatorAndSubsequentNotify(self):
        """ViewTest: Test removeMediator() and subsequent nofity()"""

        view = View.getInstance(self.KEY1)

        view.registerMediator(ViewTestMediator2(self))

        view.notifyObservers(Notification(self.NOTE1))
        self.assertEqual(True, self.lastNotification == self.NOTE1)

        view.notifyObservers(Notification(self.NOTE2))
        self.assertEqual(True, self.lastNotification == self.NOTE2)

        view.removeMediator(ViewTestMediator2.NAME)

        self.assertEqual(view.retrieveMediator(ViewTestMediator2.NAME), None)

        self.lastNotification = None

        view.notifyObservers(Notification(self.NOTE1))
        self.assertEqual(True, self.lastNotification != self.NOTE1)

        view.notifyObservers(Notification(self.NOTE2))
        self.assertEqual(True, self.lastNotification != self.NOTE2)

    def testRemoveOneOfTwoMediatorsAndSubsequentNotify(self):
        """ViewTest: Test removing one of two Mediators and subsequent notify()
        """

        view = View.getInstance(self.KEY1)

        view.registerMediator(ViewTestMediator2(self))

        view.registerMediator(ViewTestMediator3(self))

        view.notifyObservers(Notification(self.NOTE1))
        self.assertEqual(True, self.lastNotification == self.NOTE1)

        view.notifyObservers(Notification(self.NOTE2))
        self.assertEqual(True, self.lastNotification == self.NOTE2)

        view.notifyObservers(Notification(self.NOTE3))
        self.assertEqual(True, self.lastNotification == self.NOTE3)

        view.removeMediator(ViewTestMediator2.NAME)

        self.assertEqual(view.retrieveMediator(ViewTestMediator2.NAME), None)

        self.lastNotification = None

        view.notifyObservers(Notification(self.NOTE1))
        self.assertEqual(True, self.lastNotification != self.NOTE1)

        view.notifyObservers(Notification(self.NOTE2))
        self.assertEqual(True, self.lastNotification != self.NOTE2)

        view.notifyObservers(Notification(self.NOTE3))
        self.assertEqual(True, self.lastNotification == self.NOTE3)

    def testMediatorReregistration(self):
        """
        Tests registering the same mediator twice.

        A subsequent notification should only illicit one response. Also, since
        reregistration was causing 2 observers to be created, ensure that after
        removal of the mediator there will be no further response.

        Added for the fix deployed in version 2.0.4
        """
        view = View.getInstance(self.KEY1)

        view.registerMediator(ViewTestMediator5(self))

        # Try to register another instance of that mediator
        # (uses the same NAME constant).
        view.registerMediator(ViewTestMediator5(self))

        self.counter = 0
        view.notifyObservers(Notification(self.NOTE5))
        self.assertEqual(1, self.counter)

        view.removeMediator(ViewTestMediator5.NAME)

        self.assertEqual(view.retrieveMediator(ViewTestMediator5.NAME), None)

        self.counter = 0
        view.notifyObservers(Notification(self.NOTE5))
        self.assertEqual(0, self.counter)

    def testRemoveSelf(self):
        view = View.getInstance(self.KEY1)

        view.registerMediator(ViewTestMediator2(self))
        view.registerMediator(ViewTestMediator3(self))

        self.assertTrue(self.NOTE5 in view.observerMap)
        view.notifyObservers(Notification(self.NOTE5))
        self.assertFalse(self.NOTE5 in view.observerMap)
