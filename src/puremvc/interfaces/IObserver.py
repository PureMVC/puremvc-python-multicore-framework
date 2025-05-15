# IObserver.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

from abc import ABC, abstractmethod
from typing import Any, Callable

from .INotification import INotification


class IObserver(ABC):
    """
    The interface definition for a PureMVC Observer.

    In PureMVC, `IObserver` implementors assume these responsibilities:

    Encapsulate the notification (callback) method of the interested object.

    Encapsulate the notification context of the interested object.

    Provide methods for setting the interested object notification method and context.

    Provide a method for notifying the interested object.

    PureMVC does not rely upon underlying event
    models such as the one provided with Flash,
    and ActionScript 3 does not have an inherent
    event model.

    The Observer Pattern as implemented within
    PureMVC exists to support event driven communication
    between the application and the actors of the
    MVC triad.

    An Observer is an object that encapsulates information
    about an interested object with a notification method that
    should be called when an `INotification` is broadcast. The Observer then
    acts as a proxy for notifying the interested object.

    Observers can receive `Notification`s by having their
    `notify_observer` method invoked, passing
    in an object implementing the `INotification` interface, such
    as a subclass of `Notification`.

    See Also
    --------
    :class:`puremvc.interfaces.IView`
    :class:`puremvc.interfaces.INotification`

    """

    @property
    @abstractmethod
    def notify_method(self) -> Callable[[INotification], None]:
        """
        Set the notification method.

        The notification method should take one parameter of type `INotification`

        :return: The notification (callback) method of the interested object
        :rtype: Callable[[INotification], None]
        """
        pass

    @notify_method.setter
    @abstractmethod
    def notify_method(self, value: Callable[[INotification], None]):
        """
        Set the notification context.

        :param value: The notification context (self) of the interested
        :type value: Callable[[INotification, None]
        """
        pass

    @property
    @abstractmethod
    def notify_context(self) -> Any:
        """
        Get the notify_context.

        :return: notify context
        :rtype: Any
        """
        pass

    @notify_context.setter
    @abstractmethod
    def notify_context(self, value: Any):
        """
        Sets the value of the `notify_context` attribute.

        :param value: The value to be set for the `notify_context` attribute.
        :type value: Any
        :return: None
        """
        pass

    @abstractmethod
    def notify_observer(self, notification: INotification):
        """
        Notify the interested object.

        :param notification: The `INotification` to pass to the interested object's notification method
        :type notification: INotification
        """
        pass

    @abstractmethod
    def compare_notify_context(self, obj: Any) -> bool:
        """
        Compare the given object to the notification context object.

        :param obj: The object to compare.
        :type obj: Any
        :return: boolean indicating if the notification context and the object are the same.
        """
        pass
