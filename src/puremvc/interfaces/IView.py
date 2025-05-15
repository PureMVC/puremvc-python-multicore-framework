# IView.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

from abc import ABC, abstractmethod
from typing import Any

from .IMediator import IMediator
from .INotification import INotification
from .IObserver import IObserver


class IView(ABC):
    """
    The interface definition for a PureMVC View.

    In PureMVC, `IView` implementors assume these responsibilities:

    In PureMVC, the `View` class assumes these responsibilities:

    Maintain a cache of `IMediator` instances.
    Provide methods for registering, retrieving, and removing `IMediators`.
    Managing the observer lists for each `INotification` in the application.
    Providing a method for attaching `IObservers` to an `INotification`'s observer list.
    Providing a method for broadcasting an `INotification`.
    Notifying the `IObservers` of a given `INotification` when it broadcast.

    See Also
    --------
    :class:`puremvc.interfaces.IMediator`
    :class:`puremvc.interfaces.IObserver`
    :class:`puremvc.interfaces.INotification`
    """

    @abstractmethod
    def register_observer(self, notification_name: str, observer: IObserver):
        """
        Register an `IObserver` to be notified of `INotifications` with a
        given name.

        :param notification_name: The name of the `INotifications` to notify this `IObserver` of
        :type notification_name: str
        :param observer: The `IObserver` to register
        :type observer: IObserver
        """
        pass

    @abstractmethod
    def notify_observers(self, notification: INotification):
        """
        Notify the `IObservers` for a particular `INotification`.

        All previously attached `IObservers` for this `INotification`'s
        list are notified and are passed a reference to the `INotification` in
        the order in which they were registered.

        :param notification: The `INotification` to notify `IObservers` of.
        :type notification: INotification
        """
        pass

    @abstractmethod
    def remove_observer(self, notification_name: str, notify_context: Any):
        """
         Remove a group of observers from the observer list for a given Notification name.

         :param notification_name: Which observer list to remove from
         :type notification_name: str
         :param notify_context: Removed the observers with this object as their notify_context
         :type notify_context: Any
         """
        pass

    @abstractmethod
    def register_mediator(self, mediator: IMediator):
        """
          Register an `IMediator` instance with the `View`.

          Registers the `IMediator` so that it can be retrieved by name,
          and further interrogates the `IMediator` for its
          `INotification` interests.

          If the `IMediator` returns any `INotification`
          names to be notified about, an `Observer` is created encapsulating
          the `IMediator` instance's `handleNotification` method
          and registering it as an `Observer` for all `INotifications` the
          `IMediator` is interested in.

          :param mediator: A reference to the `IMediator` instance
          """
        pass

    @abstractmethod
    def retrieve_mediator(self, mediator_name: str) -> IMediator:
        """
        Retrieve an `IMediator` from the `View`.

        :param mediator_name: The name of the `IMediator` instance to retrieve.
        :type mediator_name: str
        :return: The `IMediator` instance previously registered with the given `mediatorName`.
        :rtype: IMediator
        """
        pass

    @abstractmethod
    def has_mediator(self, mediator_name: str) -> bool:
        """
        Check if a Mediator is registered or not.

        :param mediator_name: Name of the `IMediator`
        :type mediator_name: str
        :return: whether a Mediator is registered with the given `mediatorName`.
        :rtype: bool
        """
        pass

    @abstractmethod
    def remove_mediator(self, mediator_name: str) -> IMediator:
        """
         Remove an `IMediator` from the `View`.

         :param mediator_name: Name of the `IMediator` instance to be removed.
         :type mediator_name: str
         :return: the `IMediator` that was removed from the `View`
         :rtype: IMediator
         """
        pass
