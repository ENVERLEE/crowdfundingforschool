from django.urls import path
from . import views

urlpatterns = [
    path('<int:creator_id>/', views.creator_detail, name='creator_detail'),
    path('profile/edit/', views.creator_profile_edit, name='creator_profile_edit'),
    path('update/create/<int:project_id>/', views.creator_update_create, name='creator_update_create'),
]
