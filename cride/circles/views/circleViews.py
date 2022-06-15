"""Circle views."""

# Django REST Framework
from rest_framework import viewsets,mixins

from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.circlesPermissions import IsCircleAdmin

# Serializers
from cride.circles.serializers.circleSerializers import CircleModelSerializer

# Models
from cride.circles.models.circles import Circle
from cride.circles.models.memberships import Membership


class CircleViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):

    """Circle view set."""


    serializer_class = CircleModelSerializer
    lookup_field = 'slug_name'


    def get_queryset(self):
        """Restrict list to public-only."""
        queryset = Circle.objects.all()
        if self.action == 'list':
            return queryset.filter(is_public=True)
        return queryset


    def perform_create(self,serializer):
        """"assign circle admin"""
        # print(serializer) model serializer itself
        circle = serializer.save() # circle instance create
        user = self.request.user
        profile = user.profile
        Membership.objects.create(
            user=user,
            profile=profile,
            circle=circle,
            is_admin=True,
            remaining_invitations=10
        )

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsCircleAdmin)
        return [permission() for permission in permissions]

