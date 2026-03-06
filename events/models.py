from django.db import models
from django.core.validators import EmailValidator


class Category(models.Model):
    """Category model for organizing events"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_event_count(self):
        return self.events.count()


class Event(models.Model):
    """Event model with category and participant relationships"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events'
    )
    participants = models.ManyToManyField(
        'Participant',
        related_name='events',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return self.name

    def get_participant_count(self):
        return self.participants.count()

    def is_past(self):
        from django.utils import timezone
        from datetime import datetime
        event_datetime = datetime.combine(self.date, self.time)
        if timezone.is_aware(event_datetime):
            return event_datetime < timezone.now()
        return event_datetime < datetime.now()

    def is_upcoming(self):
        return not self.is_past()

    def is_today(self):
        from django.utils import timezone
        return self.date == timezone.now().date()


class Participant(models.Model):
    """Participant model with many-to-many relationship to events"""
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_event_count(self):
        return self.events.count()
