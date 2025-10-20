# usuarios/password_validators.py
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomComplexityValidator:
    """
    Validador customizado para garantir a complexidade da senha:
    - Mínimo de 1 letra maiúscula
    - Mínimo de 1 letra minúscula
    - Mínimo de 1 número
    - Mínimo de 1 caractere especial
    """
    def __init__(self, min_length=12):
        self.min_length = min_length
    
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("A senha deve conter pelo menos uma letra maiúscula."),
                code='password_no_uppercase',
            )
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _("A senha deve conter pelo menos uma letra minúscula."),
                code='password_no_lowercase',
            )
        if not re.findall(r'[0-9]', password):
            raise ValidationError(
                _("A senha deve conter pelo menos um número."),
                code='password_no_number',
            )
        # Regex para caracteres especiais (não alfa-numéricos)
        if not re.findall(r'[!@#$%^&*()_+=\[\]{}|\\,.<>/?~`":;-]', password):
            raise ValidationError(
                _("A senha deve conter pelo menos um caractere especial (ex: !@#$%^&*)."),
                code='password_no_special',
            )

    def get_help_text(self):
        return _(
            "Sua senha deve ter no mínimo %(min_length)s caracteres e conter pelo menos 1 letra maiúscula, 1 minúscula, 1 número e 1 caractere especial." % {'min_length': self.min_length}
        )