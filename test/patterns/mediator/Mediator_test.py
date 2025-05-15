# Mediator_test.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

import unittest

from puremvc.patterns.mediator import Mediator


class MediatorTest(unittest.TestCase):
    """Test the PureMVC Mediator class."""

    def test_name_accessor(self):
        """Tests getting the name using Mediator class accessor method. """
        # Create a new Mediator and use accessors to set the mediator name
        mediator = Mediator()

        # test assertions
        self.assertEqual(True, mediator.mediator_name == "Mediator",
                         "Expecting mediator.mediator_name == Mediator.NAME")

    def test_view_accessor(self):
        """Tests getting the name using Mediator class accessor method. """
        # Create a view object
        view = object()

        # Create a new Proxy and use accessors to set the proxy name
        mediator = Mediator(Mediator.NAME, view)

        # test assertions
        self.assertIsNotNone(mediator.view_component, "Expecting mediator.view_component not None")


if __name__ == '__main__':
    unittest.main()
