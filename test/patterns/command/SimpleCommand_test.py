# SimpleCommand_test.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

import unittest

from puremvc.interfaces import INotification
from puremvc.patterns.command import SimpleCommand
from puremvc.patterns.observer import Notification


class SimpleCommandTest(unittest.TestCase):
    """Test the PureMVC SimpleCommand class."""

    def test_simple_command_execute(self):
        """
        Tests the `execute` method of a `SimpleCommand`.
        
        This test creates a new `Notification`, adding a 
        `SimpleCommandTestVO` as the body. 
        It then creates a `SimpleCommandTestCommand` and invokes
        its `execute` method, passing in the note.
        
        Success is determined by evaluating a property on the 
        object that was passed on the Notification body, which will
        be modified by the SimpleCommand
        """
        # Create the VO
        vo = SimpleCommandTestVO(5)

        # Create the Notification (note)
        note = Notification("SimpleCommandTestNote", vo)

        # Create the SimpleCommand
        command = SimpleCommandTestCommand()

        # Execute the SimpleCommand
        command.execute(note)

        # test assertions
        self.assertTrue(vo.result == 10, "Expecting vo.result == 10")


class SimpleCommandTestCommand(SimpleCommand):
    """A SimpleCommand subclass used by SimpleCommandTest."""

    def execute(self, notification: INotification):
        """
        Fabricate a result by multiplying the input by 2
        :param notification: The `INotification` carrying the `SimpleCommandTestVO`
        """
        vo = notification.body

        # Fabricate a result
        vo.result = 2 * vo.input


class SimpleCommandTestVO:

    def __init__(self, data: int):
        """
        Constructor.

        :param data: The number to be fed to the SimpleCommandTestCommand
        """
        self.input = data
        self.result = 0


if __name__ == '__main__':
    unittest.main()
