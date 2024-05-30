from django.db import models

class Tender(models.Model):
    planificacion_slug = models.CharField(max_length=1024, blank=True, default='')
    convocatoria_slug = models.CharField(max_length=1024, blank=True, default='')
    adjudicacion_slug = models.CharField(max_length=1024, blank=True, default='')
    precalificacion_slug = models.CharField(max_length=1024, blank=True, default='')
    convenio_slug = models.CharField(max_length=1024, blank=True, default='')
    nro_licitacion = models.CharField(max_length=1024, blank=True, default='')
    nombre_licitacion = models.CharField(max_length=1024, blank=True, default='')
    tipo_procedimiento = models.CharField(max_length=1024, blank=True, default='')
    categoria = models.CharField(max_length=1024, blank=True, default='')
    convocante = models.CharField(max_length=1024, blank=True, default='')
    _etapa_licitacion = models.CharField(max_length=1024, blank=True, default='')
    etapa_licitacion = models.CharField(max_length=1024, blank=True, default='')
    fecha_entrega_oferta = models.DateTimeField(null=True, blank=True)
    tipo_licitacion = models.CharField(max_length=1024, blank=True, default='')
    fecha_estimada = models.DateTimeField(null=True, blank=True)
    fecha_publicacion_convocatoria = models.DateTimeField(null=True, blank=True)
    geo = models.CharField(max_length=1024, blank=True, default='')

    def __str__(self):
        return self.nombre_licitacion
    
