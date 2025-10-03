# [Seu Projeto]/urls.py (o arquivo principal)

from django.contrib import admin
from django.urls import path, include
# REMOVA: from django.views.generic.base import RedirectView 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rotas de AUTENTICAÇÃO do Django (login, logout, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # 🌟 CORREÇÃO 1: A rota raiz ('') agora inclui 'usuarios.urls'. 
    # O app 'usuarios' decidirá o que mostrar na raiz.
    path('', include('usuarios.urls')), 
    
    # Rotas do seu app 'lessons'
    path('licoes/', include('lessons.urls')), 
]