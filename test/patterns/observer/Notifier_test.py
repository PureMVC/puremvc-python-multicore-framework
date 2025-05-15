# Notifier_test.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

import unittest

from puremvc.interfaces import INotification
from puremvc.patterns.command import SimpleCommand
from puremvc.patterns.facade import Notifier


class NotifierTest(unittest.TestCase):
    """Test the PureMVC Notifier class."""

    def test_register_command_and_send_notification(self):
        # Create the Notifier
        notifier = Notifier()

        # Create the Facade, register the NotifierTestCommand to
        # handle 'NotifierTest' notifications
        notifier.initialize_notifier("NotifierTestKey1")
        notifier.facade.register_command("NotifierTestNote", lambda: NotifierTestCommand())

        # Send notification. The Command associated with the event
        # (NotifierTestCommand) will be invoked, and will multiply
        # the vo.input value by 2 and set the result on vo.result
        vo = NotifierTestVO(32)
        notifier.send_notification("NotifierTestNote", vo)

        # test assertions
        self.assertTrue(vo.result == 64, "Expecting vo.result == 64")


class NotifierTestCommand(SimpleCommand):
    def execute(self, notification: INotification):
        """
        Fabricate a result by multiplying the input by 2
        :param notification: the Notification carrying the FacadeTestVO
        :type notification: INotification
        """
        vo = notification.body

        # Fabricate a result
        vo.result = 2 * vo.input


class NotifierTestVO:
    def __init__(self, data: int):
        """
        Constructor.
        :param data: input the number to be fed to the FacadeTestCommand
        :type data: int
        """
        self.input = data
        self.result = None


if __name__ == '__main__':
    unittest.main()
