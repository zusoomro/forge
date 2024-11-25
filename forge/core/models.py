from django.db import models
from django.conf import settings

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
    updating ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class JournalEntry(TimeStampedModel):
    """
    Represents a single journal entry.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    content = models.TextField()

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Entries'

    def __str__(self):
        return self.title
