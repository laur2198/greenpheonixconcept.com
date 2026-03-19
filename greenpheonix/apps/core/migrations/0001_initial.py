from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Testimonial",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("client_nume", models.CharField(help_text="Numele clientului", max_length=100)),
                ("client_firma", models.CharField(blank=True, help_text="Firma / Brand (opțional)", max_length=150)),
                ("client_industrie", models.CharField(blank=True, help_text="Ex: Transport, eCommerce", max_length=100)),
                ("client_foto", models.ImageField(blank=True, null=True, upload_to="testimoniale/")),
                ("text", models.TextField(help_text="Citatul clientului")),
                ("rating", models.PositiveSmallIntegerField(
                    choices=[(1, "1 stele"), (2, "2 stele"), (3, "3 stele"), (4, "4 stele"), (5, "5 stele")],
                    default=5,
                )),
                ("rezultat_cheie", models.CharField(
                    blank=True, max_length=100,
                    help_text="Ex: +230% rezervări | 4.8x ROAS — apare ca highlight",
                )),
                ("activ", models.BooleanField(default=True)),
                ("featured", models.BooleanField(default=False, help_text="Afișat în prima secțiune pe homepage")),
                ("ordine", models.PositiveIntegerField(default=0)),
                ("creat_la", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Testimonial",
                "verbose_name_plural": "Testimoniale",
                "ordering": ["ordine", "-creat_la"],
            },
        ),
        migrations.CreateModel(
            name="ClientLogo",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nume", models.CharField(max_length=100)),
                ("logo", models.ImageField(blank=True, null=True, upload_to="clienti/logos/")),
                ("url_site", models.URLField(blank=True, help_text="Link către site-ul clientului (opțional)")),
                ("ordine", models.PositiveIntegerField(default=0)),
                ("activ", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Logo client",
                "verbose_name_plural": "Logo-uri clienți",
                "ordering": ["ordine"],
            },
        ),
    ]
