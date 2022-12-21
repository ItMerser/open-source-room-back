from django.db import models

from core.models.choices import OfferType


class Offer(models.Model):
    sender = models.ForeignKey(
        'core.Specialist',
        related_name='sender_set',
        on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        'core.Specialist',
        related_name='recipient_set',
        on_delete=models.CASCADE,
    )
    project = models.ForeignKey('core.Project', on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=OfferType.choices)
    response = models.BooleanField(blank=True, null=True, default=None)
