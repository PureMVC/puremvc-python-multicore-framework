# IProxy.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

from abc import abstractmethod
from typing import Any

from .INotifier import INotifier


class IProxy(INotifier):
    """
    The interface definition for a PureMVC Proxy.

    In PureMVC, 'IProxy' implementors assume these responsibilities:</P>

    Implement a common method which returns the name of the Proxy.
    Provide methods for setting and getting the data object.

    Additionally, 'IProxy's typically:

    Maintain references to one or more pieces of model data.
    Provide methods for manipulating that data.
    Generate 'INotifications' when their model data changes.
    Expose their name as a 'public static const' called 'NAME',
    if they are not instantiated multiple times.
    Encapsulate interaction with local or remote services used to fetch and persist model data.
    """

    @property
    @abstractmethod
    def proxy_name(self) -> str:
        """
        Get the Proxy name

        :return: The name of the proxy as a string.
        :rtype: str
        """
        pass

    @property
    @abstractmethod
    def data(self) -> Any:
        """
        Get the data object

        :return: The data of the method.
        :rtype: Any
        """
        pass

    @data.setter
    def data(self, value: Any):
        """
        Get the data object

        :param value: The value to be set for the `data` attribute.
        :type value: Any
        :return: None
        """
        pass

    @abstractmethod
    def on_register(self):
        """Called by the Model when the Proxy is registered."""
        pass

    @abstractmethod
    def on_remove(self):
        """Called by the Model when the Proxy is removed."""
        pass
