from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.db import transaction
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django import forms
from .models import User, Tenant, Event, SubEvent, Team, Ticket, Announcement
from .serializers import (
    UserSerializer, TenantSerializer, EventSerializer, SubEventSerializer,
    TeamSerializer, TicketSerializer, AnnouncementSerializer, LoginSerializer
)

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # Set default tenant
        tenant, created = Tenant.objects.get_or_create(name='Default Tenant')
        user.tenant = tenant
        if commit:
            user.save()
        return user

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = LoginSerializer

class CustomTokenRefreshView(TokenRefreshView):
    pass

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsAdminUser]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(tenant=self.request.user.tenant)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, tenant=self.request.user.tenant)

class SubEventViewSet(viewsets.ModelViewSet):
    queryset = SubEvent.objects.all()
    serializer_class = SubEventSerializer
    permission_classes = [IsAuthenticated]

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Team.objects.filter(event__tenant=self.request.user.tenant)

    @action(detail=True, methods=['post'])
    def join_team(self, request, pk=None):
        team = self.get_object()
        user = request.user
        if team.members.count() >= team.max_size:
            return Response({'error': 'Team is full'}, status=status.HTTP_400_BAD_REQUEST)
        if user in team.members.all():
            return Response({'error': 'Already a member'}, status=status.HTTP_400_BAD_REQUEST)
        team.members.add(user)
        return Response({'message': 'Joined team successfully'})

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def purchase(self, request):
        event_id = request.data.get('event_id')
        sub_event_id = request.data.get('sub_event_id')
        team_id = request.data.get('team_id')

        try:
            with transaction.atomic():
                event = Event.objects.get(id=event_id, tenant=request.user.tenant)
                sub_event = None
                team = None

                if sub_event_id:
                    sub_event = SubEvent.objects.get(id=sub_event_id, event=event)
                    if sub_event.capacity <= Ticket.objects.filter(sub_event=sub_event).count():
                        raise ValidationError('Sub-event is full')

                if team_id:
                    team = Team.objects.get(id=team_id, event=event)
                    if team.members.count() < team.min_size:
                        raise ValidationError('Team does not meet minimum size')

                if event.capacity <= Ticket.objects.filter(event=event).count():
                    raise ValidationError('Event is full')

                ticket = Ticket.objects.create(
                    user=request.user,
                    event=event,
                    sub_event=sub_event,
                    team=team
                )
                serializer = self.get_serializer(ticket)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (Event.DoesNotExist, SubEvent.DoesNotExist, Team.DoesNotExist):
            return Response({'error': 'Invalid IDs'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Announcement.objects.filter(event__tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# Frontend Views

def home(request):
    events = Event.objects.all().order_by('date')
    return render(request, 'home.html', {'events': events})

def events_list(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})

def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'event_detail.html', {'event': event})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def create_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date_str = request.POST.get('date')
        location = request.POST.get('location')
        capacity = request.POST.get('capacity')
        from datetime import datetime
        date = datetime.fromisoformat(date_str)
        event = Event.objects.create(
            title=title,
            description=description,
            date=date,
            location=location,
            capacity=capacity,
            created_by=request.user,
            tenant=request.user.tenant
        )
        messages.success(request, 'Event created successfully!')
        return redirect('home')
    return render(request, 'create_event.html')

def my_tickets(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'my_tickets.html', {'tickets': tickets})

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, created_by=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date_str = request.POST.get('date')
        location = request.POST.get('location')
        capacity = request.POST.get('capacity')
        from datetime import datetime
        date = datetime.fromisoformat(date_str)
        event.title = title
        event.description = description
        event.date = date
        event.location = location
        event.capacity = capacity
        event.save()
        messages.success(request, 'Event updated successfully!')
        return redirect('home')
    return render(request, 'edit_event.html', {'event': event})

@login_required
def purchase_ticket(request, event_id):
    if request.method == 'POST':
        event = Event.objects.get(id=event_id)
        ticket = Ticket.objects.create(user=request.user, event=event)
        messages.success(request, 'Ticket purchased successfully!')
        return redirect('home')
    return redirect('home')
