from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ProdutoForm
from .models import Produto


def home(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto cadastrado com sucesso.")
            return redirect("home")
    else:
        form = ProdutoForm()

    produtos = Produto.objects.all()
    return render(request, "produtos/home.html", {"form": form, "produtos": produtos})
