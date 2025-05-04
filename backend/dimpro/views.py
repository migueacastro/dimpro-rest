from auditlog.models import LogEntry
from django.contrib.admin.options import get_content_type_for_model
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from backend.settings import BASE_DIR
import os
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
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
from django.contrib.staticfiles import finders
from datetime import datetime

# Create your views here.

# pdf exporting
from django.http import FileResponse
import io
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    Frame,
    Table,
    Paragraph,
    Spacer,
    Image,
    TableStyle,
)
from svglib.svglib import svg2rlg
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()


class UserRegistrationView(APIView):  # Aqui puedes retornar responses personalizadas
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
                    {"confirmPassword": ["Las contraseñas no coinciden."]}
                )

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
                    email=serializer.validated_data.get("email")
                )
                return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        if not email:
            raise AuthenticationFailed({"email": ["Este campo no puede estar vacio."]})
        elif not password:
            raise AuthenticationFailed(
                {"password": ["Este campo no puede estar vacio."]}
            )

        user_instance = authenticate(email=email, password=password)
        if not user_instance:
            raise AuthenticationFailed(
                {"password": ["Correo o contraseña incorrectos o invalidos."]}
            )
        if (
            not user_instance.groups.filter(name="user").exists()
            or user_instance.groups.filter(name__in=["admin", "staff"]).count() > 0
        ):
            raise AuthenticationFailed(
                {"password": ["Correo o contraseña incorrectos o invalidos."]}
            )

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
                status=status.HTTP_200_OK,
            )
        return Response(login_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(
    APIView
):  # You might add this request into the Logout function inside svelte, just a fetch, doesnt have to return anything, although perhaps at somepoint we will use refresh-token to logout all users that are using a specific token, for avoiding a very risky vulnerability of JWT.
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
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        if not email:
            raise AuthenticationFailed({"email": ["Este campo no puede estar vacio."]})
        elif not password:
            raise AuthenticationFailed(
                {"password": ["Este campo no puede estar vacio."]}
            )

        user_instance = authenticate(email=email, password=password)
        if (not user_instance) or not (
            user_instance.groups.filter(name="staff").exists()
        ):
            raise AuthenticationFailed(
                {"password": ["Correo o contraseña incorrectos o invalidos."]}
            )

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
                status=status.HTTP_200_OK,
            )
        return Response(login_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        if not user:
            raise AuthenticationFailed({"message": "Acceso no Autorizado."})
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)


class UserChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data.get("old_password", None)
            password = serializer.validated_data.get("password", None)
            confirmPassword = serializer.validated_data.get("confirm_password", None)

            if not user.check_password(old_password):
                raise AuthenticationFailed(
                    {"old_password": ["La contraseña actual no es correcta."]}
                )
            if password != confirmPassword:
                raise AuthenticationFailed(
                    {"confirm_password": ["Las contraseñas no coinciden."]}
                )

            user.set_password(password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(SafeViewSet):
    permission_classes = (IsAuthenticated, IsStaff)
    serializer_class = UserSerializer
    queryset = User.objects.filter(active=True).exclude(
        groups__name="staff"
    )  # If this line does not work i will nuke Copilot

    def retrieve(self, request, *args, **kwargs):
        object_instance = self.get_object()
        return Response(UserNestedSerializer(object_instance).data)


class RefreshCSRFTokenView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response({"csrftoken": get_token(request)})


class StaffViewSet(SafeViewSet):
    permission_classes = (IsAdminUser,)
    serializer_class = UserNestedSerializer
    queryset = User.objects.filter(groups__name="staff", active=True)
    superuser_only = True


# TODO: (para lueego) RequestPasswordResetView  && PasswordTokenCheckView && SetNewPasswordView


class ProductViewSet(SafeViewSet):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated, UserReadOnlyPermission)
    queryset = Product.objects.filter(active=True)  # Aqui no por ejemplo


class ContactViewSet(SafeViewSet):
    serializer_class = ContactSerializer
    permission_classes = (IsAuthenticated, UserReadOnlyPermission)
    queryset = Contact.objects.filter(active=True)


class OrderProductViewSet(SafeViewSet):
    serializer_class = OrderProductSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Order_Product.objects.all()


class PriceTypeViewSet(SafeViewSet):
    serializer_class = PriceTypeSerializer
    permission_classes = (IsAuthenticated, UserReadOnlyPermission)
    queryset = PriceType.objects.filter(active=True)


class OrderViewSet(SafeViewSet):  # Te muestra de una vez sus propios OrderProducts
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    # No hay que preocuparse por lecturas indebidas,
    # El CORS no permitiria cualquier IP acceder al API excepto por el del mismo frontend desde la nube
    # Entonces, esa vulnerabilidad ya está cubierta, de hecho, por esa razon ya es inutil el UserReadOnlyPermission, pero dejemoslo activo
    queryset = Order.objects.filter(active=True)

    def patch(self, request, *args, **kwargs):
        print("Pasó por aqui: ", request.data)
        return super().patch(request, *args, **kwargs)


