from django.db import models

SETTING_COPY = 'copy'
SETTING_VALUE = 'value'
SETTING_CHOICE = 'choice'
SETTING_SHUFFLE = 'shuffle'
SETTINGS = [SETTING_COPY, SETTING_VALUE, SETTING_CHOICE, SETTING_SHUFFLE]
SETTINGS_CHOICES = [(setting, setting) for setting in SETTINGS]


class ModelSetting(models.Model):
    model = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    priority = models.IntegerField()

    def __str__(self):
        return self.name + ' ({})'.format(str(self.priority))


class FieldSetting(models.Model):
    model = models.ForeignKey(ModelSetting)
    field = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    mix_type = models.CharField(max_length=64, choices=SETTINGS_CHOICES, default=SETTING_COPY)
    mix_setting = models.TextField(null=True, default='')
