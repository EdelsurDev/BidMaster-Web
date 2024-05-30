import csv
import datetime
from django.core.management.base import BaseCommand
from licitaciones.models import Tender
from django.utils import timezone

class Command(BaseCommand):
    help = 'Import tenders from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                tender = Tender(
                    planificacion_slug=row['planificacion_slug'],
                    convocatoria_slug=row['convocatoria_slug'],
                    adjudicacion_slug=row['adjudicacion_slug'],
                    precalificacion_slug=row['precalificacion_slug'],
                    convenio_slug=row['convenio_slug'],
                    nro_licitacion=row['nro_licitacion'],
                    nombre_licitacion=row['nombre_licitacion'],
                    tipo_procedimiento=row['tipo_procedimiento'],
                    categoria=row['categoria'],
                    convocante=row['convocante'],
                    _etapa_licitacion=row['_etapa_licitacion'],
                    etapa_licitacion=row['etapa_licitacion'],
                    fecha_entrega_oferta=self.parse_date(row['fecha_entrega_oferta']),
                    tipo_licitacion=row['tipo_licitacion'],
                    fecha_estimada=self.parse_date(row['fecha_estimada']),
                    fecha_publicacion_convocatoria=self.parse_date(row['fecha_publicacion_convocatoria']),
                    geo=row['geo']
                )
                tender.save()
        self.stdout.write(self.style.SUCCESS('Successfully imported data'))

    def parse_date(self, date_str):
        try:
            if date_str:
                # Convert the string to a naive datetime object
                dt = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                # Make the datetime object aware by localizing it to the current timezone
                dt = timezone.make_aware(dt, timezone.get_default_timezone())
                return dt
            return None
        except ValueError:
            return None