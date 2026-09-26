from django.core.validators import MaxValueValidator
from django.db import models


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    quantidade_estoque = models.PositiveIntegerField(
        validators=[MaxValueValidator(1_000_000)],
        verbose_name="quantidade em estoque",
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em", "-id"]

    def __str__(self):
        return self.nome
