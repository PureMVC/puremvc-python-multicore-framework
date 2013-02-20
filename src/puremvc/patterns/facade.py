"""
 PureMVC Python Port by Toby de Havilland <toby.de.havilland@puremvc.org>
 PureMVC Python Port by Daniele Esposti <expo@expobrain.net>
 PureMVC - Copyright(c) 2006-08 Futurescale, Inc., Some rights reserved.
 Your reuse is governed by the Creative Commons Attribution 3.0 License
"""

from puremvc import MultitonError
import puremvc.interfaces
import puremvc.patterns.observer


class Facade(puremvc.interfaces.IFacade):
    """
    A base Multiton C{IFacade} implementation.

    In PureMVC, the C{Facade} class assumes these
    responsibilities:

    Initializing the C{Model}, C{View} and C{Controller} Singletons.

    Providing all the methods defined by the C{IModel, IView, & IController} interfaces.

    Providing the ability to override the specific C{Model}, C{View} and C{Controller} Singletons created.

    Providing a single point of contact to the application for registering C{Commands} and notifying C{Observers}


    @see: L{Model<puremvc.core.Model>}
    @see: L{View<puremvc.core.View>}
    @see: L{Controller<puremvc.core.Controller>}
    @see: L{Notification<puremvc.patterns.observer.Notification>}
    @see: L{Mediator<puremvc.patterns.mediator.Mediator>}
    @see: L{Proxy<puremvc.patterns.proxy.Proxy>}
    @see: L{SimpleCommand<puremvc.patterns.command.SimpleCommand>}
    @see: L{MacroCommand<puremvc.patterns.command.MacroCommand>}
    """

    """The Multiton Facade instanceMap."""
    instanceMap = {}

    """Message Constants"""
    MULTITON_MSG = "Facade instance for this Multiton key already constructed!"

    def __init__(self, key):
        """
        Constructor.

        This C{IFacade} implementation is a Multiton, so you should not call
        the constructor directly, but instead call the static Factory method,
        passing the unique key for this instance
        C{Facade.getInstance( multitonKey )}

        @raise MultitonError: if instance for this Multiton key has already
        been constructed
        """
        # References to Model, View and Controller
        self.controller = None
        self.model = None
        self.view = None

        # The Multiton Key for this app
        self.multitonKey = key

        if self.instanceMap.get(key):
            raise MultitonError(self.MULTITON_MSG)

        self.initializeNotifier(key)
        self.instanceMap[key] = self

        self.initializeFacade()

    def initializeFacade(self):
        """
        Initialize the Multiton C{Facade} instance.

        Called automatically by the constructor. Override in your subclass to
        do any subclass specific initializations. Be sure to call
        C{super.initializeFacade()}, though.
        """
        self.initializeController()
        self.initializeModel()
        self.initializeView()

    @classmethod
    def getInstance(cls, key):
        """
        Facade Multiton Factory method

        @return: the Multiton instance of the Facade
        """
        if cls.instanceMap.get(key) is None:
            cls.instanceMap[key] = cls(key)

        return cls.instanceMap[key]

    def initializeController(self):
        """
        Initialize the C{Controller}.

        Called by the C{initializeFacade} method.
        Override this method in your subclass of C{Facade}
        if one or both of the following are true:

        You wish to initialize a different C{IController}.
        You have C{Commands} to register with the C{Controller} at startup.

        If you don't want to initialize a different C{IController},
        call C{super.initializeController()} at the beginning of your method, then register C{Proxy}s.

        Note: This method is <i>rarely<i> overridden; in practice you are more
        likely to use a C{Command} to create and register C{Proxy}s
        with the C{Model}, since C{Proxy}s with mutable data will likely
        need to send C{INotification}s and thus will likely want to fetch a reference to
        the C{Facade} during their construction.
        """
        if self.controller is None:
            from puremvc.core import Controller

            self.controller = Controller.getInstance(self.multitonKey)

    def initializeModel(self):
        """
        Initialize the C{Model}.

        Called by the C{initializeFacade} method.
        Override this method in your subclass of C{Facade}
        if one or both of the following are true:

        You wish to initialize a different C{IModel}.

        You have C{Proxy}s to register with the Model that do not
        retrieve a reference to the Facade at construction time.

        If you don't want to initialize a different C{IModel},
        call C{super.initializeModel()} at the beginning of your
        method, then register C{Proxy}s.

        Note: This method is <i>rarely</i> overridden; in practice you are more
        likely to use a C{Command} to create and register C{Proxy}s with the
        C{Model}, since C{Proxy}s with mutable data will likely need to send
        C{INotification}s and thus will likely want to fetch a reference to
        the C{Facade} during their construction.
        """
        if self.model is None:
            from puremvc.core import Model

            self.model = Model.getInstance(self.multitonKey)

    def initializeView(self):
        """
        Initialize the C{View}.

        Called by the C{initializeFacade} method.
        Override this method in your subclass of C{Facade}
        if one or both of the following are true:

        You wish to initialize a different C{IView}.

        You have C{Observers} to register with the C{View}

        If you don't want to initialize a different C{IView},
        call C{super.initializeView()} at the beginning of your
        method, then register C{IMediator} instances.

        Note: This method is <i>rarely</i> overridden; in practice you are more
        likely to use a C{Command} to create and register C{Mediator}s with the
        C{View}, since C{IMediator} instances will need to send
        C{INotification}s and thus will likely want to fetch a reference
        to the C{Facade} during their construction.
        """
        if self.view is None:
            from puremvc.core import View

            self.view = View.getInstance(self.multitonKey)

    def registerCommand(self, notificationName, commandClassRef):
        """
        Register an C{ICommand} with the C{Controller} by Notification name.

        @param notificationName: the name of the C{INotification} to associate the C{ICommand} with
        @param commandClassRef: a reference to the Class of the C{ICommand}
        """
        self.controller.registerCommand(notificationName, commandClassRef)

    def removeCommand(self, notificationName):
        """
        Remove a previously registered C{ICommand} to C{INotification} mapping from the Controller.

        @param notificationName: the name of the C{INotification} to remove the C{ICommand} mapping for
        """
        self.controller.removeCommand(notificationName)

    def hasCommand(self, notificationName):
        """
        Check if a Command is registered for a given Notification

        @param notificationName: the name of the C{INotification}
        @return: whether a Command is currently registered for the given C{notificationName}.
        """
        return self.controller.hasCommand(notificationName)

    def registerProxy(self, proxy):
        """
        Register an C{IProxy} with the C{Model} by name.

        @param proxy: the C{IProxy} instance to be registered with the C{Model}.
        """
        self.model.registerProxy(proxy)

    def retrieveProxy(self, proxyName):
        """
        Retrieve an C{IProxy} from the C{Model} by name.

        @param proxyName: the name of the proxy to be retrieved.
        @return: the C{IProxy} instance previously registered with the given C{proxyName}.
        """
        return self.model.retrieveProxy(proxyName)

    def removeProxy(self, proxyName):
        """
        Remove an C{IProxy} from the C{Model} by name.

        @param proxyName: the C{IProxy} to remove from the C{Model}.
        @return: the C{IProxy} that was removed from the C{Model}
        """
        if self.model:
            return self.model.removeProxy(proxyName)

    def hasProxy(self, proxyName):
        """
        Check if a Proxy is registered

        @param proxyName: the name of the C{IProxy}
        @return: whether a Proxy is currently registered with the given C{proxyName}.
        """
        return self.model.hasProxy(proxyName)

    def registerMediator(self, mediator):
        """
        Register a C{IMediator} with the C{View}.

        @param mediator: a reference to the C{IMediator}
        """
        if (self.view is not None):
            self.view.registerMediator(mediator)

    def retrieveMediator(self, mediatorName):
        """
        Retrieve an C{IMediator} from the C{View}.

        @param mediatorName: the name of the C{IMediator}
        @return: the C{IMediator} previously registered with the given C{mediatorName}.
        """
        return self.view.retrieveMediator(mediatorName)

    def removeMediator(self, mediatorName):
        """
        Remove an C{IMediator} from the C{View}.

        @param mediatorName: name of the C{IMediator} to be removed.
        @return: the C{IMediator} that was removed from the C{View}
        """
        if self.view:
            return self.view.removeMediator(mediatorName)

    def hasMediator(self, mediatorName):
        """
        Check if a Mediator is registered or not

        @param mediatorName: the name of the C{IMediator}
        @return: whether a Mediator is registered with the given C{mediatorName}.
        """
        return self.view.hasMediator(mediatorName)

    def sendNotification(self, notificationName, body=None, type=None):
        """
        Create and send an C{INotification}.

        Keeps us from having to construct new notification
        instances in our implementation code.

        @param notificationName: the name of the notiification to send
        @param body: the body of the notification (optional)
        @param type: the type of the notification (optional)
        """
        self.notifyObservers(puremvc.patterns.observer.Notification(notificationName, body, type))

    def notifyObservers(self, notification):
        """
        Notify C{Observer}s.

        This method is left public mostly for backward
        compatibility, and to allow you to send custom
        notification classes using the facade.

        Usually you should just call sendNotification
        and pass the parameters, never having to
        construct the notification yourself.

        @param notification: the C{INotification} to have the C{View} notify C{Observers} of.
        """
        if (self.view is not None):
            self.view.notifyObservers(notification)

    def initializeNotifier(self, key):
        """
        Set the Multiton key for this facade instance.

        Not called directly, but instead from the constructor when getInstance
        is invoked. It is necessary to be public in order to implement
        INotifier.
        """
        self.multitonKey = key

    @classmethod
    def hasCore(cls, key):
        """
        Check if a Core is registered or not

        @param key: the multiton key for the Core in question
        @return: whether a Core is registered with the given C{key}.
        """
        return cls.instanceMap.get(key) is not None

    @classmethod
    def removeCore(cls, key):
        """
        Remove a Core.

        Remove the Model, View, Controller and Facade instances for the given
        key.

        @param key: of the Core to remove
        """
        if cls.instanceMap.get(key):
            from puremvc.core import Controller, Model, View

            Model.removeModel(key)
            View.removeView(key)
            Controller.removeController(key)

            cls.instanceMap.pop(key)
