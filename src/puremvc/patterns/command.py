"""
 PureMVC Python Port by Toby de Havilland <toby.de.havilland@puremvc.org>
 PureMVC Python Port by Daniele Esposti <expo@expobrain.net>
 PureMVC - Copyright(c) 2006-08 Futurescale, Inc., Some rights reserved.
 Your reuse is governed by the Creative Commons Attribution 3.0 License
"""

import puremvc.interfaces
import puremvc.patterns.observer

class MacroCommand(puremvc.patterns.observer.Notifier, puremvc.interfaces.ICommand):
    """
    A base C{ICommand} implementation that executes other C{ICommand}s.

    A C{MacroCommand} maintains an list of C{ICommand} Class references called <i>SubCommands</i>.

    When C{execute} is called, the C{MacroCommand}
    instantiates and calls C{execute} on each of its <i>SubCommands</i> turn.
    Each <i>SubCommand</i> will be passed a reference to the original
    C{INotification} that was passed to the C{MacroCommand}'s
    C{execute} method.

    Unlike C{SimpleCommand}, your subclass
    should not override C{execute}, but instead, should
    override the C{initializeMacroCommand} method,
    calling C{addSubCommand} once for each <i>SubCommand</i>
    to be executed.

    @see: L{Controller<puremvc.core.Controller>}
    @see: L{Notification<puremvc.patterns.observer.Notification>}
    @see: L{SimpleCommand<puremvc.patterns.command.SimpleCommand>}
    """

    def __init__(self):
        """
        MacroCommand Constructor.

        You should not need to define a constructor,
        instead, override the C{initializeMacroCommand}
        method.

        If your subclass does define a constructor, be sure to call C{super()}.
        """
        # Call superclass
        super(MacroCommand, self).__init__()

        # Initialize class
        self.subCommands = []

        self.initializeMacroCommand()

    def initializeMacroCommand(self):
        """
        Initialize the C{MacroCommand}.

        In your subclass, override this method to initialize the
        C{MacroCommand}'s <i>SubCommand</i> list with C{ICommand} class
        references like this::

            // Initialize MyMacroCommand
            function initializeMacroCommand( ) : void
            {
                addSubCommand( com.me.myapp.controller.FirstCommand );
                addSubCommand( com.me.myapp.controller.SecondCommand );
                addSubCommand( com.me.myapp.controller.ThirdCommand );
            }

        Note that <i>SubCommand</i>s may be any C{ICommand} implementor,
        C{MacroCommand}s or C{SimpleCommands} are both acceptable.
        """
        pass

    def addSubCommand(self, commandClassRef):
        """
        Add a <i>SubCommand</i>.

        The <i>SubCommands</i> will be called in First In/First Out (FIFO)
        order.

        @param commandClassRef: a reference to the C{Class} of the C{ICommand}.
        """
        self.subCommands.append(commandClassRef)

    def execute(self, notification):
        """
        Execute this C{MacroCommand}'s <i>SubCommands</i>.

        The <i>SubCommands</i> will be called in First In/First Out (FIFO)
        order.

        @param notification: the C{INotification} object to be passsed to each
        <i>SubCommand</i>.
        """
        for commandClassRef in self.subCommands[:]:
            commandInstance = commandClassRef()
            commandInstance.initializeNotifier(self.multitonKey)
            commandInstance.execute(notification)


class SimpleCommand(puremvc.patterns.observer.Notifier, puremvc.interfaces.ICommand):
    """
    A base C{ICommand} implementation.

    Your subclass should override the C{execute}
    method where your business logic will handle the C{INotification}.

    @see: L{Controller<puremvc.core.Controller>}
    @see: L{Notification<puremvc.patterns.observer.Notification>}
    @see: L{MacroCommand<puremvc.patterns.command.MacroCommand>}
    """

    def execute(self, notification):
        """
        Fulfill the use-case initiated by the given C{INotification}.

        In the Command Pattern, an application use-case typically
        begins with some user action, which results in an C{INotification} being broadcast, which
        is handled by business logic in the C{execute} method of an
        C{ICommand}.

        @param notification: the C{INotification} to handle.
        """
        pass
