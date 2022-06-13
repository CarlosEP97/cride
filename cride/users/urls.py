"""Users URLs."""

# Django
from django.urls import include, path

# Views
# from cride.users.views.usersViews import UserLoginAPIView
# from cride.users.views.usersViews import UserSignUpAPIView
# from cride.users.views.usersViews import AccountVerificationAPIView
from cride.users.views.usersViews import UserViewSet

# Django REST Framework
from rest_framework.routers import DefaultRouter

app_name = 'users'

# urlpatterns = [
#     path('login/', UserLoginAPIView.as_view(), name='login'),
#     path('signup/', UserSignUpAPIView.as_view(), name='login'),
#     path('verify/', AccountVerificationAPIView.as_view(), name='verify'),
# ]

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]
