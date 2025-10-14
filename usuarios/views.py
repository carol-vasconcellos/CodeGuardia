# usuarios/views.py

from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login
from .forms import CustomUserCreationForm 
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .tasks import send_reset_email_task 
from django.contrib.auth.views import PasswordResetView

# 🌟 CORREÇÃO: Importa a função de cálculo do app 'lessons' a partir do utils
from lessons.utils import get_progress_data 

# ----------------------------------------------------------------

@login_required
def bem_vindo(request):
    """View do Painel do Aluno, mostra o progresso, lendo do DB."""
    
    # CHAMA A FUNÇÃO QUE LÊ DO BANCO DE DADOS A PARTIR DO UTILS
    progress_data = get_progress_data(request.user) # Passa o objeto User
    
    context = {
        'nome_usuario': request.user.username,
        **progress_data, 
    }
    return render(request, 'usuarios/bem_vindo.html', context)


def criar_conta(request): 
    """View de Criação de Novo Usuário (Sign Up).""" 
    if request.method == 'POST': 
        # 🌟 USANDO O FORMULÁRIO CUSTOMIZADO 🌟
        form = CustomUserCreationForm(request.POST) 
        if form.is_valid(): 
            user = form.save() 
            # Loga o usuário automaticamente após o registro 
            login(request, user)  
            return redirect('bem_vindo')  
    else: 
        # 🌟 USANDO O FORMULÁRIO CUSTOMIZADO 🌟
        form = CustomUserCreationForm() 
      
    return render(request, 'usuarios/criar_conta.html', {'form': form})

def landing_page(request):
    """View da Página Principal (Landing Page)."""
    
    if request.user.is_authenticated:
        return redirect('bem_vindo') 
        
    mensagem = "CodeGuardia"
    botao_url = 'login' 
    botao_texto = "Comece Agora"

    context = {
        'mensagem': mensagem,
        'botao_url': botao_url,
        'botao_texto': botao_texto,
    }
    return render(request, 'usuarios/landing.html', context)

class CustomPasswordResetView(PasswordResetView):
    """
    View customizada para reset de senha que substitui o envio síncrono 
    de e-mail pela tarefa assíncrona do Celery.
    """
    
    # Este método é chamado internamente pelo Django para enviar o e-mail de reset
    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        
        # O Django passa o 'context' (que inclui o token e a URL).
        # Primeiro, precisamos renderizar o conteúdo do e-mail no worker web (Gunicorn):
        
        # 1. Renderiza o Título/Assunto
        subject = render_to_string(subject_template_name, context)
        subject = strip_tags(subject).strip() # Remove tags e espaços extras
        
        # 2. Renderiza o Corpo do E-mail (Texto Simples)
        body = render_to_string(email_template_name, context)
        
        # 3. Renderiza o Corpo do E-mail (HTML, se existir)
        html_message = render_to_string(html_email_template_name, context) if html_email_template_name else None
        
        # 4. DISPARA A TAREFA CELERY ASINCRONAMENTE
        # Usamos .delay() para enviar a tarefa para o Redis (Broker), 
        # que o Celery Worker irá processar posteriormente.
        send_reset_email_task.delay(
            subject, 
            body, # Passamos o corpo do e-mail renderizado
            to_email,
            html_message=html_message
        )
        
        # O Gunicorn retorna a resposta imediatamente, sem esperar pelo envio do e-mail.
