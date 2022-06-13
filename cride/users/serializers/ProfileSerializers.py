"""Users serializers."""

# Django
from django.conf import settings


# Django REST Framework
from rest_framework import serializers


# # Models
from cride.users.models import Profile


class ProfileModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'biography',
            'picture',
            'rides_taken',
            'rides_offered',
            'reputation'
        )
        read_only_fields = (
            'rides_taken',
            'rides_offered',
            'reputation'
        )