class UserOrderViewSet(SafeViewSet):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Order.objects.filter(active=True, user=self.request.user.id)


class AlegraUserViewSet(SafeViewSet):
    serializer_class = AlegraUserSerializer
    permission_classes = (IsAdminUser,)
    queryset = AlegraUser.objects.filter(active=True)


class WelcomeStaffView(APIView):
    def get(self, request, format=None):
        serializer = (
            WelcomeStaffSerializer()
        )  # El serializador solito agarra los registros, usara UserSerializer
        return Response(serializer.data)


class WelcomeSuperUserView(APIView):
    def get(self, request, format=None):
        serializer = (
            WelcomeSuperUserSerializer()
        )  # El serializador solito agarra los registros, usara UserSerializer
        return Response(serializer.data)


class NoteViewSet(SafeViewSet):
    serializer_class = NoteSerializer
    permission_classes = (IsAdminUser,)
    queryset = Note.objects.all()


class LogViewSet(SafeViewSet):
    serializer_class = LogSerializer
    permission_classes = (IsAdminUser,)
    queryset = LogEntry.objects.all()


class ExportOrderPDFView(APIView):
    serializer_class = ExportOrderPDFSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            id = serializer.validated_data.get('order_id', None)
            if not id:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'Error': 'Invalid ID'})
            # Create bytestream buffer
            buf = io.BytesIO()
            # Create a BaseDocTemplate
            doc = BaseDocTemplate(buf, pagesize=letter)
            # Create a frame
            frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")

            # Create a PageTemplate
            template = PageTemplate(id="test", frames=frame)

            # Add PageTemplate to the BaseDocTemplate
            doc.addPageTemplates([template])

            # Add headings
            lines = [["ID", "Item", "Referencia", "Cantidad", "Precio", "Subtotal"]]

            order = OrderSerializer(Order.objects.get(id=id)).data
            products = OrderProductSerializer(
                Order_Product.objects.filter(order_id=id), many=True
            ).data

            for order_product in products:
                id = Paragraph(str(order_product["product"]["id"]), styles["Normal"])
                item = Paragraph(str(order_product["product"]["item"]), styles["Normal"])
                reference = Paragraph(
                    str(order_product["product"]["reference"]), styles["Normal"]
                )
                quantity = Paragraph(str(order_product["quantity"]), styles["Normal"])
                price = Paragraph(str(order_product["price"]) + "$", styles["Normal"])
                cost = Paragraph(str(order_product["cost"]) + "$", styles["Normal"])

                lines.append((id, item, reference, quantity, price, cost))

            col_widths = [10 * mm, 75 * mm, 25 * mm, 17 * mm, 20 * mm, 23 * mm]

            table = Table(lines, colWidths=col_widths, rowHeights=10 * mm)

            table.setStyle(
                TableStyle(
                    [
                        (
                            "VALIGN",
                            (0, 0),
                            (-1, -1),
                            "MIDDLE",
                        ),  # Vertically center-align all cells
                        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                        ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                        ("FONTSIZE", (0, 0), (-1, 0), 10),
                        ("FONTSIZE", (0, 1), (-1, -1), 7),
                    ]
                )
            )

            drawing = svg2rlg(BASE_DIR / "static_root" / "assets" / "logodimpro.svg")
            if not drawing:
                raise FileNotFoundError("The file 'assets/logodimpro.svg' could not be found.")
            drawing.width = 100
            drawing.height = 0
            drawing.hAlign = "CENTER"

            # Parse the date string into a datetime object
            order_date = datetime.strptime(order['date'], '%Y-%m-%dT%H:%M:%S.%f%z')
            formatted_date = order_date.strftime('%d %B %Y %H:%M')
            print(order)
            information = Paragraph(
                f"<b>ID de pedido:</b> {order['id']}<br/><b>Tipo de precio:</b> {order['pricetype']['name']}<br/><b>Cliente: </b>{order['contact_name']}<br/><b>Vendedor:</b> {order['user_name']}<br/><b>Email del Vendedor:</b> { order['user']['email'] }<br/><b>Items:</b> {len(products)}<br/><b>Total:</b> {order['total']}$<br/><b>Fecha:</b> {formatted_date}",
                styles["Normal"],
            )

            # Create a spacer
            spacer = Spacer(1, 12)

            # Create story
            story = [drawing, spacer, information, spacer, table]

            # Add table to BaseDocTemplate
            doc.build(story)
            buf.seek(0)

            return FileResponse(
                buf,
                as_attachment=True,
                filename=f"order{order['id']}{order['contact_name']}-{order_date.strftime('%d-%B-%Y-%H:%M')}.pdf",
            )
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.error_messages())
