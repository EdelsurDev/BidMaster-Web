from django.urls import path

from . import views
from .views import *

urlpatterns = [
    #path('api-data/', consultar_licitaciones_dncp, name='api-data'),
    # path("", views.index, name="index"),
    path('', home_view, name='home'),
    path('procurement-categories/', ProcurementCategoriesView.as_view(), name='procurement_categories'),
    path('procurement-categories/<str:id>/', ProcurementCategoriesView.as_view(), name='procurement_category_detail'),
    path('planning/<str:id>/', PlanningDetailView.as_view(), name='planning_detail'),
    path('tender/<int:id>/', TenderDetailView.as_view(), name='tender-detail'),
    path('tender/search/', TenderSearchView.as_view(), name='tender-search'),
    path('tender/planned-search/', PlannedTenderSearchView.as_view(), name='planned-tender-search'),

]