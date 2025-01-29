from django.utils.regex_helper import Group
from rest_framework import viewsets
from rest_framework import status
from rest_framework.mixins import Response
from rest_framework import permissions




class SafeViewSet(viewsets.ModelViewSet):

  def destroy(self, request, *args, **kwargs):
    object_instance = self.get_object()
    object_instance.active = False 
    object_instance.save()
    return Response(status=status.HTTP_204_NO_CONTENT)
  

class IsStaff(permissions.BasePermission):
    message = "No posee los permisos necesarios"
    def has_permission(self, request, view):
      if not request.user.groups.filter(name="staff").exists():
          return False
      return True

class UserReadOnlyPermission(permissions.BasePermission):
    message = "No posee los permisos necesarios"
    def has_permission(self, request, view):
      allowed_methods = ["GET"]
      user_is_staff = request.user.groups.filter(name="staff").exists()
      if (not user_is_staff and request.method in allowed_methods) or user_is_staff:
         return True

def add_to_group(user,group_name):
    group = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)
