# Proxy.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

from typing import Any

from puremvc.interfaces import IProxy
from puremvc.patterns.facade import Notifier


class Proxy(IProxy, Notifier):
    """
    A base `IProxy` implementation.

    In PureMVC, `Proxy` classes are used to manage parts of the
    application's data model.

    A `Proxy` might simply manage a reference to a local data object,
    in which case interacting with it might involve setting and
    getting of its data in synchronous fashion.

    `Proxy` classes are also used to encapsulate the application's
    interaction with remote services to save or retrieve data, in which case,
    we adopt an asynchronous idiom; setting data (or calling a method) on the
    `Proxy` and listening for a `Notification` to be sent
    when the `Proxy` has retrieved the data from the service.

    See Also
    --------
    :class:`puremvc.core.Model`
    """

    """NAME (str): The name of the `Proxy`"""
    NAME = "Proxy"

    def __init__(self, proxy_name: str = None, data: Any = None):
        """
        Constructor

        :param proxy_name: The name of the proxy. Defaults to None.
        :type proxy_name: str
        :param data: The data associated with the object. Defaults to None.
        :type data: Any
        """
        super().__init__()
        self._proxy_name = self.NAME if proxy_name is None else proxy_name
        self.data = data

    @property
    def proxy_name(self) -> str:
        """
        Get the `Proxy` name

        :return: The proxy name.
        :rtype: str
        """
        return self._proxy_name

    @property
    def data(self) -> Any:
        """
        Get the `Proxy` data

        :return: The Proxy `data` object.
        :rtype: Any
        """
        return self._data

    @data.setter
    def data(self, value: Any):
        """
        Set the `Proxy` data

        :param value: The Proxy data object
        :type value: Any
        :return: None
        """
        self._data = value

    def on_register(self):
        """Called by the `Model` when the `Proxy` is registered"""
        return

    def on_remove(self):
        """Called by the `Model` when the `Proxy` is removed"""
        return
