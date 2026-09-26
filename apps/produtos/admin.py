from django.contrib import admin

from .models import Produto


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "quantidade_estoque", "criado_em")
    search_fields = ("nome",)
