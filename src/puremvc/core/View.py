# View.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

import threading
from typing import Dict, List, Callable, Any

from puremvc.interfaces import IView, IMediator, IObserver, INotification
from puremvc.patterns.observer import Observer


class View(IView):
    """
    A Multiton `IView` implementation.

    In PureMVC, the `View` class assumes these responsibilities:

    Maintain a cache of `IMediator` instances.

    Provide methods for registering, retrieving, and removing `IMediators`.

    Notifying `IMediators` when they are registered or removed.

    Managing the observer lists for each `INotification` in the application.

    Providing a method for attaching `IObservers` to an `INotification`'s observer list.

    Providing a method for broadcasting an `INotification`.

    Notifying the `IObservers` of a given `INotification` when it broadcast.

    See Also
    --------
    :class:`puremvc.patterns.mediator.Mediator`
    :class:`puremvc.patterns.observer.Observer`
    :class:`puremvc.patterns.observer.Notification`
    """
    instanceMap: Dict[str, IView] = dict()
    instanceMapLock: threading.Lock = threading.Lock()

    """MULTITON_MSG (str): Multiton error message"""
    MULTITON_MSG = "View multiton instance for this key is already constructed!"

    def __init__(self, key: str):
        """
        Constructor.

        This `IView` implementation is a Multiton, so you should not call the
        constructor directly, but instead call the static Multiton Factory
        method `View.get_instance(multiton_key)`

        :param key: The unique key for this View instance.
        :type key: str
        :raises Exception: If an instance with the given `key` already exists in the `instanceMap`.
        """
        if View.instanceMap.get(key) is not None:
            raise Exception(View.MULTITON_MSG)
        self.multitonKey: str = key
        View.instanceMap[key] = self
        self.mediatorMap: Dict[str, IMediator] = dict()
        self.observerMap: Dict[str, List[IObserver]] = dict()
        self.initialize_view()

    @classmethod
    def get_instance(cls, key: str, factory: Callable[[str], IView]) -> IView:
        """
        View Multiton Factory method.

        :param key: The key associated with the desired instance.
        :param factory: A factory function that creates an instance of the desired class using the given key.
        :return: The instance associated with the given key.
        :rtype: IView
        """
        with cls.instanceMapLock:
            if key not in cls.instanceMap:
                cls.instanceMap[key] = factory(key)
        return cls.instanceMap.get(key)

    def initialize_view(self):
        """
        Initialize the Multiton `View` instance.

        Called automatically by the constructor, this is your opportunity to
        initialize the Multiton instance in your subclass without overriding
        the constructor.

        :return: None
        """
        return

    def register_observer(self, notification_name: str, observer: IObserver):
        """
        Register an `IObserver` to be notified of `INotifications` with a given name.

        :param notification_name: The name of the notification to register the observer for.
        :type notification_name: str
        :param observer: The observer object to register.
        :type observer: IObserver
        :return: None
        """
        if notification_name in self.observerMap:
            self.observerMap[notification_name].append(observer)
        else:
            self.observerMap[notification_name] = [observer]

    def notify_observers(self, notification: INotification):
        """
        Notify the `IObservers` for a particular `INotification`.

        All previously attached `IObservers` for this `INotification`'s
        list are notified and are passed a reference to the `INotification` in
        the order in which they were registered.

        :param notification: The notification to be sent to the observers.
        :type notification: INotification
        :return: None
        """
        observers = self.observerMap.get(notification.name)
        if observers:
            for observer in observers[:]:
                observer.notify_observer(notification)

    def remove_observer(self, notification_name: str, notify_context: Any):
        """
        Remove the observer for a given notify_context from an observer list for a given Notification name.

        :param notification_name: The name of the notification to remove the observer from.
        :type notification_name: str
        :param notify_context: The context object of the observer to remove.
        :type notify_context: Any
        :return: None
        """
        observers = self.observerMap.get(notification_name)

        for i, observer in enumerate(observers):
            if observer.compare_notify_context(notify_context):
                observers.pop(i)
                break

        if len(observers) == 0:
            del self.observerMap[notification_name]

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

        :param mediator: The mediator to register.
        :type mediator: IMediator
        :return: None
        """
        # Do not allow re-registration (you must to removeMediator first)
        if self.mediatorMap.get(mediator.mediator_name):
            return
        mediator.initialize_notifier(self.multitonKey)
        self.mediatorMap[mediator.mediator_name] = mediator

        interests = mediator.list_notification_interests()
        if interests:
            observer = Observer(mediator.handle_notification, mediator)
            for interest in interests:
                self.register_observer(interest, observer)
        mediator.on_register()

    def retrieve_mediator(self, mediator_name: str) -> IMediator:
        """
        Retrieve an `IMediator` from the `View`.

        :param mediator_name: The name of the mediator to retrieve.
        :type mediator_name: str
        :return: The mediator with the given name.
        :rtype: IMediator
        """
        return self.mediatorMap.get(mediator_name)

    def has_mediator(self, mediator_name: str) -> bool:
        """
        Check if a Mediator is registered or not

        :param mediator_name: The name of the mediator to check.
        :type mediator_name: str
        :return: Returns True if the mediator exists, False otherwise.
        :rtype: bool
        """
        return self.mediatorMap.get(mediator_name) is not None

    def remove_mediator(self, mediator_name: str) -> IMediator:
        """
        Remove an `IMediator` from the `View`.

        :param mediator_name: The name of the mediator to be removed.
        :type mediator_name: str
        :return: The removed mediator instance.
        :rtype: IMediator
        """
        mediator = self.mediatorMap.get(mediator_name)
        if mediator:
            for interest in mediator.list_notification_interests():
                self.remove_observer(interest, mediator)

            del self.mediatorMap[mediator_name]
            mediator.on_remove()

        return mediator

    @classmethod
    def remove_view(cls, key: str):
        """
        Remove an `IView` instance

        :param key: The key of the view to be removed.
        :return: None
        """
        with cls.instanceMapLock:
            del cls.instanceMap[key]
