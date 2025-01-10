from django.contrib import admin
from libapp.models import bookModel, borrowModel

# Register your models here.
admin.site.register(bookModel)
admin.site.register(borrowModel)