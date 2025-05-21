from django.utils.regex_helper import Group
from rest_framework import viewsets
from rest_framework import status
from rest_framework.mixins import Response
from rest_framework import permissions
from django.core.mail import EmailMessage
import threading


class SafeViewSet(viewsets.ModelViewSet):

  def destroy(self, request, *args, **kwargs):
    object_instance = self.get_object()
    object_instance.active = False 
    object_instance.save()
    return Response(status=status.HTTP_204_NO_CONTENT)
  
class NoteViewSet(viewsets.ModelViewSet):

    #i'm insane, i know c:
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.name = request.data['name']
        instance.note = request.data['note']
        instance.date = request.data['date']
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
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

class GroupPermission(permissions.BasePermission):
   def has_model_permissions( entity, model, perms, app, request):

    match request.method:
        case "GET":
            if entity.has_perm( f"{app}.read_{model.__name__ }"):
                return True
        case "POST":
            if entity.has_perm( f"{app}.add_{model.__name__ }"):
                return True
        case "PUT" | "PATCH":
            if entity.has_perm( f"{app}.change_{model.__name__ }"):
                return True
        case "DELETE":
            if entity.has_perm( f"{app}.delete_{model.__name__ }"):
                return True
        case _:
            return False
      

def add_to_group(user,group_name):
    group = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], 
            body=data['email_body'], 
            to=[data['to_email']])
        
        #if data['email_file']:
        #    email.attach('image.jpg', data['email_file'].read(), 'image/png')
        #if data['content_type'] == 'html':
        #    email.content_subtype = 'html'
        email.send()