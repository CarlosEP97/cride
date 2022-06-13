#Django REST Framework
from rest_framework.views import APIView
from rest_framework import status, viewsets,mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny

from cride.circles.models.circles import Circle
from cride.users.models import User

from cride.circles.serializers.circleSerializers import CircleModelSerializer
from cride.users.serializers.UserSerializers import (UserLoginSerializer, UserModelSerializer,
                                                     UserSignUpSerializer,AccountVerificationSerializer)
from cride.users.serializers.ProfileSerializers import ProfileModelSerializer

from cride.users.permissions.usersPermissions import IsAccountOwner


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """User view set.
    Handle sign up, login and account verification.
    """
    queryset = User.objects.filter(is_active=True, is_client=True)
    lookup_field = 'username'
    serializer_class = UserModelSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['signup', 'login', 'verify']:
            permissions = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]


    def retrieve(self,request,*args,**kwargs):
        response = super().retrieve(request,*args,**kwargs) # do super for get the method before overwriting for add extra data
        circles = Circle.objects.filter(
            members=request.user,
            membership__is_active=True
        )
        # print(response.data) response before overwtriting
        data = {
            'user': response.data,
            'circle': CircleModelSerializer(circles, many=True).data
        }
        response.data = data
        # print(response.data) # response after
        return response

    @action(detail=True, methods=['put', 'patch'])
    def profile(self,request, *args, **kwargs):
        """update profile data"""
        user = self.get_object()
        profile = user.profile
        partial = request.method == 'PATCH'
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data)


    @action(detail=False, methods=['post'])
    def login(self, request):
        """User sign in."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Account verification."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Congratulation, now go share some rides!'}
        return Response(data, status=status.HTTP_200_OK)

# class UserLoginAPIView(APIView):
#     """User login API view."""
#
#     def post(self, request, *args, **kwargs):
#         """Handle HTTP POST request."""
#         serializer = UserLoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user, token = serializer.save()
#         data = {
#             'user': UserModelSerializer(user).data,
#             'access_token': token
#         }
#         return Response(data, status=status.HTTP_201_CREATED)
#
#
# class UserSignUpAPIView(APIView):
#     """User sign up API view."""
#
#     def post(self, request, *args, **kwargs):
#         """Handle HTTP POST request."""
#         serializer = UserSignUpSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         data = UserModelSerializer(user).data
#         return Response(data, status=status.HTTP_201_CREATED)
#
#
# class AccountVerificationAPIView(APIView):
#     """Account verification API view."""
#
#     def post(self, request, *args, **kwargs):
#         """Handle HTTP POST request."""
#         serializer = AccountVerificationSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         data = {'message': 'Congratulation, now go share some rides!'}
#         return Response(data, status=status.HTTP_200_OK)
