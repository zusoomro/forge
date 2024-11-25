from django.urls import path
from .views import (
    JournalEntryListView,
    JournalEntryDetailView,
    JournalEntryCreateView,
    JournalEntryUpdateView,
    JournalEntryDeleteView,
)

app_name = 'core'

urlpatterns = [
    path('', JournalEntryListView.as_view(), name='journal_entry_list'),
    path('<int:pk>/', JournalEntryDetailView.as_view(), name='journal_entry_detail'),
    path('create/', JournalEntryCreateView.as_view(), name='journal_entry_create'),
    path('<int:pk>/update/', JournalEntryUpdateView.as_view(), name='journal_entry_update'),
    path('<int:pk>/delete/', JournalEntryDeleteView.as_view(), name='journal_entry_delete'),
]
