# Seu urls.py principal

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. Rotas do seu App 'usuarios' (inclui todas as suas views customizadas,
    #    incluindo o fluxo de password reset customizado na raiz /password_reset/)
    path('', include('usuarios.urls')), 
    
    # 2. Rotas do seu App 'lessons'
    path('licoes/', include('lessons.urls')), 
    
    # 3. Mantenha a inclusão padrão APENAS se você precisar de outras rotas
    #    de autenticação que você NÃO definiu no 'usuarios.urls'
    #    (Ex: logout/, password_change/, se não estiverem em 'usuarios')
    #    Caso contrário, remova.
    #    path('accounts/', include('django.contrib.auth.urls')), 
]