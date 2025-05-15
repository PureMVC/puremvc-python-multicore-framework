# Mediator.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

from typing import Any

from puremvc.interfaces import IMediator, INotification
from puremvc.patterns.facade import Notifier


class Mediator(Notifier, IMediator):
    """
    A base `IMediator` implementation.

    See Also
    --------
    :class:`puremvc.core.View`
    """

    """NAME (str): The name of the `Mediator`"""
    NAME = "Mediator"

    def __init__(self, mediator_name: str = None, view_component: Any = None):
        """
        Constructor

        Typically, a `Mediator` will be written to serve
        one specific control or group controls and so,
        will not have a need to be dynamically named.

        :param mediator_name: A string representing the name of the mediator. If not provided, it defaults to self.NAME.
        :type mediator_name: str
        :param view_component: Any object representing the view component. If not provided, it defaults to None.
        :type view_component: Any
        """
        super().__init__()
        self._mediator_name = self.NAME if mediator_name is None else mediator_name
        self._view_component = view_component

    @property
    def mediator_name(self) -> str:
        """
        Get the name of the `Mediator`.

        :return: The name of the mediator.
        :rtype: str
        """
        return self._mediator_name

    @property
    def view_component(self) -> Any:
        """
        Get the `Mediator` view component.

        :return: The view component.
        :rtype: Any
        """
        return self._view_component

    @view_component.setter
    def view_component(self, value: Any):
        """
        Set the `IMediator` view component.

        :param value: The view component
        :type value: Any
        :return: None
        """
        self._view_component = value

    def list_notification_interests(self) -> [str]:
        """
        List the `INotification` names this
        `Mediator` is interested in being notified of.

        :return: List the list of `INotification` names
        :rtype: List[str]
        """
        return []

    def handle_notification(self, notification: INotification):
        """
        Handle `INotification`.

        Typically, this will be handled in an if/else statement,
        with one 'comparison' entry per `INotification`
        the `Mediator` is interested in.

        :param notification: The notification to be handled.
        :type notification: INotification
        :return: None
        """
        return

    def on_register(self):
        """Called by the View when the Mediator is registered"""
        return

    def on_remove(self):
        """Called by the View when the Mediator is removed"""
        return
