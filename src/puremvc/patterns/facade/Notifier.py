# Notifier.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

from typing import Any

from puremvc.interfaces import IFacade, INotifier
from puremvc.patterns.facade import Facade


class Notifier(INotifier):
    """
    A Base `INotifier` implementation.

    `MacroCommand, Command, Mediator` and `Proxy`
    all have a need to send `Notifications`.

    The `INotifier` interface provides a common method called
    `sendNotification` that relieves implementation code of
    the necessity to actually construct `Notifications`.

    The `Notifier` class, which all the above-mentioned classes
    extend, provides an initialized reference to the `Facade`
    Multiton, which is required for the convenience method
    for sending `Notifications`, but also eases implementation as these
    classes have frequent `Facade` interactions and usually require
    access to the facade anyway.

    NOTE: In the MultiCore version of the framework, there is one caveat to
    notifiers, they cannot send notifications or reach the facade until they
    have a valid multitonKey.

    The multitonKey is set:

    - on a Command when it is executed by the Controller
    - on a Mediator is registered with the View
    - on a Proxy is registered with the Model.

    See Also
    --------
    :class:`puremvc.patterns.proxy.Proxy`
    :class:`puremvc.patterns.facade.Facade`
    :class:`puremvc.patterns.mediator.Mediator`
    :class:`puremvc.patterns.command.MacroCommand`
    :class:`puremvc.patterns.command.SimpleCommand`
    """

    """Multiton error message"""
    MULTITON_MSG = "multitonKey for this Notifier not yet initialized!"

    def __init__(self):
        """Initialise the `INotifier` instance with an empty multiton key"""
        self.multitonKey = None

    def send_notification(self, notification_name: str, body: Any = None, note_type: str = None):
        """
        Create and send an `INotification`.

        Keeps us from having to construct new INotification instances in our
        implementation code.

        :param notification_name: The name of the notification to be sent.
        :type notification_name: str
        :param body: The body of the notification (optional). Default is None.
        :type body: Any, optional
        :param note_type: The type of the notification (optional). Default is None.
        :type note_type: str, optional
        :return: None
        """
        self.facade.send_notification(notification_name, body, note_type)

    def initialize_notifier(self, key: str):
        """
        Initialize this INotifier instance.

        This is how a Notifier gets its multitonKey. Calls to sendNotification
        or to access the facade will fail until after this method has been
        called.

        Mediators, Commands or Proxies may override this method in order to
        send notifications or access the Multiton Facade instance as soon as
        possible. They CANNOT access the facade in their constructors, since
        this method will not yet have been called.

        :param key: The multitonKey for this INotifier to use
        :type key: str
        :return: None
        """
        self.multitonKey = key

    @property
    def facade(self) -> IFacade:
        """
        Return the Multiton Facade instance

        :return: The instance of IFacade.
        :rtype: IFacade
        """
        if self.multitonKey is None:
            raise Exception(self.MULTITON_MSG)
        return Facade.get_instance(self.multitonKey, lambda key: Facade(key))
