# -*- coding: utf-8 -*-
"""
 PureMVC Python Port by Toby de Havilland <toby.de.havilland@puremvc.org>
 PureMVC Python Port by Daniele Esposti <expo@expobrain.net>
 PureMVC - Copyright(c) 2006-08 Futurescale, Inc., Some rights reserved.
 Your reuse is governed by the Creative Commons Attribution 3.0 License
"""

from puremvc import MultitonError
import puremvc.interfaces
import puremvc.patterns.observer


class Controller(puremvc.interfaces.IController):
    """
    A Multiton C{IController} implementation.

    In PureMVC, the C{Controller} class follows the
    'Command and Controller' strategy, and assumes these
    responsibilities:

    Remembering which C{ICommand}s
    are intended to handle which C{INotifications}.

    Registering itself as an C{IObserver} with
    the C{View} for each C{INotification}
    that it has an C{ICommand} mapping for.

    Creating a new instance of the proper C{ICommand}
    to handle a given C{INotification} when notified by the C{View}.

    Calling the C{ICommand}'s C{execute}
    method, passing in the C{INotification}.

    Your application must register C{ICommands} with the
    Controller.

    The simplest way is to subclass C{Facade},
    and use its C{initializeController} method to add your
    registrations.

    @see: L{View<puremvc.core.view.View>}
    @see: L{Observer<puremvc.patterns.observer.Observer>}
    @see: L{Notification<puremvc.patterns.observer.Notification>}
    @see: L{SimpleCommand<puremvc.patterns.command.SimpleCommand>}
    @see: L{MacroCommand<puremvc.patterns.command.MacroCommand>}
    """

    """Singleton instance"""
    instanceMap = {}

    """Multiton error message"""
    MULTITON_MSG = ("Controller multiton instance for this key "
                     "is already constructed!")

    @classmethod
    def removeController(cls, key):
        """
        Remove an IController instance

        @param key: of IController instance to remove
        """
        cls.instanceMap.pop(key, None)

    def __init__(self, key):
        """
        Constructor.

        This C{IController} implementation is a Multiton, so you should not
        call the constructor directly, but instead call the static Factory
        method, passing the unique key for this instance
        C{Controller.getInstance( multitonKey )}

        @raise MultitonError: if instance for this Multiton key has already
        been constructed
        """

        """Local reference to View"""
        self.view = None

        """Mapping of Notification names to Command Classes"""
        self.commandMap = {}

        """The Multiton Key for this Core"""
        self.multitonKey = key

        if self.instanceMap.get(key) is not None:
            raise MultitonError(self.MULTITON_MSG)

        self.instanceMap[key] = self

        self.initializeController()

    def initializeController(self):
        """
        Initialize the Multiton C{Controller} instance.

        Called automatically by the constructor.

        Note that if you are using a subclass of C{View} in your application,
        you should <i>also</i> subclass C{Controller} and override the
        C{initializeController} method in the following way::

            // ensure that the Controller is talking to my IView implementation
            public function initializeController(  ) : void
            {
                view = MyView.getInstance();
            }

        @return: void
        """
        self.view = View.getInstance(self.multitonKey)

    @classmethod
    def getInstance(cls, key):
        """
        C{Controller} Multiton Factory method.

        @return: the Multiton instance of C{Controller}
        """
        if cls.instanceMap.get(key) is None:
            cls.instanceMap[key] = Controller(key)

        return cls.instanceMap[key]

    def executeCommand(self, note):
        """
        If an C{ICommand} has previously been registered
        to handle a the given C{INotification}, then it is executed.

        @param note: an C{INotification}
        """
        commandClassRef = self.commandMap.get(note.getName())
        if commandClassRef is None:
            return

        commandInstance = commandClassRef()

        commandInstance.initializeNotifier(self.multitonKey)
        commandInstance.execute(note)

    def registerCommand(self, notificationName, commandClassRef):
        """
        Register a particular C{ICommand} class as the handler for a particular
        C{INotification}.

        If an C{ICommand} has already been registered to
        handle C{INotification}s with this name, it is no longer
        used, the new C{ICommand} is used instead.

        The Observer for the new ICommand is only created if this the
        first time an ICommand has been registered for this Notification name.

        @param notificationName: the name of the C{INotification}
        @param commandClassRef: the C{Class} of the C{ICommand}
        """
        if self.commandMap.get(notificationName) is None:
            self.view.registerObserver(notificationName, puremvc.patterns.observer.Observer(self.executeCommand, self))

        self.commandMap[notificationName] = commandClassRef

    def hasCommand(self, notificationName):
        """
        Check if a Command is registered for a given Notification

        @param notificationName: the name of the C{INotification}
        @return: whether a Command is currently registered for the given C{notificationName}.
        """
        return self.commandMap.get(notificationName) is not None

    def removeCommand(self, notificationName):
        """
        Remove a previously registered C{ICommand} to C{INotification} mapping.

        @param notificationName: the name of the C{INotification} to remove the
        C{ICommand} mapping for
        """
        if self.hasCommand(notificationName):
            self.view.removeObserver(notificationName, self)
            del self.commandMap[notificationName]


