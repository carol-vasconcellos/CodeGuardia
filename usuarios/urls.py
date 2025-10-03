# usuarios/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # 🌟 ROTA 1: PÁGINA RAIZ (LANDING PAGE) 🌟
    path('', views.landing_page, name='home'), 
    
    # Rota 2: Painel do Aluno (Este é o destino de login)
    path('bem-vindo/', views.bem_vindo, name='bem_vindo'),
    
    # Rota 3: Criação de Conta
    path('signup/', views.criar_conta, name='signup'), 
]