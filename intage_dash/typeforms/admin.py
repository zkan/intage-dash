from django.contrib import admin

from .models import Typeform


@admin.register(Typeform)
class TypeformAdmin(admin.ModelAdmin):
    pass
