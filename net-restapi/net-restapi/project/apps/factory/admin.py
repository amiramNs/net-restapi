from django.contrib import admin

from project.apps.factory import models

admin.site.register(models.Equipment)
admin.site.register(models.Emergency)
