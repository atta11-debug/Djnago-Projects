from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.todo)
class todoAdmin(admin.ModelAdmin):
    list_display=["srno","title","date","user"]