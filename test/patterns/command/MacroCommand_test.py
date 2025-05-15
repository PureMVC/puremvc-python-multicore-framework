# MacroCommand_test.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

import unittest

from puremvc.interfaces import INotification
from puremvc.patterns.command import SimpleCommand, MacroCommand
from puremvc.patterns.observer import Notification


class MacroCommandTest(unittest.TestCase):
    """
    Tests operation of a 'MacroCommand'.

    This test creates a new 'Notification', adding a
    'MacroCommandTestVO' as the body.
    It then creates a 'MacroCommandTestCommand' and invokes
    its 'execute' method, passing in the
    'Notification'.

    The 'MacroCommandTestCommand' has defined an
    'initializeMacroCommand' method, which is
    called automatically by its constructor. In this method,
    the 'MacroCommandTestCommand' adds 2 SubCommands
    to itself, 'MacroCommandTestSub1Command' and
    'MacroCommandTestSub2Command'.

    The 'MacroCommandTestVO' has 2 result properties,
    one is set by 'MacroCommandTestSub1Command' by
    multiplying the input property by 2, and the other is set
    by 'MacroCommandTestSub2Command' by multiplying
    the input property by itself.

    Success is determined by evaluating the 2 result properties
    on the 'MacroCommandTestVO' that was passed to
    the 'MacroCommandTestCommand' on the Notification
    body.
    """

    def test_macro_command_execute(self):
        # Create the VO
        vo = MacroCommandTestVO(5)

        # Create the Notification (note)
        note = Notification("MacroCommandTest", vo)

        # Create the SimpleCommand
        command = MacroCommandTestCommand()

        # Execute the SimpleCommand
        command.execute(note)

        # test assertions
        self.assertTrue(vo.result1 == 10)
        self.assertTrue(vo.result2 == 25)


class MacroCommandTestCommand(MacroCommand):

    def initialize_macro_command(self):
        """Initialize the MacroCommandTestCommand by adding its 2 SubCommands."""
        self.add_subcommand(lambda: MacroCommandTestSub1Command())
        self.add_subcommand(lambda: MacroCommandTestSub2Command())


class MacroCommandTestSub1Command(SimpleCommand):
    def execute(self, notification: INotification):
        """
        Fabricate a result by multiplying the input by 2

        :param notification: Notification carrying the 'MacroCommandTestVO'
        :type notification: INotification
        """
        vo = notification.body

        # Fabricate a result
        vo.result1 = 2 * vo.input


class MacroCommandTestSub2Command(SimpleCommand):
    """A SimpleCommand subclass used by MacroCommandTestCommand."""

    def execute(self, notification: INotification):
        """
        Fabricate a result by multiplying the input by itself
        :param notification: event the 'IEvent' carrying the 'MacroCommandTestVO'
        :type notification: INotification
        """
        vo = notification.body

        # Fabricate a result
        vo.result2 = vo.input * vo.input


class MacroCommandTestVO:
    def __init__(self, data: int):
        """
        Constructor.

        :param data: The number to be fed to the MacroCommandTestCommand
        """
        self.input = data
        self.result1 = 0
        self.result2 = 0


if __name__ == '__main__':
    unittest.main()
