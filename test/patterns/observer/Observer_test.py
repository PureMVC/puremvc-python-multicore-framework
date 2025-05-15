# Observer_test.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

import unittest

from puremvc.interfaces import INotification
from puremvc.patterns.observer import Notification
from puremvc.patterns.observer import Observer


class ObserverTest(unittest.TestCase):
    """
    Tests PureMVC Observer class.

    Since the Observer encapsulates the interested object's
    callback information, there are no getters, only setters.
    It is, in effect, write-only memory.

    Therefore, the only way to test it is to set the
    notification method and context and call the notifyObserver
    method.
    """

    def test_observer_accessors(self):
        """Tests observer class when initialized by accessor methods."""
        # Create observer with None args, then
        # use accessors to set notification method and context
        observer = Observer(None, None)
        self.observer_test_var = 0

        observer.notify_context = self
        observer.notify_method = self.observer_test_method

        # create a test event, setting a payload value and notify 
        # the observer with it. since the observer is this class
        # and the notification method is observer_test_method,
        # successful notification will result in our local 
        # observer_test_var being set to the value we pass in
        # on the note body.
        note = Notification("ObserverTestNote", 10)
        observer.notify_observer(note)

        # test assertions
        self.assertTrue(self.observer_test_var == 10, "Expecting observer_test_var = 10")

    def test_observer_constructor(self):
        """Tests observer class when initialized by constructor."""
        # Create observer passing in notification method and context
        observer = Observer(self.observer_test_method, self)

        # create a test note, setting a body value and notify 
        # the observer with it. since the observer is this class 
        # and the notification method is observer_test_method,
        # successful notification will result in our local 
        # observer_test_var being set to the value we pass in
        # on the note body.
        note = Notification("ObserverTestNote", 5)
        observer.notify_observer(note)
        self.assertTrue(self.observer_test_var == 5, "Expecting observerTestVar = 5")

    def test_compare_notify_context(self):
        """Tests the compareNotifyContext method of the Observer class"""
        # Create observer passing in notification method and context
        observer = Observer(self.observer_test_method, self)
        neg = object()

        # test assertions
        self.assertFalse(observer.compare_notify_context(neg), "observer.compare_notify_context(neg) == False")
        self.assertTrue(observer.compare_notify_context(self), "observer.compare_notify_context(self) == True")

    def observer_test_method(self, notification: INotification):
        """A function that is used as the observer notification
        method. It multiplies the input number by the
        observer_test_var value"""
        # A test variable that proves the notify method was
        # executed with 'self' as its execution context
        self.observer_test_var = notification.body


if __name__ == "__main__":
    unittest.main()
