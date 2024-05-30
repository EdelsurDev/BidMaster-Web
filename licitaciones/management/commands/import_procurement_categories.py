import requests
from django.core.management.base import BaseCommand
from licitaciones.models import ProcurementCategory

class Command(BaseCommand):
    help = 'Import procurement categories from external API'

    def handle(self, *args, **kwargs):
        url = "https://www.contrataciones.gov.py/datos/api/v3/doc/parameters/procurementCategories"
        response = requests.get(url)
        data = response.json()

        for category in data['list']:
            ProcurementCategory.objects.update_or_create(
                id=category['id'],
                defaults={'nombre': category['nombre']}
            )

        self.stdout.write(self.style.SUCCESS('Successfully imported procurement categories'))