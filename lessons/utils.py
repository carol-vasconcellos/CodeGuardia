# lessons/utils.py

from lessons.models import Licao # Importação local e segura
from django.shortcuts import get_object_or_404 

from usuarios.models import Progresso

def is_lesson_completed(user, licao):
    """Verifica no banco se o usuário já concluiu a lição."""
    return Progresso.objects.filter(user=user, licao=licao, concluida=True).exists()


def set_lesson_completed(user, licao):
    """Marca uma lição como concluída para o usuário no banco."""
    progresso, created = Progresso.objects.get_or_create(user=user, licao=licao)
    progresso.concluida = True
    progresso.save()


def get_progress_data(request):
    """
    Calcula e retorna os dados de progresso (total, concluídas, lista).
    Usada pelo Painel do Aluno.
    """
    # 1. Busca todas as lições do banco (ordenadas)
    licoes_db = Licao.objects.all().order_by('ordem') 
    
    # 2. Inicializa contadores
    progresso = []
    licoes_concluidas = 0
    total_licoes = licoes_db.count()
    
    # 3. Calcula o status de conclusão
    for licao in licoes_db:
        concluida = is_lesson_completed(request, licao.slug) 
        if concluida:
            licoes_concluidas += 1
        
        progresso.append({
            'titulo': licao.titulo,
            'slug': licao.slug,
            'tipo': licao.get_tipo_display(),
            'concluida': concluida,
        })
        
    # 4. Cálculo da porcentagem
    porcentagem_progresso = 0
    if total_licoes > 0:
        porcentagem_progresso = round((licoes_concluidas / total_licoes) * 100)
    
    return {
        'progresso_licoes': progresso,
        'total_licoes': total_licoes,
        'licoes_concluidas': licoes_concluidas,
        'porcentagem_progresso': porcentagem_progresso,
    }