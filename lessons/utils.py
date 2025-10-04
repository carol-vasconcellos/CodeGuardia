# lessons/utils.py

from lessons.models import Licao 
from usuarios.models import Progresso 
from django.shortcuts import get_object_or_404 
from django.contrib.auth.models import User

# --- Funções de Progresso do Banco de Dados ---

def is_lesson_completed(user: User, licao: Licao) -> bool:
    """Verifica no banco se o usuário já concluiu a lição, usando objetos User e Licao."""
    return Progresso.objects.filter(user=user, licao=licao, concluida=True).exists()


def set_lesson_completed(user: User, licao: Licao):
    """Marca uma lição como concluída para o usuário no banco."""
    progresso, created = Progresso.objects.get_or_create(user=user, licao=licao)
    progresso.concluida = True
    progresso.save()

def set_lesson_pending(user: User, licao: Licao):
    """Marca uma lição como pendente para o usuário no banco (Reseta)."""
    # Deleta o registro concluído para "resetar" o progresso da lição.
    Progresso.objects.filter(user=user, licao=licao, concluida=True).delete()


def get_progress_data(user: User) -> dict:
    """
    Calcula e retorna os dados de progresso do usuário lendo exclusivamente do banco de dados.
    Esta função é chamada pelo Painel do Aluno (usuarios/views.py).
    """
    # 1. Busca todas as lições do banco (ordenadas)
    licoes_db = Licao.objects.all().order_by('ordem') 
    
    progresso_licoes = []
    licoes_concluidas = 0
    total_licoes = licoes_db.count()
    
    # 2. Busca os slugs concluídos do usuário de forma eficiente
    concluidas_db = Progresso.objects.filter(user=user, concluida=True).values_list('licao__slug', flat=True)
    
    # 3. Cria a lista de progresso
    for licao in licoes_db:
        concluida = licao.slug in concluidas_db
        if concluida:
            licoes_concluidas += 1
        
        progresso_licoes.append({
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
        'progresso_licoes': progresso_licoes,
        'total_licoes': total_licoes,
        'licoes_concluidas': licoes_concluidas,
        'porcentagem_progresso': porcentagem_progresso,
    }
