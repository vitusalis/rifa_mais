from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from raffles.models import Raffle
from raffles.models import Ticket
from datetime import timedelta
from django.utils import timezone


class DaysReserved(SimpleListFilter):
    title = 'Dias reservado'

    parameter_name = 'dias'

    def lookups(self, request, model_admin):
        return (
            ('2', '2 dias úteis'),
        )

    def queryset(self, request, queryset):
        if self.value() == '2':
            if timezone.now().weekday() == 6:
                # domingo
                days = 3
            elif timezone.now().weekday() == 0:
                # segunda
                days = 4
            elif timezone.now().weekday() == 1:
                # terça
                days = 5
            else:
                days = 2
            print("days", days)
            print("timedelta", timezone.now() - timedelta(days=days))
            return queryset.filter(
                status='RES',
                date_creation__lt=timezone.now() - timedelta(days=days))


def set_paid(modeladmin, request, queryset):
    queryset.update(status='PAI')


def set_unpaid(modeladmin, request, queryset):
    queryset.update(status="RES")


set_paid.short_description = "Estão pagos"
set_unpaid.short_description = "Não estão pagos"


class RaffleAdmin(admin.ModelAdmin):
    list_display = ('name', "ticket_amount", "date", "ticket_price", "status")
    list_filter = ('name', 'date_creation', 'status')
    search_fields = ('name',)
    exclude = ('_id',)


class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'ticket_number', "status", 'raffle', 'name', "phone", "email", "instagram", 'days_reserved', 'date_creation')
    list_filter = ('raffle__name', 'status', DaysReserved)
    search_fields = ('name', 'phone', 'email', 'instagram' 'ticket_number')
    exclude = ('_id',)
    actions = (set_paid, set_unpaid)


admin.site.register(Raffle, RaffleAdmin)
admin.site.register(Ticket, TicketAdmin)
