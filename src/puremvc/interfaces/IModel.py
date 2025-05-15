# IModel.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

from abc import ABC, abstractmethod

from .IProxy import IProxy


class IModel(ABC):
    """
    The interface definition for a PureMVC Model.

    In PureMVC, `IModel` implementors provide
    access to `IProxy` objects by named look up.

    An `IModel` assumes these responsibilities:

    Maintain a cache of `IProxy` instances
    Provide methods for registering, retrieving, and removing `IProxy` instances
    """

    @abstractmethod
    def register_proxy(self, proxy: IProxy):
        """
        Register an `IProxy` instance with the `Model`.

        :param proxy: An object reference to be held by the `Model`.
        :type proxy: IProxy
        """
        pass

    @abstractmethod
    def retrieve_proxy(self, proxy_name: str) -> IProxy:
        """
        Retrieve an `IProxy` instance from the Model.

        :param proxy_name: The name of the proxy to retrieve.
        :type proxy_name: str
        :return: The `IProxy` instance previously registered with the given `proxy_name`.
        :rtype: IProxy
        """
        pass

    @abstractmethod
    def remove_proxy(self, proxy_name: str) -> IProxy:
        """
        Remove an `IProxy` instance from the Model.

        :param proxy_name: The name of the proxy to remove.
        :type proxy_name: str
        :return: The `IProxy` instance that was removed from the Model.
        :rtype: IProxy
        """
        pass

    @abstractmethod
    def has_proxy(self, proxy_name: str) -> bool:
        """
        Check if a proxy with the given name is registered.

        :param proxy_name: The name of the proxy to check.
        :type proxy_name: str
        :return: True if the proxy is registered, False otherwise.
        :rtype: bool
        """
        pass
