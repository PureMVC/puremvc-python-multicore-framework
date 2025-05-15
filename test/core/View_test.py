# View_test.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

import unittest

from puremvc.core import View
from puremvc.interfaces import IView, INotification, IMediator, IObserver
from puremvc.patterns.mediator import Mediator
from puremvc.patterns.observer import Observer, Notification


class ViewTest(unittest.TestCase):
    """Test the PureMVC View class."""
    NOTE1 = "note1"
    NOTE2 = "note2"
    NOTE3 = "note3"
    NOTE4 = "note4"
    NOTE5 = "note5"
    NOTE6 = "note6"

    def __init__(self, method_name: str = "runTest"):
        """Constructor."""
        super().__init__(method_name)
        self.lastNotification = ""
        self.onRegisterCalled = False
        self.onRemoveCalled = False
        self.counter = 0

    def test_get_Instance(self):
        """Tests the View Multiton Factory Method """
        # Test Factory Method
        view: IView = View.get_instance("ViewTestKey1", lambda k: View(k))

        # test assertions
        self.assertIsNotNone(view, "Expecting instance not None")
        self.assertIsInstance(view, IView, "Expecting instance implements IView")
        self.assertEqual(view, View.get_instance("ViewTestKey1", lambda k: View(k)))
        self.assertNotEqual(view, View.get_instance("Key123", lambda k: View(k)))

    """
    Tests registration and notification of Observers.
    
    An Observer is created to callback the viewTestMethod of
    this ViewTest instance. This Observer is registered with
    the View to be notified of 'ViewTestEvent' events. Such
    an event is created, and a value set on its payload. Then
    the View is told to notify interested observers of this
    Event. 
    
    The View calls the Observer's notifyObserver method
    which calls the viewTestMethod on this instance
    of the ViewTest class. The viewTestMethod method will set 
    an instance variable to the value passed in on the Event
    payload. We evaluate the instance variable to be sure
    it is the same as that passed out as the payload of the 
    original 'ViewTestEvent'.
    """

    def test_register_and_notify_observer(self):
        # Get the Multiton View instance
        view: IView = View.get_instance("ViewTestKey2", lambda k: View(k))

        # Create observer, passing in notification method and context
        observer: IObserver = Observer(self.view_test_method, self)

        # Register Observer's interest in a particular Notification with the View
        view.register_observer("ViewTestNote", observer)

        # Create a ViewTestNote, setting
        # a body value, and tell the View to notify 
        # Observers. Since the Observer is this class 
        # and the notification method is viewTestMethod,
        # successful notification will result in our local 
        # viewTestVar being set to the value we pass in 
        # on the note body.
        note: INotification = Notification("ViewTestNote", 10)
        view.notify_observers(note)

        # test assertions
        self.assertTrue(self.viewTestVar == 10, "Expecting viewTestVar = 10")

    def view_test_method(self, note: INotification):
        """
        A utility method to test the notification of Observers by the view
        """
        # A test variable that proves the viewTestMethod was invoked by the View.
        self.viewTestVar = note.body

    def test_register_and_retrieve_mediator(self):
        """Tests registering and retrieving a mediator with the View."""
        # Get the Multiton View instance
        view: IView = View.get_instance("ViewTestKey3", lambda k: View(k))

        # Create and register the test mediator
        view_test_mediator: IMediator = ViewTestMediator(self)
        view.register_mediator(view_test_mediator)

        # Retrieve the component
        mediator: IMediator = view.retrieve_mediator(ViewTestMediator.NAME)

        # test assertions
        self.assertIsInstance(mediator, ViewTestMediator, "Expecting mediator is ViewTestMediator")

    def test_has_mediator(self):
        """Tests the hasMediator Method"""
        # register a Mediator
        view: IView = View.get_instance("ViewTestKey4", lambda k: View(k))

        # Create and register the test mediator
        mediator: IMediator = Mediator("hasMediatorTest", self)
        view.register_mediator(mediator)

        # assert that the view.hasMediator method returns true for that mediator name
        self.assertTrue(view.has_mediator("hasMediatorTest"),
                        "Expecting view.has_mediator('hasMediatorTest') == true")

        view.remove_mediator("hasMediatorTest")

        # assert that the view.hasMediator method returns false for that mediator name
        self.assertFalse(view.has_mediator("hasMediatorTest"),
                         "Expecting view.has_mediator('has_mediator_test') == false")

    def test_register_and_remove_mediator(self):
        """Tests registering and removing a mediator """
        # Get the Multiton View instance
        view: IView = View.get_instance("ViewTestKey5", lambda k: View(k))

        # Create and register the test mediator
        mediator: IMediator = Mediator("testing", self)
        view.register_mediator(mediator)

        # Remove the component
        removed_mediator: IMediator = view.remove_mediator("testing")

        # assert that we have removed the appropriate mediator
        self.assertTrue(removed_mediator.mediator_name == "testing",
                        "Expecting removedMediator.mediator_name == 'testing'")

        # assert that the mediator is no longer retrievable
        self.assertIsNone(view.retrieve_mediator("testing"),
                          "Expecting view.retrieveMediator('testing') == None )")

    def test_on_register_and_on_remove(self):
        """Tests that the View calls the on_register and on_remove methods"""
        # Get the Multiton View instance
        view: IView = View.get_instance("ViewTestKey6", lambda k: View(k))

        # Create and register the test mediator
        mediator: IMediator = ViewTestMediator4(self)
        view.register_mediator(mediator)

        # assert that onRegisterCalled was called, and the mediator responded by setting our boolean
        self.assertTrue(self.onRegisterCalled, "Expecting onRegisterCalled == true")

        # Remove the component
        view.remove_mediator(ViewTestMediator4.NAME)

        # assert that the mediator is no longer retrievable
        self.assertTrue(self.onRemoveCalled, "Expecting onRemoveCalled == true")

    def test_successive_register_and_remove_mediator(self):
        """Tests successive register and remove of the same mediator."""
        # Get the Multiton View instance
        view: IView = View.get_instance("ViewTestKey7", lambda k: View(k))

        # Create and register the test mediator, but not so we have a reference to it
        view.register_mediator(ViewTestMediator(self))

        # test that we can retrieve it
        self.assertIsInstance(view.retrieve_mediator(ViewTestMediator.NAME), ViewTestMediator,
                              "Expecting view.retrieveMediator(ViewTestMediator.NAME) is ViewTestMediator")

        # Remove the Mediator
        view.remove_mediator(ViewTestMediator.NAME)

        # test that retrieving it now returns None
        self.assertIsNone(view.retrieve_mediator(ViewTestMediator.NAME),
                          "Expecting view.retrieve_mediator(ViewTestMediator.NAME) == None")

        # test that removing the mediator again once its gone doesn't cause crash
        self.assertIsNone(view.remove_mediator(ViewTestMediator.NAME),
                          "Expecting view.remove_mediator(ViewTestMediator.NAME) doesn't crash")

        # Create and register another instance of the test mediator
        view.register_mediator(ViewTestMediator(self))

        self.assertIsInstance(view.retrieve_mediator(ViewTestMediator.NAME), ViewTestMediator,
                              "Expecting view.retrieve_mediator(ViewTestMediator.NAME) is ViewTestMediator")

        # Remove the Mediator
        view.remove_mediator(ViewTestMediator.NAME)

        # test that retrieving it now returns None
        self.assertIsNone(view.retrieve_mediator(ViewTestMediator.NAME),
                          "Expecting view.retrieve_mediator(ViewTestMediator.NAME) == None")

    def test_remove_mediator_and_subsequent_notify(self):
        """
        Tests registering a Mediator for 2 different notifications, removing the
        Mediator from the View, and seeing that neither notification causes the
        Mediator to be notified.
        """
        # Get the Multiton View instance
        view: IView = View.get_instance("ViewTestKey8", lambda k: View(k))

        # Create and register the test mediator to be removed.
        view.register_mediator(ViewTestMediator2(self))

        # test that notifications work
        view.notify_observers(Notification(ViewTest.NOTE1))
        self.assertTrue(self.lastNotification == ViewTest.NOTE1, "Expecting lastNotification == NOTE1")

        view.notify_observers(Notification(ViewTest.NOTE2))
        self.assertTrue(self.lastNotification == ViewTest.NOTE2, "Expecting lastNotification == NOTE2")

        # Remove the Mediator
        view.remove_mediator(ViewTestMediator2.NAME)

        # test that retrieving it now returns None
        self.assertIsNone(view.retrieve_mediator(ViewTestMediator2.NAME),
                          "Expecting view.retrieve_mediator(ViewTestMediator2.NAME) == None")

        # test that notifications no longer work
        # (ViewTestMediator2 is the one that sets lastNotification
        # on this component, and ViewTestMediator)
        self.lastNotification = None

        view.notify_observers(Notification(ViewTest.NOTE1))
        self.assertTrue(self.lastNotification != ViewTest.NOTE1, "Expecting lastNotification != NOTE1")

        view.notify_observers(Notification(ViewTest.NOTE2))
        self.assertTrue(self.lastNotification != ViewTest.NOTE2, "Expecting lastNotification != NOTE2")

    def test_remove_one_of_two_mediators_and_subsequent_notify(self):
        """
        Tests registering one of two registered Mediators and seeing
        that the remaining one still responds.
        """
        # Get the Multiton View instance
        view: IView = View.get_instance("ViewTestKey9", lambda k: View(k))

        # Create and register that responds to notifications 1 and 2
        view.register_mediator(ViewTestMediator2(self))

        # Create and register that responds to notification 3
        view.register_mediator(ViewTestMediator3(self))

        # test that all notifications work
        view.notify_observers(Notification(ViewTest.NOTE1))
        self.assertTrue(self.lastNotification == ViewTest.NOTE1, "Expecting lastNotification == NOTE1")

        view.notify_observers(Notification(ViewTest.NOTE2))
        self.assertTrue(self.lastNotification == ViewTest.NOTE2, "Expecting lastNotification == NOTE2")

        view.notify_observers(Notification(ViewTest.NOTE3))
        self.assertTrue(self.lastNotification == ViewTest.NOTE3, "Expecting lastNotification == NOTE3")

        # Remove the Mediator that responds to 1 and 2
        view.remove_mediator(ViewTestMediator2.NAME)

        # test that retrieving it now returns None
        self.assertIsNone(view.retrieve_mediator(ViewTestMediator2.NAME),
                          "Expecting view.retrieve_mediator(ViewTestMediator2.NAME) == None")

        # test that notifications no longer work
        # for notifications 1 and 2, but still work for 3
        self.lastNotification = None

        view.notify_observers(Notification(ViewTest.NOTE1))
        self.assertTrue(self.lastNotification != ViewTest.NOTE1)

        view.notify_observers(Notification(ViewTest.NOTE2))
        self.assertTrue(self.lastNotification != ViewTest.NOTE2)

        view.notify_observers(Notification(ViewTest.NOTE3))
        self.assertTrue(self.lastNotification == ViewTest.NOTE3)

    def test_mediator_reregistration(self):
        """
        Tests registering the same mediator twice.
        A subsequent notification should only illicit
        one response. Also, since reregistration
        was causing 2 observers to be created, ensure
        that after removal of the mediator there will
        be no further response.
        """
        # Get the Singleton View instance
        view: IView = View.get_instance("ViewTestKey10", lambda k: View(k))

        # Create and register that responds to notification 5
        view.register_mediator(ViewTestMediator5(self))

        # try to register another instance of that mediator (uses the same NAME constant).
        view.register_mediator(ViewTestMediator5(self))

        # test that the counter is only incremented once (mediator 5's response)
        self.counter = 0
        view.notify_observers(Notification(ViewTest.NOTE5))
        self.assertEqual(self.counter, 1, "Expecting counter == 1")

        # Remove the Mediator
        view.remove_mediator(ViewTestMediator5.NAME)

        # test that retrieving it now returns None
        self.assertIsNone(view.retrieve_mediator(ViewTestMediator5.NAME),
                          "Expecting view.retrieve_mediator(ViewTestMediator5.NAME) == None")

        # test that the counter is no longer incremented
        self.counter = 0
        view.notify_observers(Notification(ViewTest.NOTE5))
        self.assertEqual(self.counter, 0, "Expecting counter == 0")

    def test_modify_observer_list_during_notification(self):
        """
        Tests the ability for the observer list to
        be modified during the process of notification,
        and all observers be properly notified. This
        happens most often when multiple Mediators
        respond to the same notification by removing
        themselves.
        """
        # Get the Singleton View instance
        view: IView = View.get_instance("ViewTestKey11", lambda k: View(k))

        # Create and register several mediator instances that respond to notification 6 
        # by removing themselves, which will cause the observer list for that notification 
        # to change.
        view.register_mediator(ViewTestMediator6(ViewTestMediator6.NAME + "/1", self))
        view.register_mediator(ViewTestMediator6(ViewTestMediator6.NAME + "/2", self))
        view.register_mediator(ViewTestMediator6(ViewTestMediator6.NAME + "/3", self))
        view.register_mediator(ViewTestMediator6(ViewTestMediator6.NAME + "/4", self))
        view.register_mediator(ViewTestMediator6(ViewTestMediator6.NAME + "/5", self))
        view.register_mediator(ViewTestMediator6(ViewTestMediator6.NAME + "/6", self))
        view.register_mediator(ViewTestMediator6(ViewTestMediator6.NAME + "/7", self))
        view.register_mediator(ViewTestMediator6(ViewTestMediator6.NAME + "/8", self))

        # clear the counter
        self.counter = 0

        # send the notification. each of the above mediators will respond by removing
        # themselves and incrementing the counter by 1. This should leave us with a
        # count of 8, since 8 mediators will respond.
        view.notify_observers(Notification(ViewTest.NOTE6))

        # verify the count is correct
        self.assertEqual(self.counter, 8, "Expecting counter == 8")

        # clear the counter
        self.counter = 0
        view.notify_observers(Notification(ViewTest.NOTE6))
        # verify the count is 0
        self.assertEqual(self.counter, 0, "Expecting counter == 0")


class ViewTestMediator(Mediator):
    # A Mediator class used by ViewTest.
    NAME = "ViewTestMediator"

    def __init__(self, view: object):
        super().__init__(ViewTestMediator.NAME, view)

    def list_notification_interests(self) -> [str]:
        return ["ABC", "DEF", "GHI"]


class ViewTestMediator2(Mediator):
    # The Mediator name
    NAME = "ViewTestMediator2"

    def __init__(self, view: object):
        super().__init__(ViewTestMediator2.NAME, view)

    def list_notification_interests(self) -> [str]:
        # be sure that the mediator has some Observers created
        # to test remove_mediator
        return [ViewTest.NOTE1, ViewTest.NOTE2]

    def handle_notification(self, notification: INotification):
        self.view_component.lastNotification = notification.name


class ViewTestMediator3(Mediator):
    # The Mediator name
    NAME = "ViewTestMediator3"

    def __init__(self, view: object):
        super().__init__(ViewTestMediator3.NAME, view)

    def list_notification_interests(self) -> [str]:
        # be sure that the mediator has some Observers created
        # to test remove_mediator
        return [ViewTest.NOTE3]

    def handle_notification(self, notification: INotification):
        self.view_component.lastNotification = notification.name


class ViewTestMediator4(Mediator):
    # The Mediator name
    NAME = "ViewTestMediator4"

    def __init__(self, view: object):
        super().__init__(ViewTestMediator4.NAME, view)

    def on_register(self):
        self.view_component.onRegisterCalled = True

    def on_remove(self):
        self.view_component.onRemoveCalled = True


class ViewTestMediator5(Mediator):
    # The Mediator name
    NAME = "ViewTestMediator5"

    def __init__(self, view: object):
        super().__init__(ViewTestMediator5.NAME, view)

    def list_notification_interests(self) -> [str]:
        return [ViewTest.NOTE5]

    def handle_notification(self, notification: INotification):
        self.view_component.counter += 1


class ViewTestMediator6(Mediator):
    # The Mediator name
    NAME = "ViewTestMediator6"

    def __init(self, name: str, view: object):
        super().__init__(name, view)

    def list_notification_interests(self) -> [str]:
        return [ViewTest.NOTE6]

    def handle_notification(self, notification: INotification):
        self.facade.remove_mediator(self.mediator_name)

    def on_remove(self):
        self.view_component.counter += 1


if __name__ == '__main__':
    unittest.main()
