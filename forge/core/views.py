from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import JournalEntry
from .forms import JournalEntryForm


class JournalEntryListView(LoginRequiredMixin, ListView):
    """
    Displays a list of journal entries for the logged-in user.
    """
    model = JournalEntry
    template_name = 'core/journal_entry_list.html'
    context_object_name = 'entries'

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user).order_by('-created')


class JournalEntryDetailView(LoginRequiredMixin, DetailView):
    """
    Displays the details of a specific journal entry.
    """
    model = JournalEntry
    template_name = 'core/journal_entry_detail.html'
    context_object_name = 'entry'

    def get_queryset(self):
        # Ensure the user can only view their own entries
        return JournalEntry.objects.filter(user=self.request.user)


class JournalEntryCreateView(LoginRequiredMixin, CreateView):
    """
    Handles creating a new journal entry.
    """
    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'core/journal_entry_form.html'
    success_url = reverse_lazy('core:journal_entry_list')

    def form_valid(self, form):
        # Automatically associate the entry with the logged-in user
        form.instance.user = self.request.user
        return super().form_valid(form)


class JournalEntryUpdateView(LoginRequiredMixin, UpdateView):
    """
    Handles updating an existing journal entry.
    """
    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'core/journal_entry_form.html'
    success_url = reverse_lazy('core:journal_entry_list')

    def get_queryset(self):
        # Ensure the user can only update their own entries
        return JournalEntry.objects.filter(user=self.request.user)


class JournalEntryDeleteView(LoginRequiredMixin, DeleteView):
    """
    Handles deleting a journal entry.
    """
    model = JournalEntry
    template_name = 'core/journal_entry_confirm_delete.html'
    success_url = reverse_lazy('core:journal_entry_list')

    def get_queryset(self):
        # Ensure the user can only delete their own entries
        return JournalEntry.objects.filter(user=self.request.user)
