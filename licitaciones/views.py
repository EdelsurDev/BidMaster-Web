from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

import requests
from django.http import JsonResponse, Http404, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import Tender
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
from usuarios.models import RolePermission
from usuarios.mixins import PermissionRequiredMixin
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from usuarios.models import Usuario
from .serializers import TenderSerializer
from usuarios.decorators import firebase_login_required


# Create your views here.

def home_view(request):
    return render(request, 'home.html')

class ProcurementCategoriesView(PermissionRequiredMixin, APIView):
    """
    Vista para buscar categorías.

    Esta vista permite ver los distintos tipos de categorías de licitaciones y planificaciones.

    Métodos:
        get(request, *args, **kwargs): Maneja las solicitudes GET para buscar categorías.
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('nombre', openapi.IN_QUERY, description="Nombre de la categoría para filtrar", type=openapi.TYPE_STRING)
        ],
        responses={
            200: openapi.Response('OK', openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_STRING, description='ID de la categoría'),
                        'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la categoría'),
                    }
                )
            )),
            404: "Not Found"
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Maneja las solicitudes GET para buscar categorías.

        Args:
            request (HttpRequest): El objeto de solicitud HTTP.

        Returns:
            JsonResponse: Una respuesta JSON que contiene los datos de las categorías,
            incluyendo el estado HTTP.
        """
        url = 'https://www.contrataciones.gov.py/datos/api/v3/doc/parameters/procurementCategories'
        response = requests.get(url)
        data = response.json()

        categories = data.get('list', [])

        category_id = kwargs.get('id')
        if category_id:
            category = next((item for item in categories if item["id"] == category_id), None)
            if category is None:
                raise Http404("Procurement category not found")
            return JsonResponse(category, safe=False)

        nombre_keyword = request.GET.get('nombre')
        if nombre_keyword:
            filtered_categories = [item for item in categories if nombre_keyword.lower() in item["nombre"].lower()]
            return JsonResponse(filtered_categories, safe=False)

        return JsonResponse(categories, safe=False)

@method_decorator(firebase_login_required, name='dispatch')
class PlanningDetailView(PermissionRequiredMixin, APIView):
    """
    Vista para obtener los detalles de una planificación específica.

    Esta vista permite a los usuarios recuperar los detalles de una planificación utilizando su ID.

    Atributos:
        required_permission (str): El permiso requerido para acceder a esta vista.
        permission_classes (list): Lista de clases de permisos requeridos.
    
    Métodos:
        get(request, *args, id, **kwargs): Maneja las solicitudes GET para obtener los detalles de una planificación.
    """
    required_permission = 'view_planning_detail'
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID de la planificación", type=openapi.TYPE_STRING),
        ],
        responses={200: openapi.Response('OK', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING, description='ID de la planificación'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la planificación'),
            }
        )),
            404: "Not Found"
        }
    )
    def get(self, request, *args, id, **kwargs):
        """
        Maneja las solicitudes GET para obtener los detalles de una planificación.

        Args:
            request (HttpRequest): El objeto de solicitud HTTP.
            id (int): El ID de la planificación.

        Returns:
            JsonResponse: Una respuesta JSON que contiene los detalles de la planificación
            y el estado HTTP.
        """
        url = f'https://www.contrataciones.gov.py/datos/api/v3/doc/planning/{id}'
        response = requests.get(url)
        if response.status_code == 404:
            raise Http404("Tender not found")

        return JsonResponse(response.json(), status=status.HTTP_200_OK)

