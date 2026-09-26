import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Produto",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=100)),
                (
                    "quantidade_estoque",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MaxValueValidator(1000000)],
                        verbose_name="quantidade em estoque",
                    ),
                ),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-criado_em"],
            },
        ),
    ]
