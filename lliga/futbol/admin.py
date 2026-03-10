from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Lliga)
admin.site.register(Equip)
admin.site.register(Jugador)

class EventInLine(admin.StackedInline):
    exclude = ["detalls"]
    model = Event
    extra = 2
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # filtrem els jugadors i només deixem els que siguin d'algun dels 2 equips (local o visitant)
        if db_field.name == "jugador":
            partit_id = request.resolver_match.kwargs['object_id']
            partit = Partit.objects.get(id=partit_id)
            jugadors_local = [jugador.id for jugador in partit.equip_local.jugadors.all()]
            jugadors_visitant = [jugador.id for jugador in partit.equip_visitant.jugadors.all()]
            jugadors = jugadors_local + jugadors_visitant
            kwargs["queryset"] = Jugador.objects.filter(id__in=jugadors)
        # filtrem els equips i només deixem els 2 equips del partit
        elif db_field.name == "equip":
            partit_id = request.resolver_match.kwargs['object_id']
            partit = Partit.objects.get(id=partit_id)
            equips = [partit.equip_local.id, partit.equip_visitant.id]
            kwargs["queryset"] = Equip.objects.filter(id__in=equips)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)            

class PartitAdmin(admin.ModelAdmin):
    search_fields = ["lliga__nom"]
    list_display = ["lliga", "equip_local", "equip_visitant"]
    inlines = [EventInLine,]

admin.site.register(Partit, PartitAdmin)