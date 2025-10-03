from django.contrib import admin
from .models import Licao

# Opcional: Personaliza como as lições aparecem na lista do Admin
class LicaoAdmin(admin.ModelAdmin):
    list_display = ('ordem', 'titulo', 'tipo', 'slug')
    list_filter = ('tipo',)
    # O slug será preenchido automaticamente com base no título
    prepopulated_fields = {'slug': ('titulo',)} 

admin.site.register(Licao, LicaoAdmin)