from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import RoomForm, MessageForm, CustomUserCreationForm, UserProfileForm
from .models import Room, Topic, Message, UserProfile


def login_page(request):
    """Handle user login."""
    form = AuthenticationForm()

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Password or user is not correct")
        else:
            messages.error(request, "Username or password is invalid")

    return render(request, "base/login.html", {"form": form})


def register_page(request):
    """Handle user registration."""
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("home")
        else:
            messages.error(request, "An error occurred during registration")

    return render(request, "base/register.html", {"form": form})


def user_profile(request, username):
    """Display user profile with rooms and messages."""
    user = get_object_or_404(User, username=username)
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    user_rooms = Room.objects.filter(host=user).order_by('-updated')[:5]
    user_messages = Message.objects.filter(user=user).order_by('-created')[:10]
    
    context = {
        'profile_user': user,
        'profile': profile,
        'user_rooms': user_rooms,
        'user_messages': user_messages,
        'is_own_profile': request.user == user
    }
    return render(request, 'base/user_profile.html', context)


@login_required(login_url="login")
def edit_profile(request):
    """Edit user profile information."""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('user-profile', username=request.user.username)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserProfileForm(instance=profile, user=request.user)
    
    return render(request, 'base/edit_profile.html', {'form': form})


@login_required(login_url="login")
def delete_profile(request):
    """Delete user account."""
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect("home")
    
    return render(request, "base/delete_profile.html")


def logout_user(request):
    """Log out the current user."""
    logout(request)
    return redirect("home")


def home(request):
    """Display home page with rooms, topics, and search functionality."""
    q = request.GET.get("q", "")
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    ).order_by('-updated', '-created')
    
    if q:
        topics = Topic.objects.filter(
            Q(name__icontains=q) & Q(room__isnull=False)
        ).annotate(room_count=Count('room')).distinct().order_by('name')
    else:
        topics = Topic.objects.filter(
            room__isnull=False
        ).annotate(room_count=Count('room')).distinct().order_by('name')
    
    room_count = rooms.count()
    
    if q:
        room_messages = Message.objects.filter(
            Q(room__topic__name__icontains=q) |
            Q(room__name__icontains=q) |
            Q(room__description__icontains=q) |
            Q(body__icontains=q)
        ).select_related('user', 'room', 'room__topic').order_by('-created')[:5]
    else:
        room_messages = Message.objects.select_related(
            'user', 'room', 'room__topic'
        ).order_by('-created')[:5]
    
    return render(
        request,
        "base/home.html",
        {
            "rooms": rooms, 
            "room_count": room_count, 
            "topics": topics,
            "room_messages": room_messages
        },
    )


def room(request, pk):
    """Display room with messages and handle new message posting."""
    room_instance = Room.objects.get(pk=pk)
    room_messages = room_instance.message_set.all().order_by('created')
    
    participant_ids = room_instance.message_set.values_list('user', flat=True).distinct()
    participants = User.objects.filter(id__in=participant_ids)
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            body = request.POST.get('body', '').strip()
            if body and len(body) <= 1000:
                Message.objects.create(
                    user=request.user,
                    room=room_instance,
                    body=body
                )
                return redirect('room', pk=room_instance.id)
            else:
                messages.error(request, "Message cannot be empty or exceed 1000 characters.")
        else:
            return redirect('login')
    
    context = {
        'room': room_instance,
        'room_messages': room_messages,
        'participants': participants
    }
    return render(request, "base/room.html", context)


@login_required(login_url="login")
def create_room(request):
    """Create a new study room."""
    form = RoomForm()
    topics = Topic.objects.all()
    
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect("home")

    return render(request, "base/room_form.html", {"form": form, "topics": topics})


@login_required(login_url="login")
def update_room(request, pk):
    """Update an existing room (host only)."""
    room = get_object_or_404(Room, id=pk)
    
    if request.user != room.host:
        messages.error(request, "You're not allowed to edit this room. Only the room host can make changes.")
        return redirect("room", pk=room.id)
    
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, "Room updated successfully!")
            return redirect("room", pk=room.id)

    return render(request, "base/room_form.html", {"form": form, "topics": topics})


@login_required(login_url="login")
def delete_room(request, pk):
    """Delete a room (host only)."""
    room = get_object_or_404(Room, id=pk)
    
    if request.user != room.host:
        messages.error(request, "You're not allowed to delete this room. Only the room host can delete it.")
        return redirect("room", pk=room.id)

    if request.method == "POST":
        room_name = room.name
        room.delete()
        messages.success(request, f"Room '{room_name}' has been deleted successfully.")
        return redirect("home")
    
    return render(request, "base/delete.html", {"obj": room})


@login_required(login_url="login")
def delete_message(request, pk):
    """Delete a message (author only)."""
    message = get_object_or_404(Message, id=pk)
    
    if request.user != message.user:
        messages.error(request, "You're not allowed to delete this message!")
        return redirect("room", pk=message.room.id)
    
    if request.method == "POST":
        room_id = message.room.id
        message.delete()
        messages.success(request, "Message deleted successfully.")
        return redirect("room", pk=room_id)
    
    return render(request, "base/delete.html", {"obj": message})


@require_http_methods(["GET"])
def get_room_messages(request, pk):
    """API endpoint to get room messages for real-time updates."""
    try:
        room_instance = Room.objects.get(pk=pk)
        messages_list = room_instance.message_set.all().order_by('created')
        
        messages_data = []
        for message in messages_list:
            messages_data.append({
                'id': message.id,
                'user': message.user.username,
                'body': message.body,
                'created': message.created.isoformat(),
                'is_host': message.user == room_instance.host,
                'is_own_message': message.user == request.user if request.user.is_authenticated else False,
            })
        
        return JsonResponse({
            'messages': messages_data,
            'count': len(messages_data)
        })
    except Room.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)
