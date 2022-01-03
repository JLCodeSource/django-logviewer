from django.contrib import admin

from .models import Asset, Log

# Register your models here.


class LogInline(admin.TabularInline):
    model = Log
    extra = 1


class AssetAdmin(admin.ModelAdmin):
    inlines = [LogInline]
    list_display = ("name", "get_latest_log")


admin.site.register(Asset, AssetAdmin)
