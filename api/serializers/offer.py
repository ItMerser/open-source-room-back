from rest_framework import serializers

from core.models import Offer


class OfferCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('id', 'sender', 'recipient', 'project', 'type',)
