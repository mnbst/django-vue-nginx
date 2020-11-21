from django.core.management import call_command
from django.test import TestCase


class UpdateFirestoreTest(TestCase):
    def test_command(self):
        call_command("update_firestore")
        self.assertIn("Expected output", container={1: 1})
