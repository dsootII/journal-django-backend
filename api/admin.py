from django.contrib import admin
from .models import Entry, Container
# Register your models here.
admin.site.register([Entry, Container])

