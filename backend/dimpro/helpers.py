from rest_framework import viewsets
from rest_framework import status
from rest_framework.mixins import Response
from rest_framework import permissions
from serializers import UserNestedSerializer




class SafeViewSet(viewsets.ModelViewSet):

  def destroy(self, request, *args, **kwargs):
    object_instance = self.get_object()
    object_instance.active = False 
    object_instance.save()
    return Response(status=status.HTTP_204_NO_CONTENT)
  

class IsStaff(permissions.BasePermission):
    message = "Not enough permissions"
    def has_permission(self, request, view):
      if not request.user.is_staff:
          return False
      return True

class UserReadOnlyPermission(permissions.BasePermission):
    message = "Not enough permissions"
    def has_permission(self, request, view):
      allowed_methods = ["GET"]
      if (not request.user.is_staff and request.method in allowed_methods) or request.user.is_staff:
         return True