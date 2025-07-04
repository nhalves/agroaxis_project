from django.contrib import admin
from .models import Animal, ReproductiveEvent, HealthEvent

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('earring', 'name', 'status', 'breed', 'birth_date')
    search_fields = ('name', 'earring')
    list_filter = ('status', 'breed')

@admin.register(ReproductiveEvent)
class ReproductiveEventAdmin(admin.ModelAdmin):
    list_display = ('animal', 'event_type', 'event_date')
    list_filter = ('event_type', 'event_date')
    search_fields = ('animal__name', 'animal__earring')
    date_hierarchy = 'event_date'

@admin.register(HealthEvent)
class HealthEventAdmin(admin.ModelAdmin):
    list_display = ('animal', 'event_type', 'event_date', 'medication', 'withdrawal_period_days')
    list_filter = ('event_type', 'event_date')
    search_fields = ('animal__name', 'animal__earring', 'medication')
    date_hierarchy = 'event_date'