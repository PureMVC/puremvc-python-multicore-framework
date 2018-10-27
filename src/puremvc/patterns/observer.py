"""
 PureMVC Python Port by Toby de Havilland <toby.de.havilland@puremvc.org>
 PureMVC Python Port by Daniele Esposti <expo@expobrain.net>
 PureMVC - Copyright(c) 2006-08 Futurescale, Inc., Some rights reserved.
 Your reuse is governed by the Creative Commons Attribution 3.0 License
"""

from puremvc import MultitonError
import puremvc.interfaces
import puremvc.patterns.facade


class Observer(puremvc.interfaces.IObserver):
    """
    A base C{IObserver} implementation.

    An C{Observer} is an object that encapsulates information
    about an interested object with a method that should
    be called when a particular C{INotification} is broadcast.

    In PureMVC, the C{Observer} class assumes these responsibilities:

    Encapsulate the notification (callback) method of the interested object.

    Encapsulate the notification context (this) of the interested object.

    Provide methods for setting the notification method and context.

    Provide a method for notifying the interested object.

    @see: L{View<puremvc.core.View>}
    @see: L{Notification<puremvc.patterns.observer.Notification>}
    """

    def __init__(self, notifyMethod, notifyContext):
        """
        Constructor.

        The notification method on the interested object should take
        one parameter of type C{INotification}

        @param notifyMethod: the notification method of the interested object
        @param notifyContext: the notification context of the interested object
        """
        self.notify = None
        self.context = None

        self.setNotifyMethod(notifyMethod)
        self.setNotifyContext(notifyContext)

    def setNotifyMethod(self, notifyMethod):
        """
        Set the notification method.

        The notification method should take one parameter of type C{INotification}.

        @param notifyMethod: the notification (callback) method of the interested object.
        """
        self.notify = notifyMethod

    def setNotifyContext(self, notifyContext):
        """
        Set the notification context.

        @param notifyContext: the notification context (this) of the interested object.
        """
        self.context = notifyContext

    def getNotifyMethod(self):
        """
        Get the notification method.

        @return: the notification (callback) method of the interested object.
        """
        return self.notify

    def getNotifyContext(self):
        """
        Get the notification context.

        @return: the notification context (C{this}) of the interested object.
        """
        return self.context

    def notifyObserver(self, notification):
        """
        Notify the interested object.

        @param notification: the C{INotification} to pass to the interested
        object's notification method.
        """
        self.getNotifyMethod()(notification)

    def compareNotifyContext(self, obj):
        """
        Compare an object to the notification context.

        @param obj: the object to compare
        @return: boolean indicating if the object and the notification context
        are the same
        """
        return (obj is self.context)


