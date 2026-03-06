from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import date, datetime
from .models import Event, Participant, Category
from .forms import (
    EventForm, ParticipantForm, CategoryForm,
    EventFilterForm, SearchForm, ParticipantSelectionForm
)


# ==================== CATEGORY VIEWS ====================

def category_list(request):
    """List all categories"""
    categories = Category.objects.all().annotate(event_count=Count('events'))
    return render(request, 'events/category_list.html', {
        'categories': categories,
        'page_title': 'Categories'
    })


def category_create(request):
    """Create a new category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'events/category_form.html', {
        'form': form,
        'page_title': 'Create Category'
    })


def category_update(request, pk):
    """Update an existing category"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'events/category_form.html', {
        'form': form,
        'category': category,
        'page_title': 'Edit Category'
    })


def category_delete(request, pk):
    """Delete a category"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    return render(request, 'events/category_confirm_delete.html', {
        'category': category
    })


# ==================== EVENT VIEWS ====================

def event_list(request):
    """
    List all events with:
    - Optimized fetching using select_related for category
    - Optimized fetching using prefetch_related for participants
    - Search functionality using request.GET and icontains
    - Filter by category
    - Filter by date range
    """
    # Initialize querysets with optimized queries
    events = Event.objects.select_related('category').prefetch_related('participants')

    # Search functionality
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('q')
        if search_query:
            events = events.filter(
                Q(name__icontains=search_query) |
                Q(location__icontains=search_query)
            )

    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        events = events.filter(category_id=category_id)

    # Filter by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        events = events.filter(date__gte=start_date)
    if end_date:
        events = events.filter(date__lte=end_date)

    # Get all categories for filter dropdown
    categories = Category.objects.all()

    return render(request, 'events/event_list.html', {
        'events': events,
        'categories': categories,
        'search_form': search_form,
        'page_title': 'Events'
    })


def event_detail(request, pk):
    """Display detailed information for an event including all participants"""
    # Optimized query with select_related and prefetch_related
    event = get_object_or_404(
        Event.objects.select_related('category').prefetch_related('participants'),
        pk=pk
    )
    return render(request, 'events/event_detail.html', {
        'event': event,
        'page_title': event.name
    })


def event_create(request):
    """Create a new event"""
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {
        'form': form,
        'page_title': 'Create Event'
    })


def event_update(request, pk):
    """Update an existing event"""
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {
        'form': form,
        'event': event,
        'page_title': 'Edit Event'
    })


def event_delete(request, pk):
    """Delete an event"""
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {
        'event': event
    })


def event_participants(request, pk):
    """Manage participants for an event"""
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = ParticipantSelectionForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Participants updated successfully!')
            return redirect('event_detail', pk=pk)
    else:
        form = ParticipantSelectionForm(instance=event)
    return render(request, 'events/event_participants.html', {
        'form': form,
        'event': event,
        'page_title': f'Manage Participants - {event.name}'
    })


# ==================== PARTICIPANT VIEWS ====================

def participant_list(request):
    """List all participants"""
    participants = Participant.objects.prefetch_related('events').all()
    return render(request, 'events/participant_list.html', {
        'participants': participants,
        'page_title': 'Participants'
    })


def participant_create(request):
    """Create a new participant"""
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Participant created successfully!')
            return redirect('participant_list')
    else:
        form = ParticipantForm()
    return render(request, 'events/participant_form.html', {
        'form': form,
        'page_title': 'Create Participant'
    })


def participant_update(request, pk):
    """Update an existing participant"""
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Participant updated successfully!')
            return redirect('participant_list')
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'events/participant_form.html', {
        'form': form,
        'participant': participant,
        'page_title': 'Edit Participant'
    })


def participant_delete(request, pk):
    """Delete a participant"""
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        participant.delete()
        messages.success(request, 'Participant deleted successfully!')
        return redirect('participant_list')
    return render(request, 'events/participant_confirm_delete.html', {
        'participant': participant
    })


# ==================== DASHBOARD VIEWS ====================

def dashboard(request):
    """
    Organizer Dashboard with:
    - Total number of participants (aggregate query)
    - Total number of events
    - Number of past events
    - Number of upcoming events
    - Today's events listing
    - Interactive stats that filter displayed data
    """
    today = timezone.now().date()

    # Get filter parameter for interactivity
    filter_type = request.GET.get('filter', 'all')

    # Aggregate query for total participants
    total_participants = Participant.objects.count()

    # Total events
    total_events = Event.objects.count()

    # Past events count
    past_events_count = Event.objects.filter(date__lt=today).count()

    # Upcoming events count
    upcoming_events_count = Event.objects.filter(date__gte=today).count()

    # Today's events - optimized query
    today_events = Event.objects.select_related('category').filter(date=today)

    # Filter events based on filter_type for interactive display
    if filter_type == 'past':
        display_events = Event.objects.select_related('category').filter(date__lt=today)
    elif filter_type == 'upcoming':
        display_events = Event.objects.select_related('category').filter(date__gte=today)
    elif filter_type == 'today':
        display_events = today_events
    else:
        # Default: show all events
        display_events = Event.objects.select_related('category').all()

    # Get recent events for context
    recent_events = Event.objects.select_related('category').order_by('-date', '-time')[:5]

    context = {
        'total_participants': total_participants,
        'total_events': total_events,
        'past_events_count': past_events_count,
        'upcoming_events_count': upcoming_events_count,
        'today_events': today_events,
        'display_events': display_events,
        'recent_events': recent_events,
        'filter_type': filter_type,
        'today': today,
        'page_title': 'Dashboard'
    }

    return render(request, 'events/dashboard.html', context)


# ==================== HOME VIEW ====================

def home(request):
    """Home page redirecting to event list"""
    return redirect('event_list')
