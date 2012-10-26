"""
 PureMVC Python Port by Toby de Havilland <toby.de.havilland@puremvc.org>
 PureMVC Python Port by Daniele Esposti <expo@expobrain.net>
 PureMVC - Copyright(c) 2006-08 Futurescale, Inc., Some rights reserved.
 Your reuse is governed by the Creative Commons Attribution 3.0 License
"""

import puremvc.interfaces
import puremvc.patterns.observer

class Proxy(puremvc.patterns.observer.Notifier, puremvc.interfaces.IProxy):
    """
    A base C{IProxy} implementation.

    In PureMVC, C{Proxy} classes are used to manage parts of the
    application's data model.

    A C{Proxy} might simply manage a reference to a local data object,
    in which case interacting with it might involve setting and
    getting of its data in synchronous fashion.

    C{Proxy} classes are also used to encapsulate the application's
    interaction with remote services to save or retrieve data, in which case,
    we adopt an asyncronous idiom; setting data (or calling a method) on the
    C{Proxy} and listening for a C{Notification} to be sent
    when the C{Proxy} has retrieved the data from the service.

    @see: L{Model<puremvc.core.Model>}
    """

    NAME = "Proxy"

    def __init__(self, proxyName=None, data=None):
        """
        Proxy Constructor

        @param proxyName: the name of the proxy instance (optional)
        @param data: the proxy data (optional)
        """

        """ Call superclass """
        super(Proxy, self).__init__()

        """ The proxy name """
        self.proxyName = proxyName if proxyName is not None else self.NAME

        """ The proxy data """
        self.data = None

        if data is not None:
            self.setData(data)

    def getProxyName(self):
        """
        Get the Proxy name

        @return: the proxy name
        """
        return self.proxyName

    def setData(self, data):
        """
        Set the Proxy data

        @param data: the Proxy data object
        """
        self.data = data

    def getData(self):
        """
        Get the proxy data

        @return: the Proxy data object
        """
        return self.data

    def onRegister(self):
        """
        Called by the Model when the Proxy is registered
        """
        pass

    def onRemove(self):
        """
        Called by the Model when the Proxy is removed
        """
        pass
