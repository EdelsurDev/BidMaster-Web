from django.shortcuts import render
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

# Create your views here.

def home_view(request):
    return render(request, 'home.html')

@require_http_methods(["GET"])
def index(request):
    #return HttpResponse("Hello, world")
    url = "https://www.contrataciones.gov.py/datos/api/v3/doc/tender/429339"  # En durazo para probar
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return JsonResponse(data, safe=False)
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def consultar_licitaciones_dncp(request):
    url = "https://www.contrataciones.gov.py/datos/api/v3/doc/tender/429339"  # En durazo para probar
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        data = response.json()  # Converts JSON response to a Python dictionary
        return JsonResponse(data, safe=False)  # safe=False is needed if the top level JSON object is not a dictionary
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
    
class ProcurementCategoriesView(View):
    
    def get(self, request, *args, **kwargs):
        url = 'https://www.contrataciones.gov.py/datos/api/v3/doc/parameters/procurementCategories'
        response = requests.get(url)
        data = response.json()

        # Extract the 'list' object from the JSON response
        categories = data.get('list', [])

        # Check if 'id' is provided in the kwargs
        category_id = kwargs.get('id')
        if category_id:
            # Find the category by id
            category = next((item for item in categories if item["id"] == category_id), None)
            if category is None:
                raise Http404("Procurement category not found")
            return JsonResponse(category, safe=False)

        # Check if 'nombre' query parameter is provided in the request
        nombre_keyword = request.GET.get('nombre')
        if nombre_keyword:
            # Filter categories by 'nombre' keyword
            filtered_categories = [item for item in categories if nombre_keyword.lower() in item["nombre"].lower()]
            return JsonResponse(filtered_categories, safe=False)

        # If no 'id' or 'nombre' is provided, return all categories
        return JsonResponse(categories, safe=False)
    
class PlanningDetailView(PermissionRequiredMixin, View):
    required_permission = 'view_planning_detail'

    @method_decorator(login_required)
    def get(self, request, *args, id, **kwargs):
        url = f'https://www.contrataciones.gov.py/datos/api/v3/doc/planning/{id}'
        response = requests.get(url)
        if response.status_code == 404:
            raise Http404("Tender not found")

        return JsonResponse(response.json(), safe=False)
    
class PlannedTenderSearchView(PermissionRequiredMixin, View):
    required_permission = 'view_planning'

    @method_decorator(login_required)
    def get(self, request):
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
        return JsonResponse(response, safe=False)

class TenderDetailView(PermissionRequiredMixin, View):
    required_permission = 'view_tender_detail'

    @method_decorator(login_required)
    def get(self, request, id, *args, **kwargs):
        url = f'https://www.contrataciones.gov.py/datos/api/v3/doc/tender/{id}'
        response = requests.get(url)
        if response.status_code == 404:
            raise Http404("Tender not found")

        return JsonResponse(response.json(), safe=False)
    
class TenderSearchView(PermissionRequiredMixin, View):
    required_permission = 'view_tenders'

    @method_decorator(login_required)
    def get(self, request):
        categoria = request.GET.get('categoria')
        keyword = request.GET.get('keyword')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)

        # Start with all tenders and apply ordering
        tenders = Tender.objects.all().order_by('-fecha_publicacion_convocatoria')

        # Apply date filtering if provided
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            tenders = tenders.filter(fecha_publicacion_convocatoria__gte=start_date)

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            tenders = tenders.filter(fecha_publicacion_convocatoria__lte=end_date)

        # Apply additional filters using Q objects for combined filtering
        if categoria and keyword:
            tenders = tenders.filter(
                Q(categoria__icontains=categoria) & 
                Q(nombre_licitacion__icontains=keyword)
            )
        elif categoria:
            tenders = tenders.filter(categoria__icontains=categoria)
        elif keyword:
            tenders = tenders.filter(nombre_licitacion__icontains=keyword)

        # Paginate the results
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
        return JsonResponse(response, safe=False)

    