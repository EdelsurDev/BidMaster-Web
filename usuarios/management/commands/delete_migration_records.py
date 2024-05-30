from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Delete migration records for specified apps'

    def handle(self, *args, **options):
        apps_to_delete = ['usuarios', 'admin']
        with connection.cursor() as cursor:
            for app in apps_to_delete:
                cursor.execute("DELETE FROM django_migrations WHERE app=%s", [app])
        self.stdout.write(self.style.SUCCESS('Successfully deleted migration records for apps: {}'.format(', '.join(apps_to_delete))))