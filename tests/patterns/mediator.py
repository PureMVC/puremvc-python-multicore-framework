# -*- coding: utf-8 -*-

from puremvc.patterns.mediator import Mediator
import unittest


class MediatorTest(unittest.TestCase):
    """MediatorTest: Test Mediator Pattern"""

    def testNameAccessor(self):
        """MediatorTest: Test getMediatorName()"""
        mdiatr = Mediator()
        self.assertEqual(True, mdiatr.getMediatorName() == Mediator.NAME)

    def testViewAccessor(self):
        """MediatorTest: Test getViewComponent()"""

        view = object()
        mdiatr = Mediator(Mediator.NAME, view)
        self.assertEqual(True, mdiatr.getViewComponent() is not None)
