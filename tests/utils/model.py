# -*- coding: utf-8 -*-

from puremvc.patterns.proxy import Proxy


class ModelTestProxy(Proxy):

    NAME = 'ModelTestProxy'
    ON_REGISTER_CALLED = 'onRegister Called'
    ON_REMOVE_CALLED = 'onRemove Called'

    def __init__(self):
        super(ModelTestProxy, self).__init__(ModelTestProxy.NAME, object())

    def onRegister(self):
        self.setData(ModelTestProxy.ON_REGISTER_CALLED)

    def onRemove(self):
        self.setData(ModelTestProxy.ON_REMOVE_CALLED)
