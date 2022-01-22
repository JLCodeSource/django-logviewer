from django.contrib import admin

from .models import Asset, Log

# Register your models here.


class LogInline(admin.TabularInline):
    model = Log
    extra = 1


class AssetAdmin(admin.ModelAdmin):
    inlines = [LogInline]
    list_display = (
        "name",
        "site",
        "phase",
        "get_latest_created",
        "get_latest_severity",
        "get_latest_message",
    )
    """
    Need to add custom filter
    https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter
    """
    list_filter = ["site", "phase", "log__severity", "log__resolved"]


admin.site.register(Asset, AssetAdmin)
