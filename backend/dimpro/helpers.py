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

    # i'm insane, i know c:
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.name = request.data["name"]
        instance.note = request.data["note"]
        instance.date = request.data["date"]
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
    def has_model_permissions(entity, model, perms, app, request):

        match request.method:
            case "GET":
                if entity.has_perm(f"{app}.read_{model.__name__ }"):
                    return True
            case "POST":
                if entity.has_perm(f"{app}.add_{model.__name__ }"):
                    return True
            case "PUT" | "PATCH":
                if entity.has_perm(f"{app}.change_{model.__name__ }"):
                    return True
            case "DELETE":
                if entity.has_perm(f"{app}.delete_{model.__name__ }"):
                    return True
            case _:
                return False


def add_to_group(user, group_name):
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
            subject=data["email_subject"],
            body=data["email_body"],
            to=[data["to_email"]],
        )

        # if data['email_file']:
        #    email.attach('image.jpg', data['email_file'].read(), 'image/png')
        # if data['content_type'] == 'html':
        #    email.content_subtype = 'html'
        email.send()


PERMISSION_TRANSLATIONS = {
    "can": "puede",
    "Can": "Puede",
    "add": "añadir",
    "change": "cambiar",
    "delete": "eliminar",
    "view": "ver",
    "user": "usuario",
    "its": "su",
    "own": "propio",
    "export": "exportar",
    "user": "usuario",
    "group": "grupo",
    "order": "pedido",
    "product": "producto",
    "contact": "contacto",
    "note": "nota",
    "price": "precio",
    "image": "imagen",
    "session": "sesión",
    "settings": "configuración",
}

PERMISSION_CONTENT_TYPE_NAME_TRANSLATIONS = {
    "log entry": "entrada de registro",
    "alegra user": "usuario de alegra",
    "exchange currency": "moneda de cambio",
    "exchange rate": "tasa de cambio",
    "order product": "producto de pedido",
    "password reset token": "token de restablecimiento de contraseña",
    "price type": "tipo de precio",
    "pricetype tax": "impuesto de tipo de precio",
    "update database": "actualizar base de datos",
    "receivable": "cuenta por cobrar",
    "staff user": "usuario staff",
    "advanced homepage": "página de inicio avanzada",
}
PERMISSION_CONTENT_TYPE_TRANSLATIONS = {
    "user": "usuario",
    "group": "grupo",
    "order": "pedido",
    "product": "producto",
    "contact": "contacto",
    "note": "nota",
    "price": "precio",
    "image": "imagen",
    "session": "sesión",
    "settings": "configuración",
    "alegrauser": "usuario de alegra",
    "permission": "permiso",
    "logentry": "entrada de registro",
    "order_product": "producto de pedido",
    "price_type": "tipo de precio",
    "precio tipo": "tipo de precio",
    "image": "imagen",
    "session": "sesión",
    "pricetype": "tipo de precio",
    "receivable": "cuenta por cobrar",
    "exchangerate":"taza de cambio",
    "exchangecurrency": "moneda de cambio",
    "passwordresettoken": "token de restablecimiento de contraseña",
    "pricetypetax": "impuesto de tipo de precio",
    "updatedb": "usuario",
}


def translate_permission_content_type(codename):
    content_type = "_".join(codename.split("_")[1:])
    
    name = PERMISSION_CONTENT_TYPE_TRANSLATIONS.get(content_type)
    if not name:
        content_type = content_type.split("_")[-1]
        name =  PERMISSION_CONTENT_TYPE_TRANSLATIONS.get(content_type)
    return name

def translate_permission_name(name):
    for key, value in PERMISSION_CONTENT_TYPE_NAME_TRANSLATIONS.items():
        if key in name:
            name = name.replace(key, value)
            break
    parts = name.split(" ")
    for i, part in enumerate(parts):
        if part in PERMISSION_TRANSLATIONS:
            parts[i] = PERMISSION_TRANSLATIONS[part]
    name = " ".join(parts).replace("_","")
    
    return name