class Model(puremvc.interfaces.IModel):
    """
    A Multiton C{IModel} implementation.

    In PureMVC, the C{Model} class provides access to model objects (Proxies)
    by named lookup.

    The C{Model} assumes these responsibilities:

        - Maintain a cache of C{IProxy} instances.
        - Provide methods for registering, retrieving, and removing C{IProxy}
          instances.

    Your application must register C{IProxy} instances with the C{Model}.
    Typically, you use an C{ICommand} to create and register C{IProxy}
    instances once the C{Facade} has initialized the Core actors.

    @see: L{Proxy<puremvc.patterns.proxy.Proxy>}
    @see: L{IProxy<puremvc.interfaces.IProxy>}
    """

    """Singleton instance"""
    instanceMap = {}

    """Multiton error message"""
    MULTITON_MSG = ("Model multiton instance for this key "
                     "is already constructed!")

    @classmethod
    def removeModel(cls, key):
        """
        Remove an IModel instance.

        @param key: of IModel instance to remove
        """
        cls.instanceMap.pop(key, None)

    @classmethod
    def getInstance(cls, key):
        """
        C{Model} Multiton Factory method.

        @return: the instance for this Multiton key
        """
        if cls.instanceMap.get(key) is None:
            cls.instanceMap[key] = Model(key)

        return cls.instanceMap[key]

    def __init__(self, key):
        """
        Constructor.

        This C{IModel} implementation is a Multiton, so you should not call the
        constructor directly, but instead call the static Multiton Factory
        method C{Model.getInstance( multitonKey )}

        @raise MultitonError: if instance for this Multiton key instance has
        already been constructed
        """

        """Mapping of proxyNames to IProxy instances"""
        self.proxyMap = {}

        """The Multiton Key for this Core"""
        self.multitonKey = None

        if self.instanceMap.get(key) is not None:
            raise MultitonError(self.MULTITON_MSG)

        self.multitonKey = key
        self.instanceMap[key] = self
        self.proxyMap = {}

        self.initializeModel()

    def initializeModel(self):
        """
        Initialize the C{Model} instance.

        Called automatically by the constructor, this is your opportunity to
        initialize the Singleton instance in your subclass without overriding
        the constructor.
        """
        return

    def registerProxy(self, proxy):
        """
        Register an C{IProxy} with the C{Model}.

        @param proxy: an C{IProxy} to be held by the C{Model}.
        """
        proxy.initializeNotifier(self.multitonKey)
        self.proxyMap[proxy.getProxyName()] = proxy
        proxy.onRegister()

    def retrieveProxy(self, proxyName):
        """
        Retrieve an C{IProxy} from the C{Model}.

        @param proxyName: the name of the C{IProxy}
        @return: the C{IProxy} instance previously registered with the given C{proxyName}.
        """
        return self.proxyMap.get(proxyName)

    def hasProxy(self, proxyName):
        """
        Check if a Proxy is registered

        @param proxyName: the name of the C{IProxy}
        @return: whether a Proxy is currently registered with the given C{proxyName}.
        """
        return self.proxyMap.get(proxyName) is not None

    def removeProxy(self, proxyName):
        """
        Remove an C{IProxy} from the C{Model}.

        @param proxyName: name of the C{IProxy} instance to be removed.
        @return: the C{IProxy} that was removed from the C{Model}
        """
        proxy = self.proxyMap.get(proxyName)
        if proxy:
            del self.proxyMap[proxyName]
            proxy.onRemove()
        return proxy


