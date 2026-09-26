from django import forms

from .models import Produto


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ["nome", "quantidade_estoque"]
        labels = {
            "nome": "Nome",
            "quantidade_estoque": "Quantidade em estoque",
        }

    def clean_nome(self):
        nome = self.cleaned_data["nome"]
        if Produto.objects.filter(nome__iexact=nome).exists():
            raise forms.ValidationError("Já existe um produto com esse nome.")
        return nome
