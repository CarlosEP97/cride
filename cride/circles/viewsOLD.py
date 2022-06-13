#Django REST Framework

from rest_framework.decorators import api_view
from rest_framework.response import Response

# from django.http import HttpResponse,JsonResponse
from cride.circles.models import Circle

from cride.circles.serializersOLD import (
    CircleSerializer,
    CreateCircleSerializer
)

# @api_view(['GET'])
# def list_circles(request):
#     circles = Circle.objects.all().filter(is_public=True)
#     data = [circle.name for circle in circles ]
#     return Response(data)
#
# @api_view(['POST'])
# def create_circle(request):
#     """Create circle."""
#     name = request.data['name']
#     slug_name = request.data['slug_name']
#     about = request.data.get('about', '')
#     circle_create = Circle.objects.create(name=name, slug_name=slug_name, about=about)
#     circles = Circle.objects.all().filter(is_public=True)
#     data = [circle.name for circle in circles ]
#     return Response(data)

@api_view(['GET'])
def list_circles(request):
    """List circles."""
    circles = Circle.objects.filter(is_public=True)
    serializer = CircleSerializer(circles, many=True)
    return Response(serializer.data)
# Serializer(tu_objeto)
#
# Se usa cuando quieres extraer los de un objecto y mostrarlos como un JSON o XML


@api_view(['POST'])
def create_circle(request):
    """Create circle."""
    serializer = CreateCircleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    circle = serializer.save()
    return Response(CircleSerializer().data)
# **Serializer(data=diccionario) **
#
# se usa cuando quieres crear un nuevo objecto