class ProcurementCategory(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

# Create your models here.

# class Documento:
#     FechaPublicacion: models.DateTimeField()
#     TipoDocumentoDetallado: models.CharField(max_lenght = 100)
#     Idioma: models.CharField(max_lenght = 10)
#     Id: models.CharField(max_lenght = 100)
#     Titulo: models.CharField(max_lenght = 50)
#     Url: models.CharField(max_lenght = 500)
#     TipoDocumento: models.CharField(max_lenght = 10)
#     Format: models.CharField(max_lenght = 50)
    
# class Requerimiento:
#     ValorEsperado: models.CharField(max_lenght = 200)
#     Id: models.CharField(max_lenght = 50)
#     Titulo: models.CharField(max_lenght = 100)
    
# class Criterio:
#     Id: models.CharField(max_lenght = 20)
#     Descripcion: models.CharField(max_lenght = 500)
#     Fuente: models.CharField(max_lenght = 50)
#     Titulo: models.CharField(max_lenght = 50)
#     Requerimientos: List[Requerimiento]
    
# class EntregaOferta:
#     Fecha: models.DateTimeField()
#     DireccionEntrega: models.CharField(max_lenght = 100)
    
# class Periodo:
#     FechaInicio: models.DateTimeField()
#     FechaFin: models.DateTimeField()
#     DuracionEnDias: models.IntegerField(default = 0)
    
# class Consulta:
#     Fecha: models.DateTimeField()
#     Respuesta: models.CharField(max_lenght = 2000)
#     Id: models.CharField(max_lenght = 100)
#     Titulo: models.CharField(max_lenght = 500)
#     FechaRespuesta: models.DateTimeField()
    
# class Atributo:
#     Id: models.CharField(max_lenght = 50)
#     Nombre: models.CharField(max_lenght = 100)
#     Valor: models.CharField(max_lenght = 5)
    
# class Monto:
#     Cantidad: models.DoubleField(default = 0.0)
#     Moneda: models.CharField(max_lenght = 5)
    
# class Lote:
#     AbastecimientoInstantaneo: models.BooleanField(default = False)
#     Estado: models.CharField(max_lenght = 20)
#     Atributos: List[Atributo]
#     Id: models.CharField(max_lenght = 10)
#     Titulo: models.CharField(max_lenght = 50)
#     Monto: Monto
    
# class ClasificacionItem:
#     Id: models.IntegerField()
#     Esquema: models.CharField(max_lenght = 10)
#     Descripcion: models.CharField(max_lenght = 100)
#     Uri: models.CharField(max_lenght = 500)
    
# class Unidad:
#     Nombre: models.CharField(max_lenght = 20)
#     Id: models.CharField(max_lenght = 3)
#     Monto: Monto
    
# class Item:
#     Id: models.CharField(max_lenght = 30)
#     Descripcion: models.CharField(max_lenght = 100)
    
# class ItemPlanificado(Item):
#     ClasificacionItem: ClasificacionItem
    
# class ItemCotizado(Item):
#     ClasificacionNivel5: ClasificacionItem
#     ClasificacionesAdicionales: List[ClasificacionItem]
#     Unidad: Unidad
#     Cantidad: models.IntegerField(default = 1)
#     LoteRelacionado: models.CharField(max_lenght = 200)
#     Atributos : List[Atributo]
    
# class Proveedor:
#     Id: models.CharField(max_lenght = 40)
#     Nombre: models.CharField(max_lenght = 100)

# class ClasificacionesPresupuestales:
#     Cdp: models.CharField(max_lenght = 50)
#     TipoPrograma: models.CharField(max_lenght = 10)
#     Subprograma: models.CharField(max_lenght = 5)
#     FuenteFinanciamiento: models.CharField(max_lenght = 3)
#     Entidad: models.CharField(max_lenght = 50)
#     Programa: models.CharField(max_lenght = 10)
#     Proyecto: models.CharField(max_lenght = 20)
#     Departamento: models.CharField(max_lenght = 100)
#     Nivel: models.CharField(max_lenght = 5)
#     Anio: models.CharField(max_lenght = 4)
#     Financiador: models.CharField(max_lenght = 30)

# class Medidas:
#     MontoUtilizar: Monto
#     MontoUtilizado: Monto

# class DetallePresupuesto:
#     Id: models.CharField(max_lenght = 50)
#     ClasificacionesPresupuestales: ClasificacionesPresupuestales
#     Periodo: Periodo
#     Medidas: Medidas
#     Proveedor: Proveedor
    
# class Presupuesto:
#     Monto: Monto
#     DetallesPresuesto: List[DetallePresupuesto]
#     Descripcion: models.CharField(max_lenght = 300)
    
# class Planificacion:
#     Id: models.CharField(max_lenght = 20)
#     FechaEstimada: models.DateTimeField()
#     ItemsPlanificados: List[ItemPlanificado]
#     Presupuesto: Presupuesto
    
# class Categoria:
#     Id: models.CharField(max_lenght = 10)
#     Nombre: models.CharField(max_lenght = 100)
#     FechaCreacion: models.DateTimeField()
    
# class Usuario:
#     Nombre: models.CharField(max_lenght = 100)
#     Telefono: models.CharField(max_lenght = 20)
#     #Admin site de Django?
#     Roles: List[Rol]
#     Email: models.CharField(max_lenght = 20)
#     #Primera idea: palabras separadas por comas, revisar
#     Keywords: models.CharField(max_lenght = 1000)
#     Rubros: List[Categoria]
    
# class IdentificadorConvocante:
#     Esquema: models.CharField(max_lenght = 15)
#     Id: models.CharField(max_lenght = 5)
#     NombreLegal: models.CharField(max_lenght = 100)
    
# class DetallesConvocante:
#     Nivel: models.CharField(max_lenght = 5)
#     TipoEntidad: models.CharField(max_lenght = 10)
#     Tipo: models.CharField(max_lenght = 20)
    
# class Convocante:
#     Id: models.CharField(max_lenght = 20)
#     Nombre: models.CharField(max_lenght = 50)
#     Identificador: IdentificadorConvocante
#     Detalles: DetallesConvocante
#     FechaCreacion: models.DateTimeField()
    

# class Licitacion:
#     Titulo: models.CharField(max_lenght = 50)
#     Categoria: Categoria
#     Documentos: List[Documento]
#     Convocante: Convocante
#     CriteriosOferta: List[Criterio]
#     InicioPeriodoAdjudicacion: models.DateTimeField()
#     EntregaOferta: EntregaOferta
#     ObjetoLlamado: models.CharField(max_lenght = 10)
#     PeriodoConsultas: Periodo
#     Consultas: List[Consulta]
#     TieneConsultas: models.BooleanField(default = False)
#     Lotes: List[Lote]
#     Items: List[ItemCotizado]
#     Uoc: models.CharField(max_lenght = 30)
#     Modalidad: models.CharField(max_lenght = 15)
#     EstadoConvocatoria: models.CharField(max_lenght = 10)
#     PeriodoAdjudicacion: Periodo
#     CriterioAdjudicacion: models.CharField(max_lenght = 40)
#     CriterioElegible: models.CharField(max_lenght = 50)
#     Monto: Monto
#     PeriodoLicitacion: Periodo
#     Invitados: List[Proveedor]
#     FechaInicio: models.DateTimeField()
#     FechaPublicacion: models.DateTimeField()
#     Planificacion: Planificacion
#     Responsable: Usuario
#     Estado: models.CharField(max_lenght = 10)
