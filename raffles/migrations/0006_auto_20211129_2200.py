# Generated by Django 3.2.9 on 2021-11-30 01:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('raffles', '0005_alter_raffle_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='raffle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='raffles.raffle', verbose_name='Sorteio'),
        ),
        migrations.AlterUniqueTogether(
            name='ticket',
            unique_together={('raffle', 'ticket_number')},
        ),
    ]
