from django.contrib import admin

# Register your models here.

from stocks.models import Companies

admin.site.register(Companies)
