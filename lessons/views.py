# lessons/views.py (CÓDIGO FINAL E COMPLETO LENDO DO BANCO DE DADOS)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Licao # Importa o Model Licao do banco de dados
import io
import sys

# 🚨 IMPORTANTE: O DICIONÁRIO ESTATICO 'LICOES' FOI REMOVIDO DE PROPÓSITO.
# O sistema agora usa Licao.objects.all().

# -------------------------------------------------------------
# FUNÇÕES AUXILIARES DE SESSÃO E NAVEGAÇÃO (USAM MODEL)
# -------------------------------------------------------------

def set_lesson_completed(request, slug):
    """Marca uma lição como concluída na sessão do usuário."""
    if 'completed_lessons' not in request.session:
        request.session['completed_lessons'] = []
    if slug not in request.session['completed_lessons']:
        request.session['completed_lessons'].append(slug)
        request.session.modified = True 

def is_lesson_completed(request, slug):
    """Verifica se a lição está concluída."""
    return slug in request.session.get('completed_lessons', [])

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

# Função para o Painel do Aluno (usuários/views.py chama esta)
def get_progress_data_from_db(request):
    """Calcula o progresso lendo do Banco de Dados."""
    licoes_db = Licao.objects.all().order_by('ordem')
    total_licoes = licoes_db.count()
    licoes_concluidas = 0
    progresso = []

    for licao in licoes_db:
        concluida = is_lesson_completed(request, licao.slug)
        if concluida:
            licoes_concluidas += 1
        
        progresso.append({
            'titulo': licao.titulo,
            'slug': licao.slug,
            'tipo': licao.get_tipo_display(), # Usa método do Model
            'concluida': concluida,
        })
    
    porcentagem_progresso = 0
    if total_licoes > 0:
        porcentagem_progresso = round((licoes_concluidas / total_licoes) * 100)
    
    return {
        'progresso_licoes': progresso,
        'total_licoes': total_licoes,
        'licoes_concluidas': licoes_concluidas,
        'porcentagem_progresso': porcentagem_progresso,
    }

# -------------------------------------------------------------
# 1. VIEW PARA LISTAR AS LIÇÕES (LÊ DO BANCO)
# -------------------------------------------------------------

@login_required
def lista_licoes(request):
    # LÊ TODAS AS LIÇÕES DO BANCO, ORDENADAS PELA ORDEM
    licoes_db = Licao.objects.all().order_by('ordem')
    
    licoes_status = [
        (licao.slug, licao, is_lesson_completed(request, licao.slug))
        for licao in licoes_db
    ]
    return render(request, 'lessons/lista_licoes.html', {'licoes_status': licoes_status})


# -------------------------------------------------------------
# 2. DETALHE DA LIÇÃO (LÊ DO BANCO)
# -------------------------------------------------------------

# lessons/views.py (FUNÇÃO licao_detalhe CORRIGIDA)

@login_required
def licao_detalhe(request, slug):
    # BUSCA A LIÇÃO NO BANCO DE DADOS
    licao = get_object_or_404(Licao, slug=slug)
    
    # 🌟 Mapeamento de variáveis simplificado e direto para o Model 🌟
    tipo_licao = licao.tipo 
    codigo_padrao_db = licao.codigo_padrao if licao.codigo_padrao else ""
    esperado_db = licao.esperado if licao.esperado else "" # Campo esperado do Model
    conselho_db = licao.conselho if licao.conselho else "" # Campo conselho (para dicas)
    
    output = ""
    sucesso = is_lesson_completed(request, slug) 
    dica_erro = None
    feedback_tipo = None
    codigo_usuario = codigo_padrao_db
    
    if request.method == 'POST':
        
        # A. Lição de vídeo
        if tipo_licao == 'video' and 'marcar_concluida' in request.POST:
            set_lesson_completed(request, slug)
            return redirect('lessons:licao_detalhe', slug=slug) 
        
        # B. Lição de código
        elif tipo_licao == 'codigo':
            esperado = esperado_db
            codigo_usuario = request.POST.get('codigo_editor', codigo_padrao_db)

            old_stdout = sys.stdout
            redirected_output = sys.stdout = io.StringIO()
            
            try:
                exec(codigo_usuario, {}, {})
                output = redirected_output.getvalue()
                
                if output == esperado:
                    set_lesson_completed(request, slug) 
                    sucesso = True
                    feedback_tipo = 'SUCESSO'
                    output = "✅ Parabéns! Você concluiu esta lição! 🎉"
                else:
                    feedback_tipo = 'ERRO_SAIDA'
                    dica_erro = conselho_db # Usa o campo conselho como dica
                    output = f"Sua Saída:\n{output}\n---\nSaída Esperada:\n{esperado}"
                    
            except Exception as e:
                feedback_tipo = 'ERRO_CODIGO'
                output = f"❌ ERRO no código: {type(e).__name__}: {e}"
                dica_erro = "Verifique a sintaxe (indentação, aspas, parênteses) ou se o nome da variável está certo."
                
            finally:
                sys.stdout = old_stdout
            
    if request.method == 'GET' and tipo_licao == 'codigo':
        codigo_usuario = codigo_padrao_db

    context = {
        'slug': slug,
        'licao': licao, # O template usa licao.url_video|safe
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
# 3. REFAZER LIÇÃO (MANTIDA)
# -------------------------------------------------------------

@login_required
def refazer_licao(request, slug):
    """Remove a lição da lista de concluídas na sessão e redireciona."""
    if 'completed_lessons' in request.session:
        request.session['completed_lessons'] = [
            s for s in request.session['completed_lessons'] if s != slug
        ]
        request.session.modified = True
    return redirect('lessons:licao_detalhe', slug=slug)