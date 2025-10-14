from django.urls import path, reverse_lazy 
from . import views # Importa as views do seu app (incluindo a CustomPasswordResetView)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.landing_page, name='home'), 
    path('bem-vindo/', views.bem_vindo, name='bem_vindo'),
    path('signup/', views.criar_conta, name='signup'), 
    
    # 🌟 Login
    path(
        'login/', 
        auth_views.LoginView.as_view(
            template_name='registration/login.html'
        ), 
        name='login'
    ),

    # 🌟 Logout
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page=reverse_lazy('login')),
        name='logout'
    ),

    # 🌟 Reset de senha (4 etapas)
    # --------------------------------------------------------
    # CORREÇÃO CRÍTICA: USAR A VIEW CUSTOMIZADA DO CELERY
    path(
        'password_reset/', 
        views.CustomPasswordResetView.as_view( # <--- AGORA USA A SUA CLASSE
            template_name='registration/reset_password_request.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt',
            success_url=reverse_lazy('password_reset_done')
        ), 
        name='password_reset'
    ),
    # --------------------------------------------------------
    path(
        'password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ), 
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html', 
            success_url=reverse_lazy('password_reset_complete') 
        ), 
        name='password_reset_confirm'
    ),
    path(
        'reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html' 
        ), 
        name='password_reset_complete'
    ),
]
