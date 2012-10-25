# -*- coding: utf-8 -*-

from puremvc.patterns.command import SimpleCommand


class TestDoubleCommand(SimpleCommand):
    """Simple test command which double the input value"""

    def execute(self, note):
        vo = note.getBody()

        vo.result = 2 * vo.input


class TestIncrementCommand(SimpleCommand):
    """Simple test command which increments by 1 the input value"""

    def execute(self, note):
        vo = note.getBody()

        vo.result = 2 * vo.input


class TestVO(object):
    """Test value object"""

    def __init__(self, num=0):
        self.input = num
        self.result = 0
