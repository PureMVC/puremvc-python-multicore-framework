# IController.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

from abc import ABC, abstractmethod
from typing import Callable

from .ICommand import ICommand
from .INotification import INotification


class IController(ABC):
    """
    The interface definition for a PureMVC Controller.

    In PureMVC, an `IController` implementor follows the 'Command and Controller' strategy, and
    assumes these responsibilities:

    Remembering which `ICommand`s are intended to handle which `INotifications`.

    Registering itself as an `IObserver` with the `View` for each `INotification`
    that it has an `ICommand` mapping for.

    Creating a new instance of the proper `ICommand` to handle a given `INotification` when notified by the `View`.

    Calling the `ICommand`'s `execute` method, passing in the `INotification`.

    See Also
    --------
    :class:`puremvc.interfaces.INotification`
    :class:`puremvc.interfaces.ICommand`
    """

    @abstractmethod
    def register_command(self, notification_name: str, factory: Callable[[], ICommand]):
        """
        Register a particular `ICommand` class as the handler for a particular `INotification`.

        :param notification_name: The name of the `INotification`
        :type notification_name: str
        :param factory: A factory function that returns an instance of ICommand.
        :type factory: Callable[[], ICommand]
        :return: None
        """
        pass

    @abstractmethod
    def execute_command(self, notification: INotification):
        """
        Execute the `ICommand` previously registered as the handler for
        `INotification` with the given notification name.

        :param notification: The `INotification` to execute the associated `ICommand` for
        :type notification: INotification
        :return: None
        """
        pass

    @abstractmethod
    def has_command(self, notification_name: str) -> bool:
        """
        Check if a Command is registered for a given Notification.

        :param notification_name: The name of the `INotification`
        :type notification_name: str
        :return: True if a command is registered for the notification_name, False otherwise.
        :rtype: bool
        """
        pass

    @abstractmethod
    def remove_command(self, notification_name: str):
        """
        Remove a previously registered `ICommand` to `INotification` mapping.

        :param notification_name: The name of the `INotification` to remove the `ICommand` mapping for
        :type notification_name: str
        :return: None
        """
        pass
