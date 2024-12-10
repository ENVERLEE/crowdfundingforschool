# urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='projects:project_list'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('become-creator/', views.become_creator, name='become_creator'),
    
    # 비밀번호 관리
    path('password/change/', 
        auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),
        name='password_change'),
    path('password/change/done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
        name='password_change_done'),
    path('password/reset/',
        auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
        name='password_reset'),
    path('password/reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
        name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('password/reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'),
    
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/give-initial-points/<int:user_id>/', views.give_initial_points, name='give_initial_points'),
    path('admin/approve-creator/<int:user_id>/', views.approve_creator, name='approve_creator'),
    path('admin/reject-creator/<int:user_id>/', views.reject_creator, name='reject_creator'),
]
