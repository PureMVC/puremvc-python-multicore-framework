# IFacade.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

from abc import ABC, abstractmethod
from typing import Callable

from .ICommand import ICommand
from .IMediator import IMediator
from .INotification import INotification
from .INotifier import INotifier
from .IProxy import IProxy


class IFacade(INotifier, ABC):
    """
    The interface definition for a PureMVC Facade.

    The Facade Pattern suggests providing a single class to act as a central point of communication
    for a subsystem.

    In PureMVC, the Facade acts as an interface between the core MVC actors (Model, View, Controller) and
    the rest of your application.

    :class:`puremvc.interfaces.IModel`
    :class:`puremvc.interfaces.IView`
    :class:`puremvc.interfaces.IController`
    :class:`puremvc.interfaces.ICommand`
    :class:`puremvc.interfaces.INotification`
    """

    @abstractmethod
    def register_proxy(self, proxy: IProxy):
        """
        Register a `Proxy` with the `Model` by name.

        :param proxy: The `IProxy` to be registered with the `Model`.
        :type proxy: IProxy
        :return: None
        """
        pass

    @abstractmethod
    def retrieve_proxy(self, proxy_name: str) -> IProxy:
        """
        Retrieve a `IProxy` from the `Model` by name.

        :param proxy_name: The name of the `IProxy` instance to be retrieved.
        :type proxy_name: str
        :return: the `IProxy` previously registered by `proxyName` with the `Model`.
        """
        pass

    @abstractmethod
    def remove_proxy(self, proxy_name: str) -> IProxy:
        """
        Remove an `IProxy` instance from the `Model` by name.

        :param proxy_name: The `IProxy` to remove from the `Model`.
        :type proxy_name: str
        :return: the `IProxy` that was removed from the `Model`
        :rtype: IProxy
        """
        pass

    @abstractmethod
    def has_proxy(self, proxy_name: str) -> bool:
        """
        Check if a Proxy is registered

        :param proxy_name: The name of the proxy to check.
        :type proxy_name: str
        :return: True if the proxy is currently registered, False otherwise.
        :rtype: bool
        """
        pass

    @abstractmethod
    def register_command(self, notification_name: str, factory: Callable[[], ICommand]):
        """
        Register an `ICommand` with the `Controller`.

        :param notification_name: The name of the `INotification` to associate the `ICommand` with.
        :type notification_name: str
        :param factory: A callable factory function that creates an instance of `ICommand`.
        :type factory: Callable[[], ICommand]
        :return: None
        """
        pass

    @abstractmethod
    def has_command(self, notification_name: str) -> bool:
        """
        Check if a Command is registered for a given `Notification`.

        :param notification_name: The name of the notification to check.
        :type notification_name: str
        :return: True if a command exists for the given `notification_name`, False otherwise.
        """
        pass

    @abstractmethod
    def remove_command(self, notification_name: str):
        """
        Remove a previously registered `ICommand` to `INotification` mapping from the Controller.

        :param notification_name: The name of the `INotification` to remove the `ICommand` mapping for
        :type notification_name: str
        :return: None
        """
        pass

    @abstractmethod
    def register_mediator(self, mediator: IMediator):
        """
        Register an `IMediator` instance with the `View`.

        :param mediator: A reference to the `IMediator` instance
        :type mediator: IMediator
        :return: None
        """
        pass

    @abstractmethod
    def retrieve_mediator(self, mediator_name: str) -> IMediator:
        """
        Retrieve an `IMediator` instance from the `View`.

        :param mediator_name: The name of the `IMediator` instance to retrieve
        :type mediator_name: str
        :return: The mediator object found, of type IMediator.
        """
        pass

    @abstractmethod
    def has_mediator(self, mediator_name: str) -> bool:
        """
        Check if a Mediator is registered or not

        :param mediator_name: The name of the mediator to check for.
        :type mediator_name: str
        :return: True if the mediator exists, False otherwise.
        """
        pass

    @abstractmethod
    def remove_mediator(self, mediator_name: str) -> IMediator:
        """
        Remove a `IMediator` instance from the `View`.

        :param mediator_name: name of the `IMediator` instance to be removed.
        :type mediator_name: str
        :return: The `IMediator` instance previously registered with the given `mediator_name`.
        """
        pass

    @abstractmethod
    def notify_observers(self, notification: INotification):
        """
        Notify `Observer`

        :param notification: The `INotification` to have the `View` notify `Observers` of.
        :type notification: INotification
        :return: None
        """
        pass
