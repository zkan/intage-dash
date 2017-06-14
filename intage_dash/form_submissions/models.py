from django.contrib.postgres.fields import JSONField
from django.db import models

from typeforms.models import Typeform


class FormResponse(models.Model):
    typeform = models.ForeignKey(
        Typeform
    )
    answers = JSONField(
        null=False,
        blank=False,
        default={}
    )
    token = models.CharField(
        null=False,
        blank=False,
        max_length=100
    )
