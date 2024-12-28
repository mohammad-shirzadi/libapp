from django.contrib import admin
from libapp.models import bookModel, borrowModels

# Register your models here.
admin.site.register(bookModel)
admin.site.register(borrowModels)