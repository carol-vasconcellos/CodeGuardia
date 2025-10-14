from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_reset_email_task(subject, message, recipient_list, html_message=None):
    """Tarefa Celery para enviar emails em background."""
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            html_message=html_message,
            fail_silently=False  # Para ver erros reais no log do Celery Worker
        )
        print(f"E-mail de reset enviado com sucesso para: {recipient_list}")
    except Exception as e:
        # Se houver uma falha aqui, ela aparece no log do Celery Worker, não no Gunicorn
        print(f"ERRO CRÍTICO NO ENVIO DE EMAIL: {e}")
        # Você pode logar o erro aqui para debug
