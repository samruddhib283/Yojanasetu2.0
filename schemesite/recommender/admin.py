from django.contrib import admin
from .models import SchemeRequest

admin.site.register(SchemeRequest)

from .models import SchemeHistory
admin.site.register(SchemeHistory)
