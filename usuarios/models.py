from django.db import models
from django.contrib.auth.models import User
from lessons.models import Licao

class Progresso(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    licao = models.ForeignKey(Licao, on_delete=models.CASCADE)
    concluida = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.licao.titulo} - {'Concluída' if self.concluida else 'Pendente'}"
