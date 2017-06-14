from django.contrib import admin

from .models import FormResponse


@admin.register(FormResponse)
class FormResponseAdmin(admin.ModelAdmin):
    list_display = (
        'typeform',
        'answers',
        'token',
    )
