# Facade.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

import threading
from typing import Dict, Callable, Any

from puremvc.core import Controller, Model, View
from puremvc.interfaces import IFacade, INotification, ICommand, IProxy, IMediator, IController, IModel, IView
from puremvc.patterns.observer import Notification


class Facade(IFacade):
    """
    A base Multiton `IFacade` implementation.

    In PureMVC, the `Facade` class assumes these responsibilities:

    Initializing the `Model`, `View` and `Controller` Singletons.

    Providing all the methods defined by the `IModel, IView, & IController` interfaces.

    Providing the ability to override the specific `Model`, `View` and `Controller` Singletons created.

    Providing a single point of contact to the application for registering `Commands` and notifying `Observers`

    See Also
    --------
    :class:`puremvc.core.Model`
    :class:`puremvc.core.View`
    :class:`puremvc.core.Controller`
    :class:`puremvc.patterns.observer.Notification`
    :class:`puremvc.patterns.mediator.Mediator`
    :class:`puremvc.patterns.proxy.Proxy`
    :class:`puremvc.patterns.command.SimpleCommand`
    :class:`puremvc.patterns.command.MacroCommand`
    """
    instanceMap: Dict[str, IFacade] = dict()
    instanceMapLock = threading.Lock()

    """MULTITON_MSG (str): Multiton error message"""
    MULTITON_MSG = "Facade instance for this Multiton key already constructed!"

    def __init__(self, key: str):
        """
        Constructor.

        This `IFacade` implementation is a Multiton, so you should not call
        the constructor directly, but instead call the static Factory method,
        passing the unique key for this instance `Facade.get_instance(multitonKey, lambda k: Facade(k))`

        :param key: The Multiton key for the Facade instance.
        :type key: str
        :raises Exception: If a Facade instance has already been constructed with the same Multiton key.
        """
        if Facade.instanceMap.get(key) is not None:
            raise Exception(Facade.MULTITON_MSG)
        self.multitonKey = None
        self.controller = None
        self.model = None
        self.view = None
        self.initialize_notifier(key)
        Facade.instanceMap[key] = self
        self.initialize_facade()

    def initialize_facade(self):
        """
        Initialize the Multiton `Facade` instance.

        Called automatically by the constructor. Override in your subclass to
        do any subclass specific initializations. Be sure to call
        `super.initialize_facade()`, though.

        :return: None
        """
        self.initialize_model()
        self.initialize_controller()
        self.initialize_view()

    @classmethod
    def get_instance(cls, key: str, factory: Callable[[str], IFacade]) -> IFacade:
        """
        Facade Multiton Factory method

        :param key: The key used to identify the Multiton instance
        :type key: str
        :param factory: A callable object that takes a string parameter and returns an instance of the IFacade interface
        :type factory: Callable[[str], IFacade]
        :return: the Multiton instance of the Facade
        """
        with cls.instanceMapLock:
            if key not in cls.instanceMap:
                cls.instanceMap[key] = factory(key)
        return cls.instanceMap.get(key)

    def initialize_controller(self):
        """
        Initialize the `Controller`.

        Called by the `initialize_facade` method.
        Override this method in your subclass of `Facade`
        if one or both of the following are true:

        You wish to initialize a different `IController`.
        You have `Commands` to register with the `Controller` at startup.

        If you don't want to initialize a different `IController`,
        call `super.initialize_controller()` at the beginning of your method, then register `Proxy`.

        Note: This method is rarely overridden; in practice, you are more
        likely to use a `Command` to create and register `Proxy`s
        with the `Model`, since `Proxy` with mutable data will likely
        need to send `INotification` and thus will likely want to fetch a reference to
        the `Facade` during their construction.

        :return: None
        """
        self.controller: IController = Controller.get_instance(self.multitonKey, lambda k: Controller(k))

    def initialize_model(self):
        """
        Initialize the `Model`.

        Called by the `initialize_facade` method.
        Override this method in your subclass of `Facade`
        if one or both of the following are true:

        You wish to initialize a different `IModel`.

        You have `Proxy` to register with the Model that does not
        retrieve a reference to the Facade at construction time.

        If you don't want to initialize a different `IModel`,
        call `super.initialize_model()` at the beginning of your
        method, then register `Proxy`.

        Note: This method is rarely overridden; in practice, you are more
        likely to use a `Command` to create and register `Proxy` with the
        `Model`, since `Proxy` with mutable data will likely need to send
        `INotification` and thus will likely want to fetch a reference to
        the `Facade` during their construction.

        :return: None
        """
        self.model: IModel = Model.get_instance(self.multitonKey, lambda k: Model(k))

    def initialize_view(self):
        """
        Initialize the `View`.

        Called by the `initialize_facade` method.
        Override this method in your subclass of `Facade`
        if one or both of the following are true:

        You wish to initialize a different `IView`.

        You have `Observers` to register with the `View`

        If you don't want to initialize a different `IView`,
        call `super.initialize_view()` at the beginning of your
        method, then register `IMediator` instances.

        Note: This method is rarely overridden; in practice, you are more
        likely to use a `Command` to create and register `Mediator` with the
        `View`, since `IMediator` instances will need to send
        `INotification` and thus will likely want to fetch a reference
        to the `Facade` during their construction.

        :return: None
        """
        self.view: IView = View.get_instance(self.multitonKey, lambda k: View(k))

    def register_command(self, notification_name: str, factory: Callable[[str], ICommand]):
        """
        Register an `ICommand` with the `Controller` by Notification name.

        :param notification_name: The name of the `INotification` to associate the `ICommand` with
        :type notification_name: str
        :param factory: A factory function that will be used to create instances of the `ICommand`.
        :type factory: Callable[[str], ICommand]
        :return: None
        """
        self.controller.register_command(notification_name, factory)

    def has_command(self, notification_name: str) -> bool:
        """
        Check if a Command is registered for a given Notification

        :param notification_name: The name of the `INotification`
        :type notification_name: str
        :return: `True` if a command is registered for the notification, `False` otherwise.
        """
        return self.controller.has_command(notification_name)

    def remove_command(self, notification_name: str):
        """
        Remove a previously registered `ICommand` to `INotification` mapping from the Controller.

        :param notification_name: The name of the `INotification` to remove the `ICommand` mapping for.
        :type notification_name: str
        :return: None
        """
        self.controller.remove_command(notification_name)

    def register_proxy(self, proxy: IProxy):
        """
        Register an `IProxy` with the `Model` by name.

        :param proxy: The `IProxy` instance to be registered with the `Model`.
        :type proxy: IProxy
        :return: None.
        """
        self.model.register_proxy(proxy)

    def retrieve_proxy(self, proxy_name: str) -> IProxy:
        """
        Retrieve an `IProxy` from the `Model` by name.

        :param proxy_name: The name of the proxy to be retrieved.
        :type proxy_name: str
        :return: the `IProxy` instance previously registered with the given `proxyName`.
        """
        return self.model.retrieve_proxy(proxy_name)

    def has_proxy(self, proxy_name: str) -> bool:
        """
        Check if a Proxy is registered

        :param proxy_name: The name of the `IProxy`
        :type proxy_name: str
        :return: True if the proxy exists, False otherwise.
        """
        return self.model.has_proxy(proxy_name)

    def remove_proxy(self, proxy_name: str) -> IProxy:
        """
        Remove an `IProxy` from the `Model` by name.

        :param proxy_name: The `IProxy` to remove from the `Model`.
        :type proxy_name: IProxy
        :return: the `IProxy` that was removed from the `Model`
        """
        return self.model.remove_proxy(proxy_name)

    def register_mediator(self, mediator: IMediator):
        """
        Register a `IMediator` with the `View`.

        :param mediator: A reference to the `IMediator`
        :type mediator: IMediator
        :return: None
        """
        self.view.register_mediator(mediator)

    def retrieve_mediator(self, mediator_name: str) -> IMediator:
        """
        Retrieve an `IMediator` from the `View`.

        :param mediator_name: The name of the `IMediator`
        :type mediator_name: str
        :return: the `IMediator` previously registered with the given `mediator_name`.
        :rtype: IMediator
        """
        return self.view.retrieve_mediator(mediator_name)

    def has_mediator(self, mediator_name: str) -> bool:
        """
        Check if a Mediator is registered or not

        :param mediator_name: The name of the `IMediator`
        :type mediator_name: str
        :return: True if the mediator with the specified name exists in the view, False otherwise.
        :rtype: bool
        """
        return self.view.has_mediator(mediator_name)

    def remove_mediator(self, mediator_name: str) -> IMediator:
        """
        Remove an `IMediator` from the `View`.

        :param mediator_name: Name of the `IMediator` to be removed.
        :type mediator_name: str
        :return: The `IMediator` that was removed from the `View`
        :rtype: IMediator
        """
        return self.view.remove_mediator(mediator_name)

    def send_notification(self, notification_name: str, body: Any = None, _type: str = None):
        """
        Create and send an `INotification`.

        Keeps us from having to construct new notification
        instances in our implementation code.

        :param notification_name: The name of the notification.
        :type notification_name: str
        :param body: The body of the notification (optional).
        :type body: Any
        :param _type: The type of the notification (optional).
        :type _type: str
        :return: None
        """
        self.notify_observers(Notification(notification_name, body, _type))

    def notify_observers(self, notification: INotification):
        """
        Notify `Observer`.

        This method is left public mostly for backward
        compatibility, and to allow you to send custom
        notification classes using the facade.

        Usually you should just call sendNotification
        and pass the parameters, never having to
        construct the notification yourself.

        :param notification: The `INotification` to have the `View` notify `Observers` of.
        :type notification: INotification
        :return: None
        """
        self.view.notify_observers(notification)

    def initialize_notifier(self, key: str):
        """
        Set the Multiton key for this facade instance.

        Not called directly, but instead from the constructor when getInstance
        is invoked. It is necessary to be public to implement
        INotifier.

        :param key: A string representing the key for the notifier.
        :type key: str
        :return: None
        """
        self.multitonKey = key

    @classmethod
    def has_core(cls, key: str) -> bool:
        """
        Check if a Core is registered or not

        :param key: The multiton key for the Core in question
        :type key: str
        :return: True if an instance with the specified key exists, False otherwise.
        """
        return cls.instanceMap.get(key) is not None

    @classmethod
    def remove_core(cls, key: str):
        """
        Remove a Core.

        Remove the Model, View, Controller and Facade instances for the given
        key.

        :param key: The key representing the core components to be removed.
        :type key: str
        :return: None
        """
        if cls.instanceMap.get(key) is None:
            return
        Model.remove_model(key)
        View.remove_view(key)
        Controller.remove_controller(key)
        del cls.instanceMap[key]
