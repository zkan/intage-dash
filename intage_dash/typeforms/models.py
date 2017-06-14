from django.contrib.postgres.fields import JSONField
from django.db import models


class Typeform(models.Model):
    uid = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    payload = JSONField(
        null=False,
        blank=False,
        default={'data': ''}
    )

    def __str__(self):
        return self.uid
