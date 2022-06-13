"""Circle serializers."""

# Django REST Framework
from rest_framework import serializers

# Model
from cride.circles.models import Circle


class CircleModelSerializer(serializers.ModelSerializer):
    """Circle model serializer."""

    members_limit = serializers.IntegerField(
        required=False,
        min_value=10,
        max_value=32000
    )
    is_limited = serializers.BooleanField(default=False)

    class Meta:
        """Meta class."""

        model = Circle
        fields = (
            'name', 'slug_name',
            'about', 'picture',
            'rides_offered', 'rides_taken',
            'verified', 'is_public',
            'is_limited', 'members_limit'
        )
        read_only_fields = (
            'is_public',
            'verified',
            'rides_offered',
            'rides_taken',
        )

    def validate(self, data):
        """Ensure both member_limit and is_limited are present."""

        method = self.context['request'].method
        members_limit = data.get('members_limit', None)
        is_limited = data.get('is_limited', False)

        if method == 'POST' or method == 'PUT':
            if is_limited ^ bool(members_limit):
                raise serializers.ValidationError(
                    'If circle is limited, a member_limit must be provider and is_limited must be True')

        elif method == 'PATCH':
            actual_member_limit = self.instance.members_limit
            actual_is_limited = self.instance.is_limited

            if (bool(members_limit) and actual_is_limited == False) or (is_limited and actual_member_limit == 0):
                raise serializers.ValidationError(
                    'If circle is limited, a member_limit must be provider and is_limited must be True')

        return data
