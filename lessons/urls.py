# lessons/urls.py

from django.urls import path
from . import views

app_name = 'lessons' 
urlpatterns = [
    # Rotas existentes
    path('', views.lista_licoes, name='lista_licoes'),
    path('<slug:slug>/', views.licao_detalhe, name='licao_detalhe'),
    
    # 🌟 CORREÇÃO: ADICIONAR A ROTA REFAZER_LICAO 🌟
    path('refazer/<slug:slug>/', views.refazer_licao, name='refazer_licao'), 
]