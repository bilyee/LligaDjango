from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Lliga)
admin.site.register(Equip)
admin.site.register(Jugador)

class EventInLine(admin.StackedInline):
    model = Event
    extra = 2

class PartitAdmin(admin.ModelAdmin):
    inlines = [EventInLine,]

admin.site.register(Partit, PartitAdmin)