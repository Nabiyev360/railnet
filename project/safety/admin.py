from django.contrib import admin

from .models import Misconduct


class MisconductAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'position', 'reason', 'created_by')
    list_display_links = ('fullname',)
    list_filter = ('created_by',)


admin.site.register(Misconduct, MisconductAdmin)