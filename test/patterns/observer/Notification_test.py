# Notification_test.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

import unittest

from puremvc.patterns.observer import Notification


class NotificationTest(unittest.TestCase):
    """Test the PureMVC Notification class."""

    def test_name_accessor(self):
        """Tests setting and getting the name using Notification class accessor methods."""
        # Create a new Notification and use accessors to set the note name
        note = Notification("TestNote")

        # test assertions
        self.assertTrue(note.name == "TestNote", "Expecting note.name == 'TestNote'")

    def test_test_body_accessors(self):
        """Tests setting and getting the body using Notification class accessor methods."""
        # Create a new Notification and use accessors to set the body
        note = Notification("TestNote")
        note.body = 5

        # test assertions
        self.assertTrue(note.body == 5, "Expecting note.body == 5")

    def test_constructor(self):
        """Tests setting the name and body using the Notification class Constructor."""
        # Create a new Notification using the Constructor to set the note name and body
        note = Notification("TestNote", 5, "TestNoteType")

        # test assertions
        self.assertTrue(note.name == "TestNote", "Expecting note.name == 'TestNote'")
        self.assertTrue(note.body == 5, "Expecting note.body == 5")
        self.assertTrue(note.type == "TestNoteType", "Expecting note.type == 'TestNoteType'")


if __name__ == '__main__':
    unittest.main()
