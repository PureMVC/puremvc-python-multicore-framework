# Observer.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

from typing import Any, Callable, Optional

from puremvc.interfaces import IObserver, INotification


class Observer(IObserver):
    """
    A base `IObserver` implementation.

    An `Observer` is an object that encapsulates information
    about an interested object with a method that should
    be called when a particular `INotification` is broadcast.

    In PureMVC, the `Observer` class assumes these responsibilities:

    Encapsulate the notification (callback) method of the interested object.

    Encapsulate the notification context (this) of the interested object.

    Provide methods for setting the notification method and context.

    Provide a method for notifying the interested object.

    See Also
    --------
    :class:`puremvc.core.View`
    :class:`puremvc.patterns.observer.Notification`
    """

    def __init__(self, notify_method: Optional[Callable[[INotification], None]] = None, notify_context: object = None) -> None:
        """
        Constructor.

        The notification method on the interested object should take
        one parameter of type `INotification`

        :param notify_method: The notification method of the interested object
        :type notify_method: Optional[Callable[[INotification], None]]
        :param notify_context: the notification context of the interested object
        :type notify_context: object
        """
        self._notify_method: Optional[Callable[[INotification], None]] = notify_method
        self._notify_context: object = notify_context

    @property
    def notify_method(self) -> Optional[Callable[[INotification], None]]:
        """
        Get the notification method.

        :return: The notify method.
        :rtype: Optional[Callable[[INotification], None]
        """
        return self._notify_method

    @notify_method.setter
    def notify_method(self, value: Callable[[INotification], None]) -> None:
        """
        Set the notification context.

        :param value: A callable function that takes an INotification object as its parameter.
        :type value: Callable[[INotification], None]
        :return: None
        """
        self._notify_method = value

    @property
    def notify_context(self) -> object:
        """
        Get the notification context.

        :return: The notify context.
        :rtype: object
        """
        return self._notify_context

    @notify_context.setter
    def notify_context(self, value: object) -> None:
        """
        Set the notification context.

        :param value: The notification context (self) of the interested object.
        :type value: object
        :return: None
        """
        self._notify_context = value

    def notify_observer(self, notification: INotification) -> None:
        """
        Notify the interested object.

        :param notification: The `INotification` to pass to the interested
        :type notification: INotification
        :return: None
        """
        if self._notify_method is not None:
            self._notify_method(notification)

    def compare_notify_context(self, obj: object) -> bool:
        """
        Compare an object to the notification context.

        :param obj: The object to compare with the notify context.
        :type obj: object
        :return: True if the given object is equal to the notify context, False otherwise.
        :rtype: bool
        """
        return obj == self._notify_context
