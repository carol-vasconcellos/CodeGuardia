# Devguardia/celery.py

import os
from celery import Celery

# Define as configurações padrão de módulo de settings do Django para 'celery'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Devguardia.settings')

# Cria uma instância da aplicação Celery. O argumento principal é o nome do módulo.
app = Celery('Devguardia')

# Carrega qualquer configuração relacionada ao Celery a partir do settings.py,
# usando o namespace 'CELERY'.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobre e carrega automaticamente as tarefas de todos os apps instalados.
app.autodiscover_tasks()