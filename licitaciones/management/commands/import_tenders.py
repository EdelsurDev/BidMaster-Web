import csv
import datetime
from django.core.management.base import BaseCommand
from licitaciones.models import Tender
from django.utils import timezone

class Command(BaseCommand):
    """
    Clase para un comando personalizado que importa datos de licitaciones desde un CSV a la Base de datos del sistema.

    Métodos:
        add_arguments(parser): Añade argumentos al parser del comando.
        handle(*args, **kwargs): Maneja la lógica principal del comando.
        parse_date(date_str): Parsea una cadena de fecha y hora en un objeto datetime consciente de zona horaria.
    """

    def add_arguments(self, parser):
        """
        Añade argumentos al parser del comando.

        Args:
            parser (ArgumentParser): El parser de argumentos.
        """
        parser.add_argument('csv_file', type=str, help='La ruta al archivo CSV')

    def handle(self, *args, **kwargs):
        """
        Maneja la lógica principal del comando.

        Lee los datos de licitaciones desde un archivo CSV y los guarda en la base de datos.

        Args:
            *args: Argumentos posicionales.
            **kwargs: Argumentos de palabra clave.
        """
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
        """
        Parsea una cadena de fecha y hora en un objeto datetime consciente de zona horaria.

        Args:
            date_str (str): La cadena de fecha y hora en formato '%Y-%m-%d %H:%M:%S'.

        Returns:
            datetime: El objeto datetime consciente de zona horaria, o None si la cadena está vacía o es inválida.
        """
        try:
            if date_str:
                # Convierte la cadena en un objeto datetime naive
                dt = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                # Hace que el objeto datetime sea consciente de la zona horaria actual
                dt = timezone.make_aware(dt, timezone.get_default_timezone())
                return dt
            return None
        except ValueError:
            return None
