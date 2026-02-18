from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.song)
class songAdmin(admin.ModelAdmin):
    list_display=['title','artist','image','audio_file','audio_link','lyrics','duration']