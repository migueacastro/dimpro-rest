from auditlog.models import LogEntry
from django.contrib.admin.options import get_content_type_for_model
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.db.models import Q
from dimpro.serializers import *
from dimpro.models import *
from auditlog.models import LogEntry
from dimpro.helpers import SafeViewSet, IsStaff, UserReadOnlyPermission
from django.utils.translation import gettext as _
from django.contrib.sessions.models import Session
from django.middleware.csrf import get_token
# Create your views here.


class UserRegistrationView(APIView
                           ):  # Aqui puedes retornar responses personalizadas
  serializer_class = UserRegistrationSerializer
  permission_classes = (
AllowAny,
  )  # Estos son las classes que indican quienes pueden meterse a este endpoint

  def post(
      self, request
  ):  # En registration solo manejaremos post, los demas quedaran como metodo no permitido
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid():
      password = serializer.validated_data.get("password", None)
      confirmPassword = serializer.validated_data.get("confirmPassword", None)

      if password != confirmPassword:
        raise AuthenticationFailed(
            {"confirmPassword": ["Las contraseñas no coinciden."]})

      new_user = serializer.save()
      if new_user:

        LogEntry.objects.create(
            content_type=get_content_type_for_model(User),
            action=LogEntry.Action.CREATE,
            changes_text="User registered",
            object_pk=new_user.id,
            object_id=new_user.id,
        ) 
        user_instance = User.objects.get(
            email=serializer.validated_data.get("email"))
        return Response(status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
  serializer_class = UserLoginSerializer
  permission_classes = (AllowAny, )

  def post(self, request, *args, **kwargs):
    email = request.data.get("email", None)
    password = request.data.get("password", None)

    if not email:
      raise AuthenticationFailed({"email": ["Este campo no puede estar vacio."]})
    elif not password:
      raise AuthenticationFailed({"password": ["Este campo no puede estar vacio."]})

    user_instance = authenticate(email=email, password=password)
    if not user_instance:
      raise AuthenticationFailed({"password": ["Correo o contraseña incorrectos o invalidos."]})
    if not user_instance.groups.filter(name="user").exists() or user_instance.groups.filter(name__in=["admin", "staff"]).count() > 0:
      raise AuthenticationFailed({"password": ["Correo o contraseña incorrectos o invalidos."]})

    login_serializer = self.serializer_class(data=request.data)
    if login_serializer.is_valid():
      user_serializer = UserSerializer(user_instance)
      login(request, user_instance)
      LogEntry.objects.create(
        content_type=get_content_type_for_model(User),
        action=LogEntry.Action.UPDATE,
        changes_text="User logged in",
        object_pk=user_instance.id,
        object_id=user_instance.id,
      ) 
      
      return Response(
          {
              "user": user_serializer.data,
              "message": "Successfull login",
          },
          status=status.HTTP_200_OK)
    return Response(login_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView): # You might add this request into the Logout function inside svelte, just a fetch, doesnt have to return anything, although perhaps at somepoint we will use refresh-token to logout all users that are using a specific token, for avoiding a very risky vulnerability of JWT. 
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
      user_instance = request.user
      logout(request)

      Session.objects.filter(session_key=request.session.session_key).delete()
      LogEntry.objects.create(
        content_type=get_content_type_for_model(User),
        action=LogEntry.Action.UPDATE,
        changes_text="User logged out",
        object_pk=user_instance.id,
        object_id=user_instance.id,
      )
      return Response(status=status.HTTP_200_OK)


class StaffOnlyLoginView(APIView):
  serializer_class = UserLoginSerializer 
  permission_classes = (AllowAny, )

  def post(self, request, *args, **kwargs):
    email = request.data.get("email", None)
    password = request.data.get("password", None)

    if not email:
      raise AuthenticationFailed({"email": ["Este campo no puede estar vacio."]})
    elif not password:
      raise AuthenticationFailed({"password": ["Este campo no puede estar vacio."]})

    user_instance = authenticate(email=email, password=password)
    if (not user_instance) or not (user_instance.groups.filter(name="staff").exists()):
      raise AuthenticationFailed({"password": ["Correo o contraseña incorrectos o invalidos."]})

    login_serializer = self.serializer_class(data=request.data)
    if login_serializer.is_valid():
      login(request, user_instance)
      LogEntry.objects.create(
        content_type=get_content_type_for_model(User),
        action=LogEntry.Action.UPDATE,
        changes_text="User logged in",
        object_pk=user_instance.id,
        object_id=user_instance.id,
      ) 
      user_serializer = UserSerializer(user_instance)
      return Response(
          {
              "user": user_serializer.data,
              "message": "Successfull login",
          },
          status=status.HTTP_200_OK)
    return Response(login_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
  permission_classes = (IsAuthenticated, )

  def get(self, request):
    user = request.user
    if not user:
      raise AuthenticationFailed({"message": "Acceso no Autorizado."})
    user_serializer = UserSerializer(user)
    return Response(user_serializer.data)


class UserViewSet(SafeViewSet):
  permission_classes = (IsAuthenticated, IsStaff)
  serializer_class = UserSerializer
  queryset = User.objects.filter(active=True).exclude(groups__name="staff") # If this line does not work i will nuke Copilot

  def retrieve(self, request, *args, **kwargs): 
    object_instance = self.get_object()
    return Response(UserNestedSerializer(object_instance).data)

class RefreshCSRFTokenView(APIView):
    permission_classes = (AllowAny, )
    def get(self, request):
        return Response({
            'csrftoken': get_token(request)
        })
        

class StaffViewSet(SafeViewSet):
  permission_classes = (IsAdminUser, )
  serializer_class = UserNestedSerializer
  queryset = User.objects.filter(groups__name="staff", active=True)
  superuser_only = True


# TODO: (para lueego) RequestPasswordResetView  && PasswordTokenCheckView && SetNewPasswordView


class ProductViewSet(SafeViewSet):
  serializer_class = ProductSerializer
  permission_classes = (IsAuthenticated, UserReadOnlyPermission)
  queryset = Product.objects.filter(active=True) # Aqui no por ejemplo

class ContactViewSet(SafeViewSet):
  serializer_class = ContactSerializer
  permission_classes = (IsAuthenticated, UserReadOnlyPermission)
  queryset = Contact.objects.filter(active=True)


class OrderProductViewSet(SafeViewSet):
  serializer_class = OrderProductSerializer
  permission_classes = (IsAuthenticated, )
  queryset = Order_Product.objects.all()

class PriceTypeViewSet(SafeViewSet):
  serializer_class = PriceTypeSerializer
  permission_classes = (IsAuthenticated, UserReadOnlyPermission)
  queryset = PriceType.objects.filter(active=True)

class OrderViewSet(SafeViewSet): # Te muestra de una vez sus propios OrderProducts
  serializer_class = OrderSerializer 
  permission_classes = (IsAuthenticated, )
  # No hay que preocuparse por lecturas indebidas, 
  # El CORS no permitiria cualquier IP acceder al API excepto por el del mismo frontend desde la nube
  # Entonces, esa vulnerabilidad ya está cubierta, de hecho, por esa razon ya es inutil el UserReadOnlyPermission, pero dejemoslo activo
  queryset = Order.objects.filter(active=True)
  def patch(self, request, *args, **kwargs):
    print("Pasó por aqui: ", request.data)
    return super().patch(request, *args, **kwargs)

class UserOrderViewSet(SafeViewSet):
  serializer_class = OrderSerializer
  permission_classes = (IsAuthenticatedOrReadOnly, )
  def get_queryset(self):
    return Order.objects.filter(active=True, user=self.request.user)

class AlegraUserViewSet(SafeViewSet):
  serializer_class = AlegraUserSerializer
  permission_classes = (IsAdminUser,)
  queryset = AlegraUser.objects.filter(active=True)

class WelcomeStaffView(APIView):
  def get(self, request, format=None):
    serializer = WelcomeStaffSerializer() # El serializador solito agarra los registros, usara UserSerializer
    return Response(serializer.data)
  
class WelcomeSuperUserView(APIView):
  def get(self, request, format=None):
    serializer = WelcomeSuperUserSerializer() # El serializador solito agarra los registros, usara UserSerializer
    return Response(serializer.data)

class NoteViewSet(SafeViewSet):
  serializer_class = NoteSerializer
  permission_classes = (IsAdminUser,)
  queryset = Note.objects.all()

class LogViewSet(SafeViewSet):
  serializer_class = LogSerializer
  permission_classes = (IsAdminUser,)
  queryset = LogEntry.objects.all()