class View(puremvc.interfaces.IView):
    """
    A Multiton C{IView} implementation.

    In PureMVC, the C{View} class assumes these responsibilities:

    Maintain a cache of C{IMediator} instances.

    Provide methods for registering, retrieving, and removing C{IMediators}.

    Notifiying C{IMediators} when they are registered or removed.

    Managing the observer lists for each C{INotification} in the application.

    Providing a method for attaching C{IObservers} to an C{INotification}'s observer list.

    Providing a method for broadcasting an C{INotification}.

    Notifying the C{IObservers} of a given C{INotification} when it broadcast.


    @see: L{Mediator<puremvc.patterns.mediator.Mediator>}
    @see: L{Observer<puremvc.patterns.observer.Observer>}
    @see: L{Notification<puremvc.patterns.observer.Notification>}
    """

    """Singleton instance"""
    instanceMap = {}

    """Multiton error message"""
    MULTITON_MSG = ("View multiton instance for this key "
                     "is already constructed!")

    def __init__(self, key):
        """
        Constructor.

        This C{IView} implementation is a Multiton, so you should not call the
        constructor directly, but instead call the static Multiton Factory
        method C{View.getInstance( multitonKey )}

        @raise MultitonError: if instance for this Multiton key has already
        been constructed
        """

        """Mapping of Mediator names to Mediator instances"""
        self.mediatorMap = {}

        """Mapping of Notification names to Observer lists"""
        self.observerMap = {}

        """The Multiton Key for this Core"""
        self.multitonKey = key

        if self.instanceMap.get(key) is not None:
            raise MultitonError(self.MULTITON_MSG)

        self.instanceMap[key] = self
        self.mediatorMap = {}
        self.observerMap = {}

        self.initializeView()

    def initializeView(self):
        """
        Initialize the Singleton C{View} instance.

        Called automatically by the constructor, this is your opportunity to
        initialize the Singleton instance in your subclass without overriding
        the constructor.
        """
        pass

    @classmethod
    def getInstance(cls, key):
        """
        C{View} Singleton Factory method.

        @return: the Singleton instance of C{View}
        """
        if cls.instanceMap.get(key) is None:
            cls.instanceMap[key] = View(key)

        return cls.instanceMap[key]

    def registerObserver(self, notificationName, observer):
        """
        Register an C{IObserver} to be notified
        of C{INotifications} with a given name.

        @param notificationName: the name of the C{INotifications} to notify this C{IObserver} of
        @param observer: the C{IObserver} to register
        """
        if not notificationName in self.observerMap:
            self.observerMap[notificationName] = []
        self.observerMap[notificationName].append(observer)

    def notifyObservers(self, notification):
        """
        Notify the C{IObservers} for a particular C{INotification}.

        All previously attached C{IObservers} for this C{INotification}'s
        list are notified and are passed a reference to the C{INotification} in
        the order in which they were registered.

        @param notification: the C{INotification} to notify C{IObservers} of.
        """
        # Get a reference to the observers list for this notification name
        observerRefs = self.observerMap.get(notification.getName())

        if observerRefs:
            # Notify observers from the working copy
            # Use a list's copy to avoid problems if the list content changes
            # inside the loop iteration
            for observer in observerRefs[:]:
                observer.notifyObserver(notification)

    def removeObserver(self, notificationName, notifyContext):
        """
        Remove the observer for a given notifyContext from an observer list for a given Notification name.

        @param notificationName: which observer list to remove from
        @param notifyContext: remove the observer with this object as its notifyContext
        """
        if notificationName in self.observerMap:
            # Get observer list for the notification under inspection
            observers = self.observerMap[notificationName]

            # Find the observer for the notifyContext
            for i, observer in enumerate(observers):
                if observer.compareNotifyContext(notifyContext):
                    # There can only be one bserver for a given notifyContext
                    # in any given Observer list, so remove it and break
                    del observers[i]
                    break

            # Also, when a Notification's Observer list length falls to
            # zero, delete the notification key from the observer map
            if len(observers) == 0:
                del self.observerMap[notificationName]

    def registerMediator(self, mediator):
        """
        Register an C{IMediator} instance with the C{View}.

        Registers the C{IMediator} so that it can be retrieved by name,
        and further interrogates the C{IMediator} for its
        C{INotification} interests.

        If the C{IMediator} returns any C{INotification}
        names to be notified about, an C{Observer} is created encapsulating
        the C{IMediator} instance's C{handleNotification} method
        and registering it as an C{Observer} for all C{INotifications} the
        C{IMediator} is interested in.

        @param mediator: a reference to the C{IMediator} instance
        """
        # Do not allow re-registration (you must to removeMediator first)
        name = mediator.getMediatorName()

        if self.mediatorMap.get(name):
            return

        mediator.initializeNotifier(self.multitonKey)

        # Register the Mediator for retrieval by name
        self.mediatorMap[name] = mediator

        # Get notification interests, if any
        interests = mediator.listNotificationInterests()

        # Register Mediator as an observer for each notification of interests
        if interests:
            # Create Observer referencing this mediator's
            # handleNotification method
            observer = puremvc.patterns.observer.Observer(
                mediator.handleNotification, mediator)

            # Register Mediator as Observer for its list interests
            for interest in interests:
                self.registerObserver(interest, observer)

        # Alert the Mediator that it has been registered
        mediator.onRegister()

    def retrieveMediator(self, mediatorName):
        """
        Retrieve an C{IMediator} from the C{View}.

        @param mediatorName: the name of the C{IMediator} instance to retrieve.
        @return: the C{IMediator} instance previously registered with the given C{mediatorName}.
        """
        return self.mediatorMap.get(mediatorName)

    def removeMediator(self, mediatorName):
        """
        Remove an C{IMediator} from the C{View}.

        @param mediatorName: name of the C{IMediator} instance to be removed.
        @return: the C{IMediator} that was removed from the C{View}
        """
        mediator = self.mediatorMap.get(mediatorName)

        if mediator:
            # For every notification this mediator is interested in...
            interests = mediator.listNotificationInterests()

            for interest in interests:
                # Remove the observer linking the mediator
                # to the notification interest
                self.removeObserver(interest, mediator)

            # Remove the mediator from the map
            del self.mediatorMap[mediatorName]

            # Alert the mediator that it has been removed
            mediator.onRemove()

        return mediator

    def hasMediator(self, mediatorName):
        """
        Check if a Mediator is registered or not

        @param mediatorName: the name of the C{IMediator}
        @return: whether a Mediator is registered with the given C{mediatorName}.
        """
        return self.mediatorMap.get(mediatorName) is not None

    @classmethod
    def removeView(cls, key):
        """
        Remove an IView instance

        @param key: of IView instance to remove
        """
        cls.instanceMap.pop(key, None)
