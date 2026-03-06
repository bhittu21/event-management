from django.contrib import admin
from .models import Category, Event, Participant


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'get_event_count', 'created_at']
    search_fields = ['name', 'description']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'date', 'time', 'location', 'get_participant_count']
    list_filter = ['category', 'date']
    search_fields = ['name', 'description', 'location']
    date_hierarchy = 'date'
    ordering = ['-date', '-time']


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'get_event_count', 'created_at']
    search_fields = ['name', 'email']
    ordering = ['name']
