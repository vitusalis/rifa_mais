import uuid
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models

STATUS = (("AVA", "Disponível"), ("RES", "Reservado"), ("PAI", "Pago"))


class Ticket(models.Model):
    # Auto-generated
    status = models.CharField(max_length=20, choices=STATUS, default="RES")
    date_creation = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="Data de reserva")
    _id = models.CharField(max_length=39, null=False, blank=False, default="")

    # Required
    raffle = models.ForeignKey(
        "raffles.Raffle", on_delete=models.CASCADE, verbose_name="Sorteio"
    )
    ticket_number = models.PositiveIntegerField(null=False, verbose_name="Número")
    name = models.CharField(max_length=255, verbose_name="Nome")
    email = models.EmailField(max_length=255)
    cpfCnpj = models.CharField(max_length=255, verbose_name="CPF/CNPJ")

    # Optional
    phone = models.CharField(max_length=30, null=True, blank=True, verbose_name="Telefone")
    instagram = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name if self.name else "Sorteio sem nome"

    def save(self, *args, **kwargs):

        # # missing info
        # if self.ticket_number is None or not self.raffle:
        #     print("ticket_number", self.ticket_number, "raffle", self.raffle)
        #     raise ValidationError("Missing info", code="Informações faltando")

        # more than available tickets
        if self.ticket_number >= self.raffle.ticket_amount or self.ticket_number < 0:
            raise ValidationError("Invalid ticket range", code=" Ticket não exite")

        # ticket already purchased
        if self.id:
            if self.raffle.ticket_set.filter(ticket_number=self.ticket_number).exclude(id=self.id):
                raise ValidationError("Invalid ticket number", code="Parece que este ticket já foi reservado")

        self._id = f"{uuid.uuid1().int}"
        super(Ticket, self).save(*args, **kwargs)

    class Meta:
        ordering = ["ticket_number"]
        unique_together = ("raffle", "ticket_number")

    def days_reserved(self):
        return (timezone.now() - self.date_creation).days

    days_reserved.short_description = "Dias reservado"

    def create_payment(self):
        from raffles.payment_service import PaymentService

        fields = "name", "email", "cpfCnpj", "phone"
        customer_response = PaymentService.create_asaas_customer({field: getattr(self, field) for field in fields})
        if customer_response:
            customer_id = customer_response.json().get("id")

            payment_response = PaymentService.create_asaas_payment(
                customer_id=customer_id,
                total_value=self.raffle.ticket_price,
                raffle_name=self.raffle.name,
                ticket_number=self.ticket_number,
            )
            if payment_response:
                payment_link = payment_response.get("invoiceUrl")
                return {"type": "payment_link", "payment_link": payment_link}

            return {"type": "error", "message": "Não foi possível registrar o pagamento"}

        return {"type": "error", "message": "Não foi possível registrar o usuário. Por favor, verifique se o CPF está correto"}


{"raffle_id": 2, "ticket_number": 3, "name": "Victor 2", "email": "victor.teste@gmail.com"}
