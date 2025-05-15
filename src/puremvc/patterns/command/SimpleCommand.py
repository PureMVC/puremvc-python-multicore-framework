# SimpleCommand.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

from puremvc.interfaces import INotification, ICommand

from puremvc.patterns.facade import Notifier


class SimpleCommand(Notifier, ICommand):
    """
    A base `ICommand` implementation.

    Your subclass should override the `execute`
    method where your business logic will handle the `INotification`.

    See Also
    --------
    :class:`puremvc.core.Controller`
    :class:`puremvc.patterns.observer.Notification`
    :class:`puremvc.patterns.command.MacroCommand`
    """

    def execute(self, notification: INotification):
        """
        Fulfill the use-case initiated by the given `INotification`.

        In the Command Pattern, an application use-case typically
        begins with some user action, which results in an `INotification` being broadcast, which
        is handled by business logic in the `execute` method of an `ICommand`.

        :param notification: The `INotification` to handle.
        :type notification: INotification
        :return: None
        """
        return
