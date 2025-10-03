# lessons/apps.py
from django.apps import AppConfig

class LessonsConfig(AppConfig): # <-- CORRETO: Classe renomeada
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lessons'             # <-- CORRETO: O nome do app em minúsculas