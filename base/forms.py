from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Room, Topic, Message, UserProfile


class CustomUserCreationForm(UserCreationForm):
    """Extended user creation form with additional profile fields."""
    
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    bio = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself...'})
    )
    location = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'City, Country'})
    )
    website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'placeholder': 'https://yourwebsite.com'})
    )
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 
            'password1', 'password2', 'bio', 'location', 'website', 'birth_date'
        )

    def save(self, commit=True):
        """Save user and create associated profile with additional fields."""
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.bio = self.cleaned_data.get('bio', '')
            profile.location = self.cleaned_data.get('location', '')
            profile.website = self.cleaned_data.get('website', '')
            profile.birth_date = self.cleaned_data.get('birth_date')
            profile.save()
        
        return user


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile information."""
    
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = UserProfile
        fields = ('bio', 'location', 'website', 'birth_date')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

    def save(self, commit=True):
        """Save profile and update associated user fields."""
        profile = super().save(commit=False)
        
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']
            if commit:
                self.user.save()
        
        if commit:
            profile.save()
        
        return profile


class RoomForm(forms.ModelForm):
    """Form for creating and editing study rooms."""
    
    topic_name = forms.CharField(
        max_length=200,
        required=True,
        label='Topic',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter or select a topic...',
            'list': 'topics-list',
            'autocomplete': 'off'
        }),
        help_text='Type a new topic or select from existing ones'
    )
    
    class Meta:
        model = Room
        fields = ['name', 'topic_name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter room name'}),
            'description': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Describe what this room is about...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.topic:
            self.fields['topic_name'].initial = self.instance.topic.name
    
    def save(self, commit=True):
        """Save room and handle topic creation/assignment."""
        room = super().save(commit=False)
        topic_name = self.cleaned_data['topic_name'].strip()
        
        topic, created = Topic.objects.get_or_create(
            name__iexact=topic_name,
            defaults={'name': topic_name}
        )
        room.topic = topic
        
        if commit:
            room.save()
        return room


class MessageForm(forms.ModelForm):
    """Form for posting messages in study rooms."""
    
    class Meta:
        model = Message
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Type your message here...',
                'class': 'message-input'
            }),
        }
        labels = {
            'body': '',
        }
