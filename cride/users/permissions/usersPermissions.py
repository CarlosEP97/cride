from rest_framework.permissions import BasePermission



class IsAccountOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        # print(obj)
        return request.user == obj # the object is te user retrieve request


