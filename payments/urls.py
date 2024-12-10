from django.urls import path
from . import views

urlpatterns = [
    path('pledge/<int:project_id>/', views.pledge_create, name='pledge_create'),
    path('pledge/detail/<int:pledge_id>/', views.pledge_detail, name='pledge_detail'),
    path('pledges/', views.pledge_list, name='pledge_list'),
    path('pledge/<int:pledge_id>/approve/', views.pledge_approve, name='pledge_approve'),
    path('pledge/<int:pledge_id>/reject/', views.pledge_reject, name='pledge_reject'),
]
