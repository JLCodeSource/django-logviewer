from django.contrib import admin

from .models import Asset, Log

# Register your models here.


class LogInline(admin.TabularInline):
    model = Log
    extra = 1


class AssetAdmin(admin.ModelAdmin):
    inlines = [LogInline]


admin.site.register(Asset, AssetAdmin)