class Notifier(puremvc.interfaces.INotifier):
    """
    A Base C{INotifier} implementation.

    C{MacroCommand, Command, Mediator} and C{Proxy}
    all have a need to send C{Notifications}.

    The C{INotifier} interface provides a common method called
    C{sendNotification} that relieves implementation code of
    the necessity to actually construct C{Notifications}.

    The C{Notifier} class, which all of the above mentioned classes
    extend, provides an initialized reference to the C{Facade}
    Multiton, which is required for the convenience method
    for sending C{Notifications}, but also eases implementation as these
    classes have frequent C{Facade} interactions and usually require
    access to the facade anyway.

    NOTE: In the MultiCore version of the framework, there is one caveat to
    notifiers, they cannot send notifications or reach the facade until they
    have a valid multitonKey.

    The multitonKey is set:

    on a Command when it is executed by the Controller

    on a Mediator is registered with the View

    on a Proxy is registered with the Model.

    @see: L{Proxy<puremvc.patterns.proxy.Proxy>}
    @see: L{Facade<puremvc.patterns.facade.Facade>}
    @see: L{Mediator<puremvc.patterns.mediator.Mediator>}
    @see: L{MacroCommand<puremvc.patterns.command.MacroCommand>}
    @see: L{SimpleCommand<puremvc.patterns.command.SimpleCommand>}
    """

    """Multiton error message"""
    MULTITON_MSG = ("Notifier multiton instance for this key "
                     "is not yet initialised!")

    def __init__(self, *args, **kwds):
        """
        Initialise the C{INotifier} instance with an empty multiton key
        """
        self.multitonKey = None

    def sendNotification(self, notificationName, body=None, type=None):
        """
        Create and send an C{INotification}.

        Keeps us from having to construct new INotification instances in our
        implementation code.


        @param notificationName: the name of the notification to send
        @param body: the body of the notification (optional)
        @param type: the type of the notification (optional)
        """
        if self.facade:
            self.facade.sendNotification(notificationName, body, type)

    def initializeNotifier(self, key):
        """
        Initialize this INotifier instance.

        This is how a Notifier gets its multitonKey. Calls to sendNotification
        or to access the facade will fail until after this method has been
        called.

        Mediators, Commands or Proxies may override this method in order to
        send notifications or access the Multiton Facade instance as soon as
        possible. They CANNOT access the facade in their constructors, since
        this method will not yet have been called.

        @param key: the multitonKey for this INotifier to use
        """
        self.multitonKey = key

    @property
    def facade(self):
        """
        Return the Multiton Facade instance
        """
        key = self.multitonKey

        if key is None:
            raise MultitonError(self.MULTITON_MSG)

        return puremvc.patterns.facade.Facade.getInstance(key)


class Notification(puremvc.interfaces.INotification):
    """
    A base C{INotification} implementation.

    PureMVC does not rely upon underlying event models such
    as the one provided with Flash, and ActionScript 3 does
    not have an inherent event model.

    The Observer Pattern as implemented within PureMVC exists
    to support event-driven communication between the
    application and the actors of the MVC triad.

    Notifications are not meant to be a replacement for Events
    in Flex/Flash/Apollo. Generally, C{IMediator} implementors
    place event listeners on their view components, which they
    then handle in the usual way. This may lead to the broadcast of C{Notification}s to
    trigger C{ICommand}s or to communicate with other C{IMediators}. C{IProxy} and C{ICommand}
    instances communicate with each other and C{IMediator}s
    by broadcasting C{INotification}s.

    A key difference between Flash C{Event}s and PureMVC
    C{Notification}s is that C{Event}s follow the
    'Chain of Responsibility' pattern, 'bubbling' up the display hierarchy
    until some parent component handles the C{Event}, while
    PureMVC C{Notification}s follow a 'Publish/Subscribe'
    pattern. PureMVC classes need not be related to each other in a
    parent/child relationship in order to communicate with one another
    using C{Notification}s.

    @see: L{Observer<puremvc.patterns.observer.Observer>}
    """

    def __init__(self, name, body=None, type=None):
        """
        Constructor.

        @param name: name of the C{Notification} instance. (required)
        @param body: the C{Notification} body. (optional)
        @param type: the type of the C{Notification} (optional)
        """

        """The name of the notification instance"""
        self.name = name

        """The body of the notification instance"""
        self.body = body

        """The type of the notification instance"""
        self.type = type

    def __repr__(self):
        """
        Get the string representation of the C{Notification} instance.

        @return: the string representation of the C{Notification} instance.
        """
        bd = "None" if self.body is None else repr(self.body)
        ty = "None" if self.type is None else repr(self.type)

        msg = "Notification Name: " + self.name
        msg += "\nBody:"+bd
        msg += "\nType:"+ty

        return msg

    def getName(self):
        """
        Get the name of the C{Notification} instance.

        @return: the name of the C{Notification} instance.
        """
        return self.name

    def setBody(self, body):
        """
        Set the body of the C{Notification} instance.
        """
        self.body = body

    def getBody(self):
        """
        Get the body of the C{Notification} instance.

        @return: the body object.
        """
        return self.body

    def setType(self, notificationType):
        """
        Set the type of the C{Notification} instance.
        """
        self.type = notificationType

    def getType(self):
        """
        Get the type of the C{Notification} instance.

        @return: the type
        """
        return self.type
