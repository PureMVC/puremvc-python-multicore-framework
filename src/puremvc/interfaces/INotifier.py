# INotifier.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

from abc import abstractmethod, ABC
from typing import Any


class INotifier(ABC):
    """
    The interface definition for a PureMVC Notifier.

    `MacroCommand, Command, Mediator` and `Proxy`
    all have a need to send `Notifications`.

    The `INotifier` interface provides a common method called
    `send_notification` that relieves implementation code of
    the necessity to actually construct `Notifications`.

    The `Notifier` class, which all the above-mentioned classes
    extend, also provides an initialized reference to the `Facade`
    Singleton, which is required for the convenience method
    for sending `Notifications`, but also eases implementation as these
    classes have frequent `Facade` interactions and usually require
    access to the facade anyway.

    See Also
    --------
    :class:`puremvc.interfaces.IFacade`
    :class:`puremvc.interfaces.INotification`
    """

    @abstractmethod
    def send_notification(self, notification_name: str, body: Any = None, _type: str = None):
        """
        Send a `INotification`.

        Convenience method to prevent having to construct new notification
        instances in our implementation code.

        @param notification_name: The name of the notification to send
        @type notification_name: str
        @param body: the body of the notification (optional)
        @type body: Any
        @param _type: the type of the notification (optional)
        @type _type: str
        """
        pass

    @abstractmethod
    def initialize_notifier(self, key: str):
        """
        Initialise this `INotifier` instance.

        This is how a `Notifier` gets its `multiton_key`. Calls to `send_notification`
        or to access the facade will fail until after this method has been
        called.

        @param key: The `multiton_key` for this `INotifier` to use
        """
        pass
