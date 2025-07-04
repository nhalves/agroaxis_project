from django.contrib import admin
from .models import MilkQuality

@admin.register(MilkQuality)
class MilkQualityAdmin(admin.ModelAdmin):
    list_display = ('animal', 'date', 'ccs', 'cbt')
    search_fields = ('animal__name', 'animal__earring')
    list_filter = ('date',)
    autocomplete_fields = ('animal',)