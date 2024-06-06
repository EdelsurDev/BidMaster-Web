from rest_framework import serializers
from usuarios.models import Usuario
from .models import Tender
from usuarios.serializers import UsuarioSerializer


class TenderSerializer(serializers.ModelSerializer):
    assigned_user = UsuarioSerializer()

    class Meta:
        model = Tender
        fields = [
            'id', 'planificacion_slug', 'convocatoria_slug', 'adjudicacion_slug', 'precalificacion_slug', 'convenio_slug',
            'nro_licitacion', 'nombre_licitacion', 'tipo_procedimiento', 'categoria', 'convocante', '_etapa_licitacion',
            'etapa_licitacion', 'fecha_entrega_oferta', 'tipo_licitacion', 'fecha_estimada', 'fecha_publicacion_convocatoria',
            'geo', 'assigned_user'
        ]

class AssignTenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tender
        fields = ['assigned_user']
