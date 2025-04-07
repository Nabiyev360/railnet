from django.contrib import admin

from .models import Profile, Role, Settings


admin.site.register(Settings)
admin.site.register(Role)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'role')
    list_filter = ('role',)


admin.site.register(Profile, ProfileAdmin)