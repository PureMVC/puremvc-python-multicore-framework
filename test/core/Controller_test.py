# Controller_test.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

import unittest

from puremvc.core import Controller, View
from puremvc.interfaces import IController, INotification, IView
from puremvc.patterns.command import SimpleCommand
from puremvc.patterns.observer import Notification


class ControllerTest(unittest.TestCase):
    """Test the PureMVC Controller class."""

    def test_get_instance(self):
        # Test Factory Method
        controller: IController = Controller.get_instance("ControllerTestKey1", lambda k: Controller(k))

        # test assertions
        self.assertIsNotNone(controller, "Expecting instance not None")
        self.assertIsInstance(controller, IController, "Expecting instance implements IController")

    """
    Tests Command registration and execution.
    
    This test gets a Multiton Controller instance 
    and registers the ControllerTestCommand class 
    to handle 'ControllerTest' Notifications.
    
    It then constructs such a Notification and tells the 
    Controller to execute the associated Command.
    Success is determined by evaluating a property
    on an object passed to the Command, which will
    be modified when the Command executes.
    """

    def test_register_and_execute_command(self):
        # Create the controller, register the ControllerTestCommand to handle 'ControllerTest' notes
        controller: IController = Controller.get_instance("ControllerTestKey2", lambda k: Controller(k))
        controller.register_command("ControllerTest", lambda: ControllerTestCommand())

        # Create a 'ControllerTest' note
        vo = ControllerTestVO(12)
        note = Notification("ControllerTest", vo)

        # Tell the controller to execute the Command associated with the note
        # the ControllerTestCommand invoked will multiply the vo.input value
        # by 2 and set the result on vo.result
        controller.execute_command(note)

        # test assertions 
        self.assertTrue(vo.result == 24, "Expecting vo.result == 24")

    """
     Tests Command registration and removal.
     
     Tests that once a Command is registered and verified
     working, it can be removed from the Controller.
    """

    def test_register_and_remove_command(self):
        # Create the controller, register the ControllerTestCommand to handle 'ControllerTest' notes
        controller: IController = Controller.get_instance("ControllerTestKey3", lambda k: Controller(k))
        controller.register_command("ControllerRemoveTest", lambda: ControllerTestCommand())

        # Create a 'ControllerTest' note
        vo = ControllerTestVO(12)
        note = Notification("ControllerRemoveTest", vo)

        # Tell the controller to execute the Command associated with the note
        # the ControllerTestCommand invoked will multiply the vo.input value
        # by 2 and set the result on vo.result
        controller.execute_command(note)

        # test assertions
        self.assertTrue(vo.result == 24, "Expecting vo.result == 24")

        # Reset result
        vo.result = 0

        # Remove the Command from the Controller
        controller.remove_command("ControllerRemoveTest")

        # Tell the controller to execute the Command associated with the
        # note. This time, it should not be registered, and our vo result
        # will not change
        controller.execute_command(note)

        # test assertions
        self.assertTrue(vo.result == 0, "Expecting vo.result == 0")

    """
    Test hasCommand method.
    """

    def test_has_command(self):
        # register the ControllerTestCommand to handle 'hasCommandTest' notes
        controller: IController = Controller.get_instance("ControllerTestKey4", lambda k: Controller(k))
        controller.register_command("hasCommandTest", lambda: ControllerTestCommand())

        # test that hasCommand returns true for hasCommandTest notifications
        self.assertTrue(controller.has_command("hasCommandTest"),
                        "Expecting controller.has_command('hasCommandTest') == true")

        # Remove the Command from the Controller
        controller.remove_command("hasCommandTest")

        # test that hasCommand returns false for hasCommandTest notifications 
        self.assertFalse(controller.has_command("hasCommandTest"),
                         "Expecting controller.has_command('hasCommandTest') == false")

    """
    Tests Removing and Reregistering a Command
    
    Tests that when a Command is re-registered that it isn't fired twice.
    This involves, minimally, registration with the controller but
    notification via the View, rather than direct execution of
    the Controller's executeCommand method as is done above in 
    testRegisterAndRemove. 
    """

    def test_re_register_and_execute_command(self):
        # Fetch the controller, register the ControllerTestCommand2 to handle 'ControllerTest2' notes
        controller: IController = Controller.get_instance("ControllerTestKey5", lambda k: Controller(k))
        controller.register_command("ControllerTestKey2", lambda: ControllerTestCommand2())

        # Remove the Command from the Controller
        controller.remove_command("ControllerTest2")

        # Re-register the Command with the Controller
        controller.register_command("ControllerTest2", lambda: ControllerTestCommand2())

        # Create a 'ControllerTest2' note
        vo = ControllerTestVO(12)
        note = Notification("ControllerTest2", vo)

        # retrieve a reference to the View from the same core.
        view: IView = View.get_instance("ControllerTestKey5", lambda k: View(k))

        # send the Notification
        view.notify_observers(note)

        # test assertions
        # if the command is executed once the value will be 24
        self.assertTrue(vo.result == 24, "Expecting vo.result == 24")

        # Prove that accumulation works in the VO by sending the notification again
        view.notify_observers(note)

        # if the command is executed twice, the value will be 48
        self.assertTrue(vo.result == 48, "Expecting vo.result == 48")


class ControllerTestCommand(SimpleCommand):
    """
    A SimpleCommand subclass used by ControllerTest.
    """

    def execute(self, notification: INotification):
        """
        Fabricate a result by multiplying the input by 2

        :param notification: The note carrying the ControllerTestVO
        :return:
        """
        vo: ControllerTestVO = notification.body

        # Fabricate a result
        vo.result = 2 * vo.input


class ControllerTestCommand2(SimpleCommand):
    """
    A SimpleCommand subclass used by ControllerTest.
    """

    def execute(self, notification: INotification):
        """
        Fabricate a result by multiplying the input by 2 and adding to the existing result

        This tests accumulation effect that would show if the command were executed more than once.
        :param notification:
        :return:
        """
        vo: ControllerTestVO = notification.body
        vo.result = vo.result + (2 * vo.input)


class ControllerTestVO:
    """
    A utility class used by ControllerTest.
    """

    def __init__(self, data: int):
        """
        Constructor.

        :param data: the number to be fed to the ControllerTestCommand
        """
        self.input = data
        self.result = 0


if __name__ == '__main__':
    unittest.main()
