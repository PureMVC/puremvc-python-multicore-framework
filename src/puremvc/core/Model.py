# Model.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

import threading
from typing import Callable, Dict, Optional

from puremvc.interfaces import IModel, IProxy


class Model(IModel):
    """
    A Multiton `IModel` implementation.

    In PureMVC, the `Model` class provides access to model objects (Proxies)
    by named lookup.

    The `Model` assumes these responsibilities:

    - Maintain a cache of `IProxy` instances.
    - Provide methods for registering, retrieving, and removing `IProxy` instances.

    Your application must register `IProxy` instances with the `Model`.
    Typically, you use an `ICommand` to create and register `IProxy`
    instances once the `Facade` has initialized the Core actors.

    See Also
    --------
    :class:`puremvc.patterns.proxy.Proxy`
    :class:`puremvc.interfaces.IProxy`
    """
    instanceMap: Dict[str, IModel] = dict()
    instanceMapLock: threading.Lock = threading.Lock()

    """MULTITON_MSG (str): Multiton error message"""
    MULTITON_MSG = "Model multiton instance for this key is already constructed!"

    def __init__(self, key: str) -> None:
        """
        Constructor.

        This IModel implementation is a Multiton,
        so you should not call the constructor
        directly, but instead call the static Multiton
        Factory method Model.get_instance(multiton_key)

        :param key: A unique key for this instance of the Model.
        :raises Exception: If an instance with the given `key` already exists in the `instanceMap`.
        :type key: str
        """
        if Model.instanceMap.get(key) is not None:
            raise Exception(Model.MULTITON_MSG)
        self.multitonKey: str = key
        Model.instanceMap[key] = self
        self.proxyMap: Dict[str, IProxy] = dict()
        self.proxyMapLock: threading.Lock = threading.Lock()
        self.initialize_model()

    def initialize_model(self) -> None:
        """
        Initialize the `Model` instance.

        Called automatically by the constructor, this is your opportunity to
        initialize the Multiton instance in your subclass without overriding
        the constructor.

        :return: None
        """
        return

    @classmethod
    def get_instance(cls, key: str, factory: Callable[[str], IModel]) -> Optional[IModel]:
        """
        Multiton Factory method.

        :param key: A string representing the key used to retrieve the instance.
        :type key: str
        :param factory: A factory function used to create new instances of `IModel`.
        :type factory: Callable[[str], IModel]
        :return: An instance of `IModel` associated with the given key.
        :rtype: Optional[IModel]
        """
        with cls.instanceMapLock:
            if key not in cls.instanceMap:
                cls.instanceMap[key] = factory(key)
        return cls.instanceMap.get(key)

    def register_proxy(self, proxy: IProxy) -> None:
        """
        Register an `IProxy` with the `Model`.

        :param proxy: An `IProxy` to be held by the `Model`.
        :type proxy: IProxy
        :return: None
        """
        proxy.initialize_notifier(self.multitonKey)
        with self.proxyMapLock:
            self.proxyMap[proxy.proxy_name] = proxy
        proxy.on_register()

    def retrieve_proxy(self, proxy_name: str) -> Optional[IProxy]:
        """
        Retrieve an `IProxy` from the `Model`.

        :param proxy_name: The name of the proxy.
        :type proxy_name: str
        :return: the `IProxy` instance previously registered with the given `proxyName`.
        :rtype: Optional[IProxy]
        """
        with self.proxyMapLock:
            return self.proxyMap.get(proxy_name)

    def has_proxy(self, proxy_name: str) -> bool:
        """
        Check if a Proxy is registered

        :param proxy_name: A string representing the name of the proxy to check.
        :type proxy_name: str
        :return: Returns True if the proxy exists in the proxy map, False otherwise.
        :rtype: bool
        """
        with self.proxyMapLock:
            return self.proxyMap.get(proxy_name) is not None

    def remove_proxy(self, proxy_name: str) -> Optional[IProxy]:
        """
        Remove an `IProxy` from the `Model`.

        :param proxy_name: The name of the `IProxy` to remove.
        :type proxy_name: str
        :return: the `IProxy` that was removed from the `Model`
        :rtype: Optional[IProxy]
        """
        with self.proxyMapLock:
            proxy = self.proxyMap.get(proxy_name)
            if proxy:
                del self.proxyMap[proxy_name]
        if proxy:
            proxy.on_remove()
        return proxy

    @classmethod
    def remove_model(cls, key: str) -> None:
        """
        Remove an IModel instance

        :param key: multiton_key of IModel instance to remove
        :type key: str
        :return: None
        """
        with cls.instanceMapLock:
            del cls.instanceMap[key]
