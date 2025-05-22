# Notification.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

from typing import Any, Optional

from puremvc.interfaces import INotification


class Notification(INotification):
    """
    A base `INotification` implementation.

    PureMVC does not rely upon underlying event models such
    as the one provided with Flash, and ActionScript 3 does
    not have an inherent event model.

    The Observer Pattern as implemented within PureMVC exists
    to support event-driven communication between the
    application and the actors of the MVC triad.

    Notifications are not meant to be a replacement for Events
    in Flex/Flash/Apollo. Generally, `IMediator` implementors
    place event listeners on their view components, which they
    then handle in the usual way. This may lead to the broadcast of `Notification` to
    trigger `ICommand` or to communicate with other `IMediators`. `IProxy` and `ICommand`
    instances communicate with each other and `IMediator`s
    by broadcasting `INotification`.

    A key difference between Flash `Event` and PureMVC
    `Notification` is that `Event` follows the
    'Chain of Responsibility' pattern, 'bubbling' up the display hierarchy
    until some parent component handles the `Event`, while
    PureMVC `Notification` follows a 'Publish/Subscribe'
    pattern. PureMVC classes need not be related to each other in a
    parent/child relationship to communicate with one another
    using `Notification`.

    See Also
    --------
    :class:`puremvc.patterns.observer.Observer`
    """

    def __init__(self, name: str, body: Any = None, type: Optional[str] = None) -> None:
        """
        Constructor.

        :param name: name of the `Notification` instance. (required)
        :type name: str
        :param body: the `Notification` body. (optional)
        :type body: Any
        :param type: The type of the note. Defaults to None.
        :type type: str
        """
        self._name = name
        self._body = body
        self._type = type

    @property
    def name(self) -> str:
        """
        Get the name of the `Notification` instance.

        :return: The name of the `Notification` instance.
        :rtype: str
        """
        return self._name

    @property
    def body(self) -> Any:
        """
        This method returns the value of the `_body` attribute.

        :return: The value of the `_body` attribute.
        :rtype: Any
        """
        return self._body

    @body.setter
    def body(self, body: Any) -> None:
        """
        Set the body of the `Notification` instance.

        :param body: The new value for the body.
        :type body: Any
        :return: None
        """
        self._body = body

    @property
    def type(self) -> Optional[str]:
        """
        Get the body of the `Notification` instance.

        :return: The type of the object.
        :rtype: Optional[str]
        """
        return self._type

    @type.setter
    def type(self, note_type: str) -> None:
        """
        Set the type of the `Notification` instance.
        :param note_type: The new type for the `Notification` instance.
        :type note_type: str
        :return: None
        """
        self._type = note_type

    def __repr__(self) -> str:
        """
        Get the string representation of the `Notification` instance.

        :return: The string representation of the `Notification` instance.
        :rtype: str
        """
        return ("Notification Name: " + self.name +
                "\nBody:" + "None" if self.body is None else repr(self.body) +
                "\nType:" + ("None" if self.type is None else repr(self.type)))