@method_decorator(firebase_login_required, name='dispatch')    
class PlannedTenderSearchView(PermissionRequiredMixin, APIView):
    """
    Vista para buscar licitaciones planificadas.

    Esta vista permite a los usuarios buscar licitaciones en la etapa de planificación
    según varios criterios, como categoría, palabra clave, fecha de inicio y fecha de fin.
    """
    required_permission = 'view_planning'
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('categoria', openapi.IN_QUERY, description="Categoría de la licitación", type=openapi.TYPE_STRING),
            openapi.Parameter('keyword', openapi.IN_QUERY, description="Palabra clave para buscar en el nombre de la licitación", type=openapi.TYPE_STRING),
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Fecha de inicio (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="Fecha de fin (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, description="Número de página", type=openapi.TYPE_INTEGER, default=1),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Tamaño de la página", type=openapi.TYPE_INTEGER, default=10),
        ],
        responses={200: openapi.Response('OK', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'tenders': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT)),
                'page': openapi.Schema(type=openapi.TYPE_INTEGER, description='Número de página actual'),
                'pages': openapi.Schema(type=openapi.TYPE_INTEGER, description='Número total de páginas'),
                'total_tenders': openapi.Schema(type=openapi.TYPE_INTEGER, description='Número total de licitaciones'),
                'has_next': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Indica si hay una página siguiente'),
                'has_previous': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Indica si hay una página anterior'),
            }
        )),
            404: "Not Found"
        }
    )

    def get(self, request):
        """
        Maneja las solicitudes GET para buscar licitaciones planificadas.

        Args:
            request (HttpRequest): El objeto de solicitud HTTP.

        Returns:
            JsonResponse: Una respuesta JSON que contiene los datos de las licitaciones planificadas,
            incluyendo la paginación y el estado HTTP.
        """
        categoria = request.GET.get('categoria')
        keyword = request.GET.get('keyword')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)

        tenders = Tender.objects.filter(etapa_licitacion='Planificada')

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            tenders = tenders.filter(fecha_publicacion_convocatoria__gte=start_date)

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            tenders = tenders.filter(fecha_publicacion_convocatoria__lte=end_date)

        if categoria and keyword:
            tenders = tenders.filter(
                Q(categoria__icontains=categoria) & 
                Q(nombre_licitacion__icontains=keyword)
            )
        elif categoria:
            tenders = tenders.filter(categoria__icontains=categoria)
        elif keyword:
            tenders = tenders.filter(nombre_licitacion__icontains=keyword)

        tenders = tenders.order_by('-fecha_estimada')

        paginator = Paginator(tenders, page_size)
        paginated_tenders = paginator.get_page(page)

        tender_data = list(paginated_tenders.object_list.values())
        response = {
            'tenders': tender_data,
            'page': paginated_tenders.number,
            'pages': paginator.num_pages,
            'total_tenders': paginator.count,
            'has_next': paginated_tenders.has_next(),
            'has_previous': paginated_tenders.has_previous(),
        }
        return JsonResponse(response, status=status.HTTP_200_OK)

@method_decorator(firebase_login_required, name='dispatch')
class TenderDetailView(PermissionRequiredMixin, APIView):
    """
    Vista para obtener los detalles de una licitación específica.

    Esta vista permite a los usuarios recuperar los detalles de una licitación utilizando su ID.
    """
    required_permission = 'view_tender_detail'
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID de la licitación", type=openapi.TYPE_STRING),
        ],
        responses={200: openapi.Response('OK', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING, description='ID de la licitación'),
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la licitación'),
                # Add other fields as necessary
            }
        )),
            404: "Not Found"
        }
    )

    def get(self, request, id, *args, **kwargs):
        """
        Maneja las solicitudes GET para obtener los detalles de una licitación.

        Args:
            request (HttpRequest): El objeto de solicitud HTTP.
            id (int): El ID de la licitación.

        Returns:
            JsonResponse: Una respuesta JSON que contiene los detalles de la licitación
            y el estado HTTP.
        """
        url = f'https://www.contrataciones.gov.py/datos/api/v3/doc/tender/{id}'
        response = requests.get(url)
        if response.status_code == 404:
            raise Http404("Tender not found")

        return JsonResponse(response.json(), status=status.HTTP_200_OK)

@method_decorator(firebase_login_required, name='dispatch')    
class TenderSearchView(PermissionRequiredMixin, APIView):
    """
    Vista para buscar licitaciones.

    Esta vista permite a los usuarios buscar licitaciones según varios criterios, 
    como categoría, palabra clave, fecha de inicio y fecha de fin.
    """
    required_permission = 'view_tenders'
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('categoria', openapi.IN_QUERY, description="Categoría de la licitación", type=openapi.TYPE_STRING),
            openapi.Parameter('keyword', openapi.IN_QUERY, description="Palabra clave para buscar en el nombre de la licitación", type=openapi.TYPE_STRING),
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Fecha de inicio (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="Fecha de fin (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, description="Número de página", type=openapi.TYPE_INTEGER, default=1),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Tamaño de la página", type=openapi.TYPE_INTEGER, default=10),
        ],
        responses={200: openapi.Response('OK', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'tenders': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT)),
                'page': openapi.Schema(type=openapi.TYPE_INTEGER, description='Número de página actual'),
                'pages': openapi.Schema(type=openapi.TYPE_INTEGER, description='Número total de páginas'),
                'total_tenders': openapi.Schema(type=openapi.TYPE_INTEGER, description='Número total de licitaciones'),
                'has_next': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Indica si hay una página siguiente'),
                'has_previous': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Indica si hay una página anterior'),
            }
        )),
            404: "Not Found"
        }
    )

    def get(self, request):
        """
        Maneja las solicitudes GET para buscar licitaciones.

        Args:
            request (HttpRequest): El objeto de solicitud HTTP.

        Returns:
            JsonResponse: Una respuesta JSON que contiene los datos de las licitaciones,
            incluyendo la paginación y el estado HTTP.
        """
        categoria = request.GET.get('categoria')
        keyword = request.GET.get('keyword')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)

        tenders = Tender.objects.all().order_by('-fecha_publicacion_convocatoria')

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            tenders = tenders.filter(fecha_publicacion_convocatoria__gte=start_date)

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            tenders = tenders.filter(fecha_publicacion_convocatoria__lte=end_date)

        if categoria and keyword:
            tenders = tenders.filter(
                Q(categoria__icontains=categoria) & 
                Q(nombre_licitacion__icontains=keyword)
            )
        elif categoria:
            tenders = tenders.filter(categoria__icontains=categoria)
        elif keyword:
            tenders = tenders.filter(nombre_licitacion__icontains=keyword)


        paginator = Paginator(tenders, page_size)
        paginated_tenders = paginator.get_page(page)

        tender_data = list(paginated_tenders.object_list.values())
        response = {
            'tenders': tender_data,
            'page': paginated_tenders.number,
            'pages': paginator.num_pages,
            'total_tenders': paginator.count,
            'has_next': paginated_tenders.has_next(),
            'has_previous': paginated_tenders.has_previous(),
        }
        return JsonResponse(response, status=status.HTTP_200_OK)

@method_decorator(firebase_login_required, name='dispatch')    
class AssignTenderAPIView(PermissionRequiredMixin, APIView):
    """
    API para asignar o desasignar un usuario a una licitación.

    Esta vista permite a los usuarios con los permisos adecuados asignar un usuario
    a una licitación específica o desasignar un usuario de una licitación.

    Atributos:
        required_permission (str): El permiso requerido para acceder a esta vista.
        permission_classes (list): Lista de clases de permisos requeridos.
    
    Métodos:
        post(request, user_id, nro_licitacion): Asigna un usuario a una licitación.
        delete(request, nro_licitacion): Desasigna un usuario de una licitación.
    """
    required_permission = 'assign_tender'
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Asigna un usuario a una licitación.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user_id', 'nro_licitacion'],
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del usuario a asignar'),
                'nro_licitacion': openapi.Schema(type=openapi.TYPE_STRING, description='Número de licitación')
            }
        ),
        responses={
            200: openapi.Response('OK', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, description='Estado de la asignación')
                }
            )),
            404: 'Not Found'
        }
    )
    def post(self, request, user_id, nro_licitacion):
        """
        Asigna un usuario a una licitación.

        Args:
            request (HttpRequest): El objeto de solicitud HTTP.
            user_id (int): El ID del usuario a asignar.
            nro_licitacion (str): El número de la licitación.

        Returns:
            Response: Una respuesta JSON que indica el estado de la asignación.
        """
        user = get_object_or_404(Usuario, id=user_id)
        tender = get_object_or_404(Tender, nro_licitacion=nro_licitacion)
        tender.assigned_user = user
        tender.save()
        return Response({'status': 'tender assigned'}, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        operation_description="Desasigna un usuario de una licitación.",
        manual_parameters=[
            openapi.Parameter('nro_licitacion', openapi.IN_PATH, description="Número de licitación", type=openapi.TYPE_STRING)
        ],
        responses={
            200: openapi.Response('OK', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, description='Estado de la desasignación')
                }
            )),
            404: 'Not Found'
        }
    )
    def delete(self, request, user_id, nro_licitacion):
        """
        Desasigna un usuario de una licitación.

        Args:
            request (HttpRequest): El objeto de solicitud HTTP.
            nro_licitacion (str): El número de la licitación.

        Returns:
            Response: Una respuesta JSON que indica el estado de la desasignación.
        """
        tender = get_object_or_404(Tender, nro_licitacion=nro_licitacion)
        tender.assigned_user = None
        tender.save()
        return Response({'status': 'tender unassigned'}, status=status.HTTP_200_OK)


    