"""
Django management command to cleanup empty topics.
"""

from django.core.management.base import BaseCommand
from base.models import Topic


class Command(BaseCommand):
    """Delete topics that have no associated rooms."""
    help = 'Delete topics that have no associated rooms'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting anything',
        )

    def handle(self, *args, **options):
        empty_topics = Topic.objects.filter(room__isnull=True)
        count = empty_topics.count()
        
        if options['dry_run']:
            self.stdout.write(
                self.style.WARNING(f'Dry run: Would delete {count} empty topics:')
            )
            for topic in empty_topics:
                self.stdout.write(f'  - {topic.name}')
        else:
            deleted_topics = []
            for topic in empty_topics:
                deleted_topics.append(topic.name)
            
            empty_topics.delete()
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted {count} empty topics:')
            )
            for topic_name in deleted_topics:
                self.stdout.write(f'  - {topic_name}')
