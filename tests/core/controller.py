# -*- coding: utf-8 -*-

from puremvc import MultitonError
from puremvc.core import Controller
from puremvc.interfaces import IController
from puremvc.patterns.observer import Notification
from utils.controller import TestDoubleCommand, TestVO, TestIncrementCommand
import unittest
import uuid


class ControllerTest(unittest.TestCase):
    """ControllerTest: Test Controller Singleton"""

    KEY1 = uuid.uuid4()
    KEY2 = uuid.uuid4()

    def testGetInstance(self):
        """ControllerTest: getInstance() with different keys"""
        self.assertNotEqual(self.KEY1, self.KEY2)

        controller1 = Controller.getInstance(self.KEY1)
        controller2 = Controller.getInstance(self.KEY2)

        self.assertNotEqual(controller1, controller2)

    def testGetSameInstance(self):
        """ControllerTest: getInstance() with same key"""
        controller1 = Controller.getInstance(self.KEY1)
        controller2 = Controller.getInstance(self.KEY1)

        self.assertEqual(controller1, controller2)

    def testErrorSameKey(self):
        """ControllerTest: raise error if create controller with same key"""
        controller1 = Controller(self.KEY1)

        self.assertRaises(MultitonError, Controller, self.KEY1)

    def testNotNone(self):
        """ControllerTest: Test instance not null"""
        controller = Controller.getInstance(self.KEY1)

        self.assertNotEqual(None, controller)

    def testIsIController(self):
        """ControllerTest: Test instance implements IController"""
        controller = Controller.getInstance(self.KEY1)

        self.assertEqual(True, isinstance(controller, IController))

    def testRegisterAndExecuteCommand(self):
        """ControllerTest: Test registerCommand() and executeCommand()"""
        controller = Controller.getInstance(self.KEY1)

        controller.registerCommand('ControllerTest', TestDoubleCommand)

        vo = TestVO(12)
        note = Notification('ControllerTest', vo)

        controller.executeCommand(note)

        self.assertEqual(True, vo.result == 24)

    def testRegisterAndRemoveCommand(self):
        """ControllerTest: Test registerCommand() and removeCommand()"""
        controller = Controller.getInstance(self.KEY1)

        controller.registerCommand('ControllerRemoveTest', TestDoubleCommand)

        vo = TestVO(12)
        note = Notification('ControllerRemoveTest', vo)

        controller.executeCommand(note)

        self.assertEqual(True, vo.result == 24)

        vo.result = 0

        controller.removeCommand('ControllerRemoveTest')
        controller.executeCommand(note)

        self.assertEqual(True, vo.result == 0)

    def testHasCommand(self):
        """ControllerTest: Test hasCommand()"""
        # Create controllers
        controller1 = Controller.getInstance(self.KEY1)
        controller2 = Controller.getInstance(self.KEY2)

        # Register commands
        controller1.registerCommand('incrementCommand', TestIncrementCommand)
        controller2.registerCommand('doubleCommand', TestDoubleCommand)

        self.assertEqual(True, controller1.hasCommand('incrementCommand'))
        self.assertEqual(False, controller2.hasCommand('incrementCommand'))

        self.assertEqual(False, controller1.hasCommand('doubleCommand'))
        self.assertEqual(True, controller2.hasCommand('doubleCommand'))

        # Remove commands
        controller1.removeCommand('incrementCommand')
        controller2.removeCommand('doubleCommand')

        self.assertEqual(False, controller1.hasCommand('incrementCommand'))
        self.assertEqual(False, controller2.hasCommand('doubleCommand'))
