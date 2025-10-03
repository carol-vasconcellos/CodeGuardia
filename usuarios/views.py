from django.shortcuts import render, redirect # Já inclui render e redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login

# 🌟 CORREÇÃO: Importa a função de cálculo do app 'lessons' 🌟
from lessons.views import get_progress_data_from_db 

# ----------------------------------------------------------------
# FUNÇÃO AUXILIAR: MANTIDA AQUI PARA SUPORTE LOCAL
# ----------------------------------------------------------------
def is_lesson_completed(request, slug):
    """Verifica se a lição está concluída, lendo a sessão."""
    return slug in request.session.get('completed_lessons', [])


@login_required
def bem_vindo(request):
    """View do Painel do Aluno, mostra o progresso."""
    
    # 🌟 CORRIGIDO: CHAMA A FUNÇÃO QUE LÊ DO BANCO DE DADOS 🌟
    progress_data = get_progress_data_from_db(request)

    context = {
        'nome_usuario': request.user.username,
        **progress_data, 
    }
    return render(request, 'usuarios/bem_vindo.html', context)


def criar_conta(request):
    """View de Criação de Novo Usuário (Sign Up)."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Loga o usuário automaticamente após o registro
            login(request, user) 
            return redirect('bem_vindo') 
    else:
        form = UserCreationForm()
    
    return render(request, 'usuarios/criar_conta.html', {'form': form})

def landing_page(request):
    """View da Página Principal (Landing Page)."""
    
    # 🌟 CORREÇÃO: SE ESTIVER AUTENTICADO, REDIRECIONA IMEDIATAMENTE 🌟
    if request.user.is_authenticated:
        return redirect('bem_vindo') 
        
    # Se não estiver logado, exibe o conteúdo de Landing Page
    mensagem = "Aprenda a programar de graça."
    botao_url = 'login' 
    botao_texto = "Comece Agora"

    context = {
        'mensagem': mensagem,
        'botao_url': botao_url,
        'botao_texto': botao_texto,
    }
    return render(request, 'usuarios/landing.html', context)