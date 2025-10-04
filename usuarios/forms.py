from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    """
    Formulário customizado para criação de usuário.
    Adiciona o campo 'email' à tupla de campos, pois o e-mail é MANDATÓRIO 
    para o fluxo de redefinição de senha funcionar.
    
    ⚠️ ATENÇÃO: Você deve atualizar a view 'usuarios/views.py:criar_conta' 
    para importar e usar este formulário em vez de UserCreationForm.
    """
    class Meta(UserCreationForm.Meta):
        # Adiciona 'email' à tupla de campos
        fields = UserCreationForm.Meta.fields + ('email',)

        # Opcionalmente, pode forçar o email a ser preenchido (se o UserCreationForm.Meta já não fizer isso)
        # fields = ('username', 'email', 'password', 'password2')

    # Você também pode adicionar o campo de email como obrigatório
    email = forms.EmailField(required=True, label='Endereço de E-mail')
