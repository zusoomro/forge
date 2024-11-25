from django.test import TestCase
from django.contrib.auth import get_user_model
from forge.core.models import JournalEntry

class JournalEntryModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="password123")
        self.entry = JournalEntry.objects.create(
            user=self.user,
            title="Test Entry",
            content="This is a test journal entry."
        )

    def test_entry_creation(self):
        """Test that a journal entry is created correctly."""
        self.assertEqual(self.entry.title, "Test Entry")
        self.assertEqual(self.entry.content, "This is a test journal entry.")
        self.assertEqual(self.entry.user, self.user)

    def test_entry_string_representation(self):
        """Test the string representation of a journal entry."""
        self.assertEqual(str(self.entry), "Test Entry")
