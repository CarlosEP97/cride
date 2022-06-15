# django
# from django.urls import path
#
# #views
#
# from cride.circles.views import list_circles,create_circle
#

#
# urlpatterns = [
#     # Django Admin
#     path('',list_circles),
#     path('create',create_circle),
# ]

"""Circles URLs."""

# app_name = 'circles'

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from cride.circles.views.circleViews import CircleViewSet
from cride.circles.views.membershipsViews import MembershipViewSet

router = DefaultRouter()
router.register(r'', CircleViewSet, basename='circle')
router.register(r'(?P<slug_name>[a-zA-Z0-9_-]+)/members', MembershipViewSet,basename='membership'
)

urlpatterns = [
    path('', include(router.urls))
]
