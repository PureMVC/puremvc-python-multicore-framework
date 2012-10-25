"""
 PureMVC Python Port by Toby de Havilland <toby.de.havilland@puremvc.org>
 PureMVC Python Port by Daniele Esposti <expo@expobrain.net>
 PureMVC - Copyright(c) 2006-08 Futurescale, Inc., Some rights reserved.
 Your reuse is governed by the Creative Commons Attribution 3.0 License
"""

import puremvc.interfaces
import puremvc.patterns.observer

class Mediator(puremvc.patterns.observer.Notifier, puremvc.interfaces.IMediator):
    """
    A base C{IMediator} implementation.

    @see: L{View<puremvc.core.View>}
    """

    """
    The name of the C{Mediator}.
    """
    NAME = "Mediator"

    def __init__(self, mediatorName=None, viewComponent=None):
        """
        Mediator Constructor

        Typically, a C{Mediator} will be written to serve
        one specific control or group controls and so,
        will not have a need to be dynamically named.
        """
        # Call superclass
        super(Mediator, self).__init__()

        # Initialize class
        self.mediatorName = self.NAME if mediatorName is None else mediatorName
        self.viewComponent = viewComponent

    def getMediatorName(self):
        """
        Get the name of the C{Mediator}.

        @return: the Mediator name
        """
        return self.mediatorName

    def setViewComponent(self, viewComponent):
        """
        Set the C{IMediator}'s view component.

        @param viewComponent: the view component
        """
        self.viewComponent = viewComponent

    def getViewComponent(self):
        """
        Get the C{Mediator}'s view component.

        Additionally, an implicit getter will usually be defined in the
        subclass that casts the view object to a type, like this::

            private function get comboBox : mx.controls.ComboBox
            {
                return viewComponent as mx.controls.ComboBox;
            }

        @return: the view component
        """
        return self.viewComponent

    def listNotificationInterests(self):
        """
        List the C{INotification} names this
        C{Mediator} is interested in being notified of.

        @return: List the list of C{INotification} names
        """
        return []

    def handleNotification(self, notification):
        """
        Handle C{INotification}s.

        Typically this will be handled in a if/else statement,
        with one 'comparison' entry per C{INotification}
        the C{Mediator} is interested in.
        """
        pass

    def onRegister(self):
        """
        Called by the View when the Mediator is registered
        """
        pass

    def onRemove(self):
        """
        Called by the View when the Mediator is removed
        """
        pass
