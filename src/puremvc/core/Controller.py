# Controller.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

import threading
from typing import Dict, Callable

from puremvc.interfaces import IController, ICommand, IView, INotification
from puremvc.patterns.observer import Observer
from .View import View


class Controller(IController):
    """
    A Multiton `IController` implementation.

    In PureMVC, the `Controller` class follows the
    'Command and Controller' strategy, and assumes these
    responsibilities:

    Remembering which `ICommand`s
    are intended to handle which `INotifications`.

    Registering itself as an `IObserver` with
    the `View` for each `INotification`
    that it has an `ICommand` mapping for.

    Creating a new instance of the proper `ICommand`
    to handle a given `INotification` when notified by the `View`.

    Calling the `ICommand`'s `execute`
    method, passing in the `INotification`.

    Your application must register `ICommands` with the
    Controller.

    The simplest way is to subclass `Facade`,
    and use its `initialize_controller` method to add your
    registrations.

    See Also
    --------
    :class:`.View`
    :class:`puremvc.patterns.observer.Observer`
    :class:`puremvc.patterns.observer.Notification`
    :class:`puremvc.patterns.command.SimpleCommand`
    :class:`puremvc.patterns.command.MacroCommand`
    """
    instanceMap: Dict[str, IController] = dict()
    instanceMapLock: threading.Lock = threading.Lock()

    """MULTITON_MSG (str): Multiton error message"""
    MULTITON_MSG = "Controller multiton instance for this key is already constructed!"

    def __init__(self, key: str):
        """
        This `IController` implementation is a Multiton, so you should not
        call the constructor directly, but instead call the static Factory
        method, passing the unique key for this instance
        `Controller.get_instance(multitonKey, lambda k: Controller(k))`

        :param key: The unique key identifier for the Controller instance.
        :type key: str
        :raises Exception: If an instance with the given `key` already exists in the `instanceMap`.
        """
        if Controller.instanceMap.get(key) is not None:
            raise Exception(Controller.MULTITON_MSG)
        self.multitonKey: str = key
        Controller.instanceMap[key] = self
        self.commandMap: Dict[str, Callable[[], ICommand]] = dict()
        self.view = None
        self.initialize_controller()

    def initialize_controller(self):
        """
        Initialize the Multiton `Controller` instance.

        Called automatically by the constructor.

        Note that if you are using a subclass of `View` in your application,
        you should also subclass `Controller` and override the
        `initialize_controller` method in the following way::

            def initialize_controller(self):
                self.view = MyView.get_instance(self.multitonKey, lambda: key: MyView(key))

        :return: None
        """
        self.view: IView = View.get_instance(self.multitonKey, lambda key: View(key))

    @classmethod
    def get_instance(cls, key: str, factory: Callable[[str], IController]) -> IController:
        """
        `Controller` Multiton Factory method.
        
        :param key: The key used to identify the instance.
        :type key: str
        :param factory: A factory function that creates a new instance of IController based on the provided key.
        :type factory: Callable[[str], IController]
        :return: The instance of IController associated with the given key.
        """
        with cls.instanceMapLock:
            if key not in cls.instanceMap:
                cls.instanceMap[key] = factory(key)
        return cls.instanceMap.get(key)

    def register_command(self, notification_name: str, factory: Callable[[], ICommand]):
        """
        Register a particular `ICommand` class as the handler for a particular
        `INotification`.

        If an `ICommand` has already been registered to
        handle `INotification`s with this name, it is no longer
        used, the new `ICommand` is used instead.

        The Observer for the new ICommand is only created if this is the
        first time an ICommand has been registered for this Notification name.

        :param notification_name: The name of the notification.
        :param factory: Callable that returns an instance of ICommand.
        :return: None.
        """
        if self.commandMap.get(notification_name) is None:
            self.view.register_observer(notification_name, Observer(self.execute_command, self))
        self.commandMap[notification_name] = factory

    def execute_command(self, notification: INotification):
        """
        Executes the specified command based on the given notification.

        :param notification: The notification to be executed.
        :type notification: INotification
        :return: None
        """
        factory = self.commandMap.get(notification.name)
        if factory is None:
            return
        command = factory()
        command.initialize_notifier(self.multitonKey)
        command.execute(notification)

    def has_command(self, notification_name: str) -> bool:
        """
        Check if a Command is registered for a given Notification

        :param notification_name: The name of the notification to check in the `commandMap`.
        :type notification_name: str
        :return: True if the `notification_name` exists in the `commandMap`, False otherwise.
        :rtype: bool
        """
        return self.commandMap.get(notification_name) is not None

    def remove_command(self, notification_name: str):
        """
        Remove a previously registered `ICommand` to `INotification` mapping.

        :param notification_name: The name of the notification associated with the command to be removed.
        :type notification_name: str
        :return: None
        """
        if self.has_command(notification_name):
            self.view.remove_observer(notification_name, self)
            del self.commandMap[notification_name]

    @classmethod
    def remove_controller(cls, key: str):
        """
        Remove an IController instance

        :param key: The key to identify the controller instance to be removed.
        :type key: str
        :return: None
        """
        with cls.instanceMapLock:
            del cls.instanceMap[key]
