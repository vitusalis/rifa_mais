from django.db import models
import uuid

STATUS = (
    ('ACT', 'Ativo'),
    ('INA', 'Inativo'),
    ('SOO', 'Em breve')
)


class Raffle(models.Model):
    _id = models.CharField(max_length=39, null=False, blank=False, default='')
    name = models.CharField(max_length=155, null=True, blank=True, verbose_name="Sorteio")
    ticket_amount = models.PositiveIntegerField(null=False, default=1, verbose_name="Quantidade de tickets")
    ticket_price = models.FloatField(null=False, default=1, verbose_name="Preço do ticket")
    date = models.DateField(null=True, blank=True, verbose_name="Data do sorteio")

    cover = models.ImageField(upload_to='photos/', null=True, blank=True, verbose_name='Foto de capa')
    photo_1 = models.ImageField(upload_to='photos/', null=True, blank=True, verbose_name='Foto 1')
    photo_2 = models.ImageField(upload_to='photos/', null=True, blank=True, verbose_name='Foto 2')
    photo_3 = models.ImageField(upload_to='photos/', null=True, blank=True, verbose_name='Foto 3')
    photo_4 = models.ImageField(upload_to='photos/', null=True, blank=True, verbose_name='Foto 4')

    info = models.CharField(max_length=255, null=True, blank=True, verbose_name='Informações do sorteio')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    status = models.CharField(max_length=20, choices=STATUS, default='SOO')

    class Meta:
        ordering = ('status',)
        verbose_name = "Sorteio"
        verbose_name_plural = "Sorteios"

    def __str__(self):
        return self.name if self.name else "Sorteio sem nome"

    def save(self, *args, **kwargs):
        self._id = f"{uuid.uuid1().int}"
        super(Raffle, self).save(*args, **kwargs)
