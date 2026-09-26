from django.test import TestCase
from django.urls import reverse

from .forms import ProdutoForm
from .models import Produto


class ProdutoModelTests(TestCase):
    def test_str_returns_nome(self):
        produto = Produto.objects.create(nome="Caneta azul", quantidade_estoque=50)
        self.assertEqual(str(produto), "Caneta azul")


class HomeViewTests(TestCase):
    def test_get_home_shows_empty_message_without_produtos(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Ainda não há produtos cadastrados.")

    def test_post_valid_data_creates_produto_and_redirects(self):
        response = self.client.post(
            reverse("home"), {"nome": "Caneta azul", "quantidade_estoque": 50}
        )
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(Produto.objects.filter(nome="Caneta azul").exists())

    def test_post_empty_nome_does_not_create_produto(self):
        response = self.client.post(
            reverse("home"), {"nome": "", "quantidade_estoque": 10}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Produto.objects.count(), 0)
        self.assertFalse(response.context["form"].is_valid())

    def test_post_negative_quantidade_does_not_create_produto(self):
        response = self.client.post(
            reverse("home"), {"nome": "Lapis", "quantidade_estoque": -5}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Produto.objects.count(), 0)

    def test_post_quantidade_acima_do_limite_nao_cria_produto(self):
        response = self.client.post(
            reverse("home"), {"nome": "Lapis", "quantidade_estoque": 1_000_001}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Produto.objects.count(), 0)

    def test_post_nome_duplicado_ignorando_maiusculas_e_espacos(self):
        Produto.objects.create(nome="Caneta azul", quantidade_estoque=10)
        response = self.client.post(
            reverse("home"), {"nome": "  caneta azul  ", "quantidade_estoque": 5}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Produto.objects.count(), 1)

    def test_produtos_listados_do_mais_recente_para_o_mais_antigo(self):
        Produto.objects.create(nome="Primeiro", quantidade_estoque=1)
        Produto.objects.create(nome="Segundo", quantidade_estoque=2)
        response = self.client.get(reverse("home"))
        produtos = list(response.context["produtos"])
        self.assertEqual([p.nome for p in produtos], ["Segundo", "Primeiro"])


class HomeTemplateDesignTests(TestCase):
    """Confere a aplicação do design system descrito em DESIGN.md na home."""

    def test_page_links_design_stylesheet(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, 'href="/static/produtos/css/design.css"')

    def test_nav_bar_is_present(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, 'class="nav-bar"')

    def test_hero_panel_shows_page_title(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, 'class="hero-panel"')

    def test_form_panel_and_submit_button_are_present(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, 'class="form-panel"')
        self.assertContains(response, 'class="button-submit"')

    def test_produtos_list_uses_news_row_styling(self):
        Produto.objects.create(nome="Caneta azul", quantidade_estoque=10)
        response = self.client.get(reverse("home"))
        self.assertContains(response, 'class="news-row"')

    def test_footer_bar_is_present(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, 'class="footer-bar"')


class ProdutoFormWidgetTests(TestCase):
    def test_nome_widget_has_text_input_class(self):
        form = ProdutoForm()
        self.assertIn('class="text-input"', str(form["nome"]))

    def test_quantidade_widget_has_text_input_class(self):
        form = ProdutoForm()
        self.assertIn('class="text-input"', str(form["quantidade_estoque"]))
