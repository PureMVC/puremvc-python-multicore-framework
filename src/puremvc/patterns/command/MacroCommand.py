# MacroCommand.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

from typing import List, Callable

from puremvc.interfaces import ICommand, INotification
from puremvc.patterns.facade import Notifier


class MacroCommand(Notifier, ICommand):
    """
    A base `ICommand` implementation that executes other `ICommand`.

    A `MacroCommand` maintains a list of `ICommand` Class references called `SubCommands`.

    When `execute` is called, the `MacroCommand`
    instantiates and calls `execute` on each of its `SubCommand` turn.
    Each `SubCommand` will be passed a reference to the original
    `INotification` that was passed to the `MacroCommand`'s
    `execute` method.

    Unlike `SimpleCommand`, your subclass
    should not override `execute`, but instead, should
    override the `initialize_macro_command` method,
    calling `add_subcommand` once for each `SubCommand`
    to be executed.

    See Also
    --------
    :class:`puremvc.core.Controller`
    :class:`puremvc.patterns.observer.Notification`
    :class:`puremvc.patterns.command.SimpleCommand`
    """

    def __init__(self):
        """
        MacroCommand Constructor.

        You should not need to define a constructor, instead, override the `initialize_macro_command` method.

        If your subclass does define a constructor, be sure to call `super().__init__()`.

        :return: None
        """
        super().__init__()
        self._subcommands: List[Callable[[], ICommand]] = []

    def initialize_macro_command(self):
        """
        Initialize the `MacroCommand`.

        In your subclass, override this method to initialize the `MacroCommand` `SubCommand` list with `ICommand`
        class references like this:

        Initialize MyMacroCommand::
        
            def initialize_macro_command(self):
                self.add_subcommand(lambda: FirstCommand())
                self.add_subcommand(lambda: SecondCommand())
                self.add_subcommand(lambda: ThirdCommand())

        Note that `SubCommand` may be any `ICommand` implementor,
        `MacroCommand` or `SimpleCommands` are both acceptable.

        :return: None
        """
        return

    def add_subcommand(self, factory: Callable[[], ICommand]):
        """
        Add a `SubCommand`.

        The `SubCommands` will be called in First In/First Out (FIFO) order.

        :param factory: A callable object that returns an instance of ICommand.
        :type factory: Callable[[], ICommand]
        :return: None
        """
        self._subcommands.append(factory)

    def execute(self, notification: INotification):
        """
        Execute this `MacroCommand`'s `SubCommands`.

        The `SubCommands` will be called in First In/First Out (FIFO)
        order.

        :param notification: The `INotification` object to be passed to each`SubCommand`.
        :type notification: INotification
        :return: None
        """
        self.initialize_macro_command()
        while self._subcommands:
            factory = self._subcommands.pop(0)
            command = factory()
            command.initialize_notifier(self.multitonKey)
            command.execute(notification)
