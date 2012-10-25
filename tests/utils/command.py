# -*- coding: utf-8 -*-

from puremvc.patterns.command import MacroCommand, SimpleCommand


class MacroCommandTestCommand(MacroCommand):

    def initializeMacroCommand(self):
        self.addSubCommand(MacroCommandTestSub1Command)
        self.addSubCommand(MacroCommandTestSub2Command)


class MacroCommandTestSub1Command(SimpleCommand):

    def execute(self, note):
        vo = note.getBody()
        vo.result1 = 2 * vo.input


class MacroCommandTestSub2Command(SimpleCommand):

    def execute(self, note):
        vo = note.getBody()
        vo.result2 = vo.input * vo.input


class MacroCommandTestVO(object):

    def __init__(self, value):
        self.input = value
        self.result1 = None
        self.result2 = None


class SimpleCommandTestCommand(SimpleCommand):

    def execute(self, note):
        vo = note.getBody()
        vo.result = 2 * vo.input


class SimpleCommandTestVO(object):

    def __init__(self, value):
        self.input = value
        self.result = None
