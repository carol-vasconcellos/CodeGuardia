from django.urls import path, reverse_lazy 
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 🌟 PÁGINA INICIAL
    path('', views.landing_page, name='home'), 

    # 🌟 Painel do aluno
    path('bem-vindo/', views.bem_vindo, name='bem_vindo'),

    # 🌟 Criação de conta
    path('signup/', views.criar_conta, name='signup'), 
    
    # 🌟 Login
    path(
        'login/', 
        auth_views.LoginView.as_view(
            template_name='registration/login.html' 
        ), 
        name='login'
    ),
    
    # 🌟 1. Formulário para inserir o email
    path('password_reset/', 
        auth_views.PasswordResetView.as_view(
            template_name='registration/reset_password_request.html',
            email_template_name='registration/password_reset_email.html',   # ✅ corrigido
            subject_template_name='registration/password_reset_subject.txt',
            success_url=reverse_lazy('password_reset_done')
        ), 
        name='password_reset'
    ),

    # 🌟 2. Mensagem de sucesso após o envio do e-mail
    path('password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html',
            
        ), 
        name='password_reset_done'
    ),

    # 🌟 3. Confirmação do token do email
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html', 
            success_url=reverse_lazy('password_reset_complete') 
        ), 
        name='password_reset_confirm'
    ),

    # 🌟 4. Mensagem de senha redefinida com sucesso
    path('reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html' 
        ), 
        name='password_reset_complete'
    ),
]
