# -*- coding: utf-8 -*-

from puremvc.interfaces import INotification, IMediator
from puremvc.patterns.mediator import Mediator
from puremvc.patterns.observer import Notification


class ViewTestNote(Notification, INotification):

    NAME = "ViewTestNote"

    def __init__(self, anme, body):
        Notification.__init__(self, ViewTestNote.NAME, body)

    @staticmethod
    def create(body):
        return ViewTestNote(ViewTestNote.NAME, body)


class ViewTestMediator(Mediator, IMediator):

    NAME = 'ViewTestMediator'

    def __init__(self, view):
        Mediator.__init__(self, ViewTestMediator.NAME, view)

    def listNotificationInterests(self):
        return ['ABC', 'DEF', 'GHI']


class ViewTestMediator2(Mediator, IMediator):

    NAME = 'ViewTestMediator2'

    def __init__(self, view):
        Mediator.__init__(self, ViewTestMediator2.NAME, view)

    def listNotificationInterests(self):
        return [
            self.viewComponent.NOTE1,
            self.viewComponent.NOTE2,
            self.viewComponent.NOTE5,
        ]

    def handleNotification(self, notification):
        self.viewComponent.lastNotification = notification.getName()

        if notification.getName() == self.viewComponent.NOTE5:
            self.facade.removeMediator(self.NAME)


class ViewTestMediator3(Mediator, IMediator):

    NAME = 'ViewTestMediator3'

    def __init__(self, view):
        Mediator.__init__(self, ViewTestMediator3.NAME, view)

    def listNotificationInterests(self):
        return [
            self.viewComponent.NOTE3,
            self.viewComponent.NOTE5,
        ]

    def handleNotification(self, notification):
        self.viewComponent.lastNotification = notification.getName()
        if notification.getName() == self.viewComponent.NOTE5:
            self.facade.removeMediator(self.NAME)


class ViewTestMediator4(Mediator, IMediator):

    NAME = 'ViewTestMediator4'

    def __init__(self, view):
        Mediator.__init__(self, ViewTestMediator4.NAME, view)

    def onRegister(self):
        self.viewComponent.onRegisterCalled = True

    def onRemove(self):
        self.viewComponent.onRemoveCalled = True


class ViewTestMediator5(Mediator, IMediator):

    NAME = 'ViewTestMediator5'

    def __init__(self, view):
        Mediator.__init__(self, ViewTestMediator5.NAME, view)

    def listNotificationInterests(self):
        return [self.viewComponent.NOTE5]

    def handleNotification(self, notification):
        self.viewComponent.counter += 1
