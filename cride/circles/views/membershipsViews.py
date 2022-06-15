#rest_framework
from rest_framework import viewsets,mixins

#django shortcuts
from rest_framework.generics import get_object_or_404

#models
from cride.circles.models.circles import Circle
from cride.circles.models.memberships import Membership

#serializers

from cride.circles.serializers.membershipsSerializers import MembershipModelSerializer


class MembershipViewSet(mixins.ListModelMixin
                        ,viewsets.GenericViewSet):
    """Circle membership view set."""
    #como el circulo no esta en la url lo tenemos que traer para poder trabajarlo con los demas por eso usamos dispatch
    # dispatch sirve para traer objetos de la url y modificar su ejecucion

    serializer_class = MembershipModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify that the circle exists."""
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super().dispatch(request, *args, **kwargs)



    def get_queryset(self):
        """Return circle members."""
        return Membership.objects.filter(
            circle=self.circle,
            is_active=True
        )





