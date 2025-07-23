from django.utils.regex_helper import Group
from rest_framework import viewsets
from rest_framework import status
from rest_framework.mixins import Response
from rest_framework import permissions
from django.core.mail import EmailMessage
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate, login

from dimpro.models import *
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
    "User": "Usuario",
    "its": "su",
    "own": "propio",
    "export": "exportar",
    "user": "usuario",
    "group": "grupo",
    "order": "pedido",
    "product": "producto",
    "contact": "contacto",
    "note": "recordatorio",
    "price": "precio",
    "image": "imagen",
    "session": "sesión",
    "settings": "configuración",
    "phonenumber": "número de teléfono",
    "name": "nombre",
    "email": "correo electrónico",
}

PERMISSION_CONTENT_TYPE_NAME_TRANSLATIONS = {
    "log entry": "entrada de registro",
    "alegra user": "token de alegra",
    "exchange currency": "moneda de cambio",
    "exchange rate": "tasa de cambio",
    "order status": "status de pedido",
    "order product": "producto de pedido",
    "order_ product": "producto de pedido",
    "password reset token": "token de restablecimiento de contraseña",
    "price type": "tipo de precio",
    "pricetype tax": "impuesto de tipo de precio",
    "update database": "actualizar base de datos",
    "receivable": "cuenta por cobrar",
    "staff user": "empleado",
    "advanced homepage": "página de inicio avanzada",
}
PERMISSION_CONTENT_TYPE_TRANSLATIONS = {
    "user": "usuario",
    "group": "grupo",
    "order": "pedido",
    "product": "producto",
    "contact": "contacto",
    "note": "recordatorio",
    "price": "precio",
    "image": "imagen",
    "session": "sesión",
    "settings": "configuración",
    "alegrauser": "token de alegra",
    "permission": "permiso",
    "logentry": "entrada de registro",
    "order_ product": "producto de pedido",
    "order_product": "producto de pedido",
    "price_type": "tipo de precio",
    "precio tipo": "tipo de precio",
    "image": "imagen",
    "session": "sesión",
    "pricetype": "tipo de precio",
    "receivable": "cuenta por cobrar",
    "exchangerate": "taza de cambio",
    "exchangecurrency": "moneda de cambio",
    "passwordresettoken": "token de restablecimiento de contraseña",
    "pricetypetax": "impuesto de tipo de precio",
    "updatedb": "usuario",
    "card id": "cédula de identidad",
}


def translate_permission_content_type(codename):
    content_type = "_".join(codename.split("_")[1:])

    name = PERMISSION_CONTENT_TYPE_TRANSLATIONS.get(content_type)
    if not name:
        content_type = content_type.split("_")[-1]
        name = PERMISSION_CONTENT_TYPE_TRANSLATIONS.get(content_type)
    return name


def translate_permission_name(name):
    name= str(name).lower()
    for key, value in PERMISSION_CONTENT_TYPE_NAME_TRANSLATIONS.items():
        if key in name:
            name = name.replace(key, value)
            break
    parts = name.split(" ")
    for i,part in enumerate(parts):
        if part in PERMISSION_TRANSLATIONS:
            parts[i] = PERMISSION_TRANSLATIONS[part] 
    name = " ".join(parts).replace("_", "")

    return name


def partial_update_user(self, request, login=False, *args, **kwargs):
    from .serializers import UserSerializer

    serializer = self.get_serializer(data=request.data, partial=True)

    email = request.data.pop("email", None)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data.copy()

    validated_data.pop("confirmPassword", None)
    user_groups = validated_data.pop("groups", None)
    password = validated_data.pop("password", None)
    # Obtén el usuario actual que deseas actualizar
    current_user = self.get_object()

    # Si no se envía un email en el request, usa el del usuario actual
    if email is None:
        raise ValidationError({"error": "El campo email es obligatorio."})

    # Verifica si existe otro usuario activo (distinto al actual) con el mismo email
    if (
        User.objects.filter(email=email, active=True)
        .exclude(id=current_user.id)
        .exists()
    ):
        return Response(
            {"error": "El correo ya existe."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Actualiza los campos del usuario actual
    if "name" in validated_data:
        current_user.name = validated_data.get("name")
    if "email" in validated_data:
        current_user.email = email
    if password:
        current_user.set_password(password)
    if "phonenumber" in validated_data:
        current_user.phonenumber = validated_data.get("phonenumber")
    if user_groups is not None:
        current_user.groups.clear()
        current_user.groups.set(user_groups)
    current_user.save()

    return Response(UserSerializer(current_user).data, status=status.HTTP_200_OK)


def create_user(self, request, *args, **kwargs):
    from dimpro.serializers import UserRegistrationSerializer, UserSerializer
    email = request.data.pop("email", None)
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=False)
    validated_data = serializer.validated_data.copy()
    validated_data.pop("confirmPassword")
    user_groups = validated_data.pop("groups", None)
    password = validated_data.pop("password", None)

    if not email:
        return Response(
            {"error": "El campo email es obligatorio."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check if an active user already exists with that email
    if User.objects.filter(email=email, active=True).exists():
        return Response(
            {"error": "El correo ya existe."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    user_instance, created = User.objects.update_or_create(
        email=email, active=True, defaults=validated_data
    )
    if password:
        user_instance.set_password(password)
    if user_groups is not None:
        user_instance.groups.set(user_groups)
    else:
        # If no groups are provided, assign the default group (if any)
        default_group = Group.objects.filter(name="user").first()
        if default_group:
            user_instance.groups.add(default_group)
    user_instance.save()
    data = UserSerializer(user_instance).data
    data["password"] = password
    return Response(data, status=status.HTTP_201_CREATED)
