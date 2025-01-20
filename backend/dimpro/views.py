from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from dimpro.serializers import *
from dimpro.models import *
from dimpro.helpers import SafeViewSet

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
        user_instance = User.objects.get(
            email=serializer.validated_data.get("email"))
        return Response(status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(TokenObtainPairView):
  serializer_class = CustomTokenObtainPairSerializer
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

    if user_instance.is_staff:
      raise AuthenticationFailed({"password": ["Correo o contraseña incorrectos o invalidos."]})

    login_serializer = self.serializer_class(data=request.data)
    if login_serializer.is_valid():
      user_serializer = UserSerializer(user_instance)
      return Response(
          {
              "token": login_serializer.validated_data.get("access"),
              "refresh-token": login_serializer.validated_data.get("refresh"),
              "user": user_serializer.data,
              "message": "Successfull login"
          },
          status=status.HTTP_200_OK)
    return Response(login_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)



class StaffOnlyLoginView(TokenObtainPairView):
  serializer_class = CustomTokenObtainPairSerializer
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

    if not (user_instance.is_staff or user_instance.is_superuser):
      raise AuthenticationFailed({"password": ["Correo o contraseña incorrectos o invalidos."]})

    login_serializer = self.serializer_class(data=request.data)
    if login_serializer.is_valid():
      user_serializer = UserSerializer(user_instance)
      return Response(
          {
              "token": login_serializer.validated_data.get("access"),
              "refresh-token": login_serializer.validated_data.get("refresh"),
              "user": user_serializer.data,
              "message": "Successfull login"
          },
          status=status.HTTP_200_OK)
    return Response(login_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
  permission_classes = (IsAuthenticated, )

  def get(self, request):
    user = request.user
    if not user:
      raise AuthenticationFailed({"message": "Unauthorized"})
    user_serializer = UserSerializer(user)
    return Response(user_serializer.data)


class UserViewSet(SafeViewSet):
  permission_classes = (IsAuthenticated, )
  serializer_class = UserSerializer
  queryset = User.objects.filter(active=True, is_staff=False)
  superuser_only = False
  staff_get_required = True


class StaffViewSet(SafeViewSet):
  permission_classes = (IsAdminUser, )
  serializer_class = UserSerializer
  queryset = User.objects.filter(Q(is_superuser=True) | Q(is_staff=True),
                                 active=True)
  superuser_only = True


# TODO: (para lueego) RequestPasswordResetView  && PasswordTokenCheckView && SetNewPasswordView


class ProductViewSet(SafeViewSet):
  serializer_class = ProductSerializer
  queryset = Product.objects.filter(active=True)


class ContactViewSet(SafeViewSet):
  serializer_class = ContacSerializer
  queryset = Contact.objects.filter(active=True)


class OrderViewSet(SafeViewSet):
  serializer_class = OrderSerializer
  queryset = Order.objects.filter(active=True)
