# Generated by Django 3.2.9 on 2021-11-30 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raffles', '0003_auto_20211125_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='cpfCnpj',
            field=models.CharField(default='null', max_length=255, verbose_name='CPF/CNPJ'),
            preserve_default=False,
        ),
    ]
