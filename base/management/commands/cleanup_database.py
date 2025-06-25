"""
Django management command for comprehensive database cleanup.
"""

from django.core.management.base import BaseCommand
from base.models import Topic, Room


class Command(BaseCommand):
    """Clean up orphaned data and maintain database integrity."""
    
    help = 'Clean up orphaned data and maintain database integrity'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Verbose output',
        )

    def handle(self, *args, **options):
        verbose = options['verbose']
        
        orphaned_topics = Topic.objects.filter(room__isnull=True)
        topic_count = orphaned_topics.count()
        
        if topic_count > 0:
            if verbose:
                self.stdout.write(f'Found {topic_count} orphaned topics:')
                for topic in orphaned_topics:
                    self.stdout.write(f'  - {topic.name}')
            
            orphaned_topics.delete()
            self.stdout.write(
                self.style.SUCCESS(f'Cleaned up {topic_count} orphaned topics')
            )
        else:
            if verbose:
                self.stdout.write(
                    self.style.SUCCESS('No orphaned topics found')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Database cleanup completed successfully')
        )
