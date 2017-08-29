from django.contrib import admin

from django_db_mixer import models


class FieldSettingsInLine(admin.StackedInline):
    model = models.FieldSetting
    extra = 0
    fields = ['name', 'mix_type', 'mix_setting']
    readonly_fields = ['name']


class ModelSettingsAdmin(admin.ModelAdmin):
    inlines = [FieldSettingsInLine]
    fields = ['name', 'priority']
    readonly_fields = ['name']
    ordering = ['priority']


admin.site.register(models.ModelSetting, ModelSettingsAdmin)
