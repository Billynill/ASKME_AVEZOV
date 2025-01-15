from django.contrib import admin
from app import models
# Register your models here.
admin.site.register(models.Post)
admin.site.register(models.Author)
admin.site.register(models.PostInstance)
admin.site.register(models.Tag)

