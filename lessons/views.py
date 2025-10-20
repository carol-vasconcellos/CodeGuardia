from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Licao 
import io
import sys

# 🌟 CORREÇÃO: Importa funções do lessons.utils.py (ENDEREÇO CORRETO E SEM CIRCULAR)
from .utils import get_progress_data, set_lesson_completed, is_lesson_completed, set_lesson_pending

# -------------------------------------------------------------
# FUNÇÕES AUXILIARES DE NAVEGAÇÃO
# -------------------------------------------------------------

def get_next_slug(current_slug):
    """Busca o slug da próxima lição no banco de dados pela ordem."""
    try:
        current_lesson = Licao.objects.get(slug=current_slug)
        next_lesson = Licao.objects.filter(ordem__gt=current_lesson.ordem).order_by('ordem').first()
        if next_lesson:
            return next_lesson.slug
    except Licao.DoesNotExist:
        pass
    return None

# -------------------------------------------------------------
# 1. VIEW PARA LISTAR AS LIÇÕES
# -------------------------------------------------------------

@login_required
def lista_licoes(request):
    user = request.user
    licoes_db = Licao.objects.all().order_by('ordem')
    
    licoes_status = [
        # Passa o user e o objeto licao para a função do utils
        (licao.slug, licao, is_lesson_completed(user, licao))
        for licao in licoes_db
    ]
    return render(request, 'lessons/lista_licoes.html', {'licoes_status': licoes_status})


# -------------------------------------------------------------
# 2. DETALHE DA LIÇÃO
# -------------------------------------------------------------

@login_required
def licao_detalhe(request, slug):
    user = request.user 
    licao = get_object_or_404(Licao, slug=slug)
    
    tipo_licao = licao.tipo 
    codigo_padrao_db = licao.codigo_padrao if licao.codigo_padrao else ""
    esperado_db = licao.esperado if licao.esperado else "" 
    conselho_db = licao.conselho if licao.conselho else "" 
    
    output = ""
    sucesso = is_lesson_completed(user, licao) # LÊ DO DB
    dica_erro = None
    feedback_tipo = None
    codigo_usuario = codigo_padrao_db
    
    if request.method == 'POST':
        
        # A. Lição de vídeo
        if tipo_licao == 'video' and 'marcar_concluida' in request.POST:
            set_lesson_completed(user, licao) # SALVA NO DB
            return redirect('lessons:licao_detalhe', slug=slug) 
        
        # B. Lição de código
        elif tipo_licao == 'codigo':
            
            # 🚨 VERSÃO FINAL SEGURA: NÃO EXECUTA CÓDIGO (RCE MITIGADO) 🚨
            
            codigo_usuario = request.POST.get('codigo_editor', codigo_padrao_db)
            
            # 💡 COMPORTAMENTO: Apenas salva o código submetido e simula sucesso
            # para permitir o fluxo, forçando o uso do console local para testes.
            
            set_lesson_completed(user, licao) # SALVA NO DB
            sucesso = True
            feedback_tipo = 'SUCESSO'
            output = f"⚠️ O teste de código foi desativado no servidor por segurança (RCE). Seu código foi salvo e a lição marcada como concluída para fins de navegação.\n\n--- SEU CÓDIGO SUBMETIDO ---\n{codigo_usuario}"
            
            return redirect('lessons:licao_detalhe', slug=slug)
            
    if request.method == 'GET' and tipo_licao == 'codigo':
        if not sucesso:
            codigo_usuario = codigo_padrao_db

    context = {
        'slug': slug,
        'licao': licao, 
        'codigo_usuario': codigo_usuario,
        'output': output,
        'sucesso': sucesso,
        'proximo_slug': get_next_slug(slug),
        'dica_erro': dica_erro, 
        'feedback_tipo': feedback_tipo,
        'forum_link': "https://forum.seu-site.com/postar-duvida-aqui", 
    }
    return render(request, 'lessons/licao_detalhe.html', context)


# -------------------------------------------------------------
# 3. REFAZER LIÇÃO
# -------------------------------------------------------------

@login_required
def refazer_licao(request, slug):
    user = request.user
    licao = get_object_or_404(Licao, slug=slug)
    
    set_lesson_pending(user, licao) # Reseta no DB
    
    return redirect('lessons:licao_detalhe', slug=slug)