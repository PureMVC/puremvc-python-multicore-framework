# IMediator.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

from abc import abstractmethod
from typing import Any

from .INotification import INotification
from .INotifier import INotifier


class IMediator(INotifier):
    """
    The base interface for all Mediator classes.

    In PureMVC, `IMediator` implementors assume these responsibilities:

    Implement a common method which returns a list of all `INotification`
    the `IMediator` has interest in implementing a notification callback method.
    Implement methods that are called when the IMediator is registered or removed from the View.
    
    Additionally, `IMediator` typically:

    Act as an intermediary between one or more view components such as text boxes or
    list controls, maintaining references and coordinating their behavior.

    In Flash-based apps, this is often the place where event listeners are
    added to view components, and their handlers implemented.

    Respond to and generate `INotifications`, interacting with of
    the rest of the PureMVC app.

    When an `IMediator` is registered with the `IView`,
    the `IView` will call the `IMediator`'s
    `list_notification_interests` method. The `IMediator` will
    return an `Array` of `INotification` names which
    it wishes to be notified about.

    The `IView` will then create an `Observer` object
    encapsulating that `IMediator`'s (`handle_notification`) method
    and register it as an Observer for each `INotification` name returned by
    `list_notification_interests`.

    See Also
    --------
    :class:`puremvc.interfaces.INotification`
    """

    @property
    @abstractmethod
    def mediator_name(self) -> str:
        """
        Get the `IMediator` instance name.

        :return: The `IMediator` instance name
        """
        pass

    @property
    @abstractmethod
    def view_component(self) -> Any:
        """
        Get the `IMediator`'s view component.

        :return: The view component.
        :rtype: Any
        """
        pass

    @view_component.setter
    def view_component(self, value: Any):
        """
        Set the `IMediator`'s view component.

        :param value: The view component
        :type value: Any
        :return: None
        """
        pass

    @abstractmethod
    def list_notification_interests(self) -> [str]:
        """
        List `INotification` interests.

        :return: A list containing strings representing the notification interests.
        :rtype: [str]
        """
        pass

    @abstractmethod
    def handle_notification(self, notification: INotification):
        """
        Handle an `INotification`.

        :param notification: The `INotification` to be handled
        :type notification: INotification
        :return: None
        """
        pass

    @abstractmethod
    def on_register(self):
        """
        Called by the View when the Mediator is registered
        :return: None
        """
        pass

    @abstractmethod
    def on_remove(self):
        """
        Called by the View when the Mediator is removed
        :return: None
        """
        pass
