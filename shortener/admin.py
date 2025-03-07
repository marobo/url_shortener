from django.contrib import admin
from .models import ShortURL


@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = ('original_url', 'short_code', 'visits', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('original_url', 'short_code')
    readonly_fields = ('short_code', 'qr_code', 'visits')
