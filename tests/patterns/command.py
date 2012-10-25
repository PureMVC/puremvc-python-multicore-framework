# -*- coding: utf-8 -*-

from puremvc.patterns.observer import Notification
from utils.command import (MacroCommandTestVO, MacroCommandTestCommand,
    SimpleCommandTestVO, SimpleCommandTestCommand)
import unittest


class CommandTest(unittest.TestCase):
    """CommandTest: Test Command Pattern"""

    def testMacroCommandExecute(self):
        """CommandTest: Test MacroCommand execute()"""

        vo = MacroCommandTestVO(5)
        note = Notification('MacroCommandTest', vo)
        command = MacroCommandTestCommand()
        command.execute(note)

        self.assertEqual(True, vo.result1 == 10)
        self.assertEqual(True, vo.result2 == 25)

    def testSimpleCommandExecute(self):
        """CommandTest: Test SimpleCommand execute()"""

        vo = SimpleCommandTestVO(5)
        note = Notification('SimpleCommandTestNote', vo)
        command = SimpleCommandTestCommand()
        command.execute(note)

        self.assertEqual(True, vo.result == 10)
