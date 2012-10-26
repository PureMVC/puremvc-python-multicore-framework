# -*- coding: utf-8 -*-

from puremvc.patterns.command import SimpleCommand


class FacadeTestCommand(SimpleCommand):

    def execute(self, note):
        vo = note.getBody()
        vo.result = 2 * vo.input


class FacadeInstanceTestCommand(SimpleCommand):

    def execute(self, note):
        note.body.result = self.facade


class FacadeTestVO(object):

    def __init__(self, value):
        self.input = value
        self.result = None
