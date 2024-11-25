from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from forge.core.models import JournalEntry

class JournalEntryViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="password123")
        self.other_user = get_user_model().objects.create_user(username="otheruser", password="password123")
        self.entry = JournalEntry.objects.create(
            user=self.user,
            title="Test Entry",
            content="This is a test journal entry."
        )

    def test_list_view(self):
        """Test that the list view displays only the logged-in user's entries."""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("core:journal_entry_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Entry")
        self.assertNotContains(response, "This is not your entry.")

    def test_detail_view(self):
        """Test that the detail view displays the correct journal entry."""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("core:journal_entry_detail", kwargs={"pk": self.entry.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Entry")

    def test_create_view(self):
        """Test that a logged-in user can create a journal entry."""
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse("core:journal_entry_create"), {
            "title": "New Entry",
            "content": "This is a new entry.",
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertEqual(JournalEntry.objects.last().title, "New Entry")

    def test_update_view(self):
        """Test that a user can update their own journal entry."""
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse("core:journal_entry_update", kwargs={"pk": self.entry.pk}), {
            "title": "Updated Entry",
            "content": "This is the updated content.",
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.title, "Updated Entry")

    def test_delete_view(self):
        """Test that a user can delete their own journal entry."""
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse("core:journal_entry_delete", kwargs={"pk": self.entry.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(JournalEntry.objects.filter(pk=self.entry.pk).exists())

    def test_permission_on_other_users_entry(self):
        """Test that a user cannot access or modify another user's entries."""
        self.client.login(username="otheruser", password="password123")
        response = self.client.get(reverse("core:journal_entry_detail", kwargs={"pk": self.entry.pk}))
        self.assertEqual(response.status_code, 404)

        response = self.client.post(reverse("core:journal_entry_update", kwargs={"pk": self.entry.pk}), {
            "title": "Hacked Entry",
            "content": "This should not be allowed.",
        })
        self.assertEqual(response.status_code, 404)

        response = self.client.post(reverse("core:journal_entry_delete", kwargs={"pk": self.entry.pk}))
        self.assertEqual(response.status_code, 404)
