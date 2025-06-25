from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Room, Topic


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile when a new User is created."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile when the User is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        UserProfile.objects.create(user=instance)


@receiver(post_delete, sender=Room)
def cleanup_orphaned_topics(sender, instance, **kwargs):
    """Delete topics that have no rooms after a room is deleted."""
    if instance.topic:
        remaining_rooms = Room.objects.filter(topic=instance.topic).count()
        if remaining_rooms == 0:
            instance.topic.delete()
