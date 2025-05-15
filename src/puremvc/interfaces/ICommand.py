# ICommand.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

from abc import abstractmethod

from .INotification import INotification
from .INotifier import INotifier


class ICommand(INotifier):
    """
    The interface definition for a PureMVC Command

    See Also
    --------
    :class:`puremvc.interfaces.INotification`
    """

    @abstractmethod
    def execute(self, notification: INotification):
        """
        Execute the `ICommand`'s logic to handle a given `INotification`.

        :param notification: An `INotification` to handle.
        :type notification: INotification
        :return: None
        """
        pass
