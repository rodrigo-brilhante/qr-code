from django.contrib import admin
from cupom.models import Record

class Records(admin.ModelAdmin):
    list_display = ('id', 'name', 'qr_code', 'hash_id', 'date_create', 'date_use')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 20

admin.site.register(Record, Records)