from django.urls import path
from .views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="BidMaster API",
        default_version='v1',
        description="API documentation for BidMaster",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@bidmaster.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    #path('api-data/', consultar_licitaciones_dncp, name='api-data'),
    # path("", views.index, name="index"),
    path('', home_view, name='home'),
    path('procurement-categories/', ProcurementCategoriesView.as_view(), name='procurement_categories'),
    path('procurement-categories/<str:id>/', ProcurementCategoriesView.as_view(), name='procurement_category_detail'),
    # path('planning/<str:id>/', PlanningDetailView.as_view(), name='planning_detail'),
    path('api/planning/<int:id>/', PlanningDetailView.as_view(), name='planning-detail-api'),
    path('api/tender/<int:id>/', TenderDetailView.as_view(), name='tender-detail-api'),
    path('api/tender/search/', TenderSearchView.as_view(), name='tender-search-api'),
    path('api/tender/planned-search/', PlannedTenderSearchView.as_view(), name='planned-tender-search-api'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-ui'),
    path('api/assign_tender/<int:user_id>/<str:nro_licitacion>/', AssignTenderAPIView.as_view(), name='assign_tender'),
    # path('api/assign_tender/<str:nro_licitacion>/', AssignTenderAPIView.as_view(), name='unassign_tender'),
]