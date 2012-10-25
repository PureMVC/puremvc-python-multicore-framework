# -*- coding: utf-8 -*-

from puremvc.patterns.observer import Observer, Notification, Notifier
import unittest


class ObserverTest(unittest.TestCase):
    """ObserverTest: Test Observer Pattern"""

    __observerTestVar = None

    def __observerTestMethod(self, note):
        self.__observerTestVar = note.getBody()

    def testReprAttribute(self):
        """ObserverTest: test __repr__()"""
        obj1 = object()
        obj2 = object()

        self.assertEqual(
            repr(Notification('ObserverTestNote', None)),
            "Notification Name: ObserverTestNote"
                + "\nBody:None"
                + "\nType:None"
        )
        self.assertEqual(
            repr(Notification('ObserverTestNote', 1, 2)),
            "Notification Name: ObserverTestNote"
                + "\nBody:1"
                + "\nType:2"
        )
        self.assertEqual(
            repr(Notification('ObserverTestNote', "aaa", "bbb")),
            "Notification Name: ObserverTestNote"
                + "\nBody:" + repr("aaa")
                + "\nType:" + repr("bbb")
        )
        self.assertEqual(
            repr(Notification('ObserverTestNote', obj1, obj2)),
            "Notification Name: ObserverTestNote"
                + "\nBody:" + repr(obj1)
                + "\nType:" + repr(obj2)
        )

    def testObserverAccessors(self):
        """ObserverTest: Test Observer Accessors"""

        obsrvr = Observer(None, None)
        obsrvr.setNotifyContext(self)

        obsrvr.setNotifyMethod(self.__observerTestMethod)

        note = Notification('ObserverTestNote', 10)
        obsrvr.notifyObserver(note)

        self.assertEqual(True, self.__observerTestVar == 10)

    def testObserverConstructor(self):
        """ObserverTest: Test Observer Constructor"""

        obsrvr = Observer(self.__observerTestMethod, self)

        note = Notification('ObserverTestNote', 5)
        obsrvr.notifyObserver(note)

        self.assertEqual(True, self.__observerTestVar == 5)

    def testCompareNotifyContext(self):
        """ObserverTest: Test compareNotifyContext()"""

        obsrvr = Observer(self.__observerTestMethod, self)

        negTestObj = object()

        self.assertEqual(False, obsrvr.compareNotifyContext(negTestObj))
        self.assertEqual(True, obsrvr.compareNotifyContext(self))

    def testNameAccessors(self):
        """NotificationTest: Test Name Accessors"""

        note = Notification('TestNote')

        self.assertEqual(True, note.getName() == 'TestNote')

    def testBodyAccessors(self):
        """NotificationTest: Test Body Accessors"""

        note = Notification(None)
        note.setBody(5)

        self.assertEqual(True, note.getBody() == 5)

    def testConstructor(self):
        """NotificationTest: Test Constructor"""
        note = Notification('TestNote', 5, 'TestNoteType')

        self.assertEqual(True, note.getName() == 'TestNote')
        self.assertEqual(True, note.getBody() == 5)
        self.assertEqual(True, note.getType() == 'TestNoteType')


class NotifierTest(unittest.TestCase):
    """ObserverTest: Test Observer Pattern"""

    def setUp(self):
        self.notifier = Notifier()
        self.notifier.multitonKey = "key"

    def testSendNotificationNoBodyAndType(self):
        """NotifierTest: send notification without body and type"""
        try:
            self.notifier.sendNotification("TestNotification")
        except Exception as e:
            self.fail(e)

    def testSendNotificationNoType(self):
        """NotifierTest: send notification without type"""
        try:
            self.notifier.sendNotification("TestNotification", 1)
        except Exception as e:
            self.fail(e)
