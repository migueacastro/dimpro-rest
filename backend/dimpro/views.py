from auditlog.models import LogEntry
from django.contrib.admin.options import get_content_type_for_model
from dimpro.pagination import LogsResultsSetPagination, StardardResultsSetPagination
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from backend.settings import BASE_DIR, FRONTEND_URL
from adrf.views import APIView as AsyncAPIView
from django.db.models import F

from django.contrib.postgres.search import TrigramSimilarity
import os
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from dimpro.tasks import updatedb
from rest_framework import status
from rest_framework import generics
from django.db.models import Q
from dimpro.serializers import *
from dimpro.models import *
from auditlog.models import LogEntry
from dimpro.helpers import (
    SafeViewSet,
    NoteViewSet,
    IsStaff,
    UserReadOnlyPermission,
    Util,
    EmailMessage,
    GroupPermission,
)
from django.utils.translation import gettext as _
from django.contrib.sessions.models import Session
from django.middleware.csrf import get_token
from django.contrib.staticfiles import finders
from dimpro.helpers import partial_update_user, create_user
import datetime
from django_q.tasks import async_task
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import *
from django_filters.rest_framework.backends import DjangoFilterBackend
from dimpro.pagination import LogEntryFilter

# Create your views here.

# pdf exporting
from django.http import FileResponse
import io
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
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
from dimpro.tasks import encodeduser, ENDPOINT
import requests

styles = getSampleStyleSheet()


class UserRegistrationView(APIView):  # Aqui puedes retornar responses personalizadas
    serializer_class = UserRegistrationSerializer
    permission_classes = (
        AllowAny,
    )  # Estos son las classes que indican quienes pueden meterse a este endpoint

    def post(
        self, request, *args, **kwargs
    ):  # En registration solo manejaremos post, los demas quedaran como metodo no permitido
        return create_user(self, request, *args, **kwargs)


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
                action=LogEntry.Action.ACCESS,
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

    def get(self, request, *args, **kwargs):
        user_instance = request.user
        Session.objects.filter(session_key=request.session.session_key).delete()
        LogEntry.objects.create(
            content_type=get_content_type_for_model(User),
            action=LogEntry.Action.ACCESS,
            changes_text="User logged out",
            object_pk=user_instance.id,
            object_id=user_instance.id,
        )
        logout(request)

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
        print(user_instance.groups.all())
        if (not user_instance) or not (
            user_instance.groups.filter(name="staff").exists()
            or user_instance.groups.filter(name="admin").exists()
        ):
            raise AuthenticationFailed(
                {"password": ["Correo o contraseña incorrectos o invalidos."]}
            )

        login_serializer = self.serializer_class(data=request.data)
        if login_serializer.is_valid():
            login(request, user_instance)
            LogEntry.objects.create(
                content_type=get_content_type_for_model(User),
                action=LogEntry.Action.ACCESS,
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

    def patch(self, request):
        user = request.user
        if not user:
            raise AuthenticationFailed({"message": "Acceso no Autorizado."})
        # Pass user instance and partial=True for updating only provided fields
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class UserChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data.get("password", None)
            confirmPassword = serializer.validated_data.get("confirm_password", None)

            if password != confirmPassword:
                raise AuthenticationFailed(
                    {"confirm_password": ["Las contraseñas no coinciden."]}
                )

            user.set_password(password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserVerifyPasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = VerifyPasswordSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data.get("password", None)
            if not user.check_password(password):
                raise AuthenticationFailed(
                    {"password": ["La contraseña actual no es correcta."]}
                )
        return Response(status=status.HTTP_200_OK)


class UserViewSet(SafeViewSet):
    permission_classes = (IsAuthenticated, GroupPermission)
    serializer_class = UserSerializer
    queryset = (
        User.objects.filter(active=True)
        .exclude(groups__name="staff")
        .exclude(groups__name="admin")
        .order_by("name")
    )  # If this line does not work i will nuke Copilot

    def retrieve(self, request, *args, **kwargs):
        object_instance = self.get_object()
        return Response(UserNestedSerializer(object_instance).data)

    def create(self, request, *args, **kwargs):
        return create_user(self, request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return partial_update_user(self, request, *args, **kwargs)


class RefreshCSRFTokenView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response({"csrftoken": get_token(request)})


class StaffViewSet(SafeViewSet):
    permission_classes = (IsAdminUser, GroupPermission)
    serializer_class = UserNestedSerializer
    queryset = (
        User.objects.filter(groups__name__in=["staff", "admin"], active=True)
        .distinct()
        .order_by("name")
    )
    superuser_only = True

    def create(self, request, *args, **kwargs):
        return create_user(self, request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return partial_update_user(self, request, *args, **kwargs)


class ProductViewSet(SafeViewSet):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated, GroupPermission)
    queryset = Product.objects.filter(active=True).order_by(
        "item"
    )  # Aqui no por ejemplo


class ContactViewSet(SafeViewSet):
    serializer_class = ContactSerializer
    permission_classes = (IsAuthenticated, GroupPermission)
    queryset = Contact.objects.filter(active=True).order_by("name")


class OrderProductViewSet(SafeViewSet):
    serializer_class = OrderProductSerializer
    permission_classes = (IsAuthenticated, GroupPermission)
    queryset = Order_Product.objects.all()


class PriceTypeViewSet(SafeViewSet, GroupPermission):
    serializer_class = PriceTypeSerializer
    permission_classes = (IsAuthenticated, GroupPermission)
    queryset = PriceType.objects.filter(active=True)


class OrderViewSet(SafeViewSet):  # Te muestra de una vez sus propios OrderProducts
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, GroupPermission)
    # No hay que preocuparse por lecturas indebidas,
    # El CORS no permitiria cualquier IP acceder al API excepto por el del mismo frontend desde la nube
    # Entonces, esa vulnerabilidad ya está cubierta, de hecho, por esa razon ya es inutil el UserReadOnlyPermission, pero dejemoslo activo
    queryset = Order.objects.filter(active=True).order_by("status").order_by("-date")

    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class UserOrderViewSet(SafeViewSet):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(active=True, user=self.request.user.id).order_by(
            "-date"
        )


class AlegraUserViewSet(SafeViewSet):
    serializer_class = AlegraUserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = AlegraUser.objects.filter(active=True)


class WelcomeStaffView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        serializer = (
            WelcomeStaffSerializer()
        )  # El serializador solito agarra los registros, usara UserSerializer
        return Response(serializer.data)


class WelcomeSuperUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        serializer = (
            WelcomeSuperUserSerializer()
        )  # El serializador solito agarra los registros, usara UserSerializer
        return Response(serializer.data)


class NoteViewSet(NoteViewSet):  # because date cannot be updated
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticated, GroupPermission)
    queryset = Note.objects.filter(active=True)


class LogViewSet(SafeViewSet):
    serializer_class = LogSerializer
    pagination_class = LogsResultsSetPagination
    permission_classes = (IsAuthenticated, GroupPermission)
    queryset = LogEntry.objects.all().order_by("-timestamp")
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = LogEntryFilter
    search_fields = [
        "actor__name",
        "actor__email",
        "content_type__model",
        "changes_text",
        "action",
        "timestamp",
        "remote_addr",
    ]
    ordering_fields = [
        "actor_id",
        "actor",
        "actor__name",
        "actor__email",
        "content_type__model",
        "changes_text",
        "timestamp",
        "remote_addr",
        "action",
    ]


class ExportOrderPDFView(APIView):
    serializer_class = ExportOrderPDFSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            id = serializer.validated_data.get("order_id", None)
            if not id:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST, data={"Error": "Invalid ID"}
                )

            # New small paragraph font style
            small_style = ParagraphStyle(
                "small",
                parent=styles["Normal"],
                fontSize=7,
                leading=8,  # adjust as needed
                spaceBefore=0,
                spaceAfter=0,
            )

            # Create bytestream buffer
            buf = io.BytesIO()
            # Create a BaseDocTemplate
            doc = BaseDocTemplate(buf, pagesize=letter)
            # Create a frame
            frame = Frame(
                doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal"
            )

            # Create a PageTemplate
            template = PageTemplate(id="test", frames=frame)

            # Add PageTemplate to the BaseDocTemplate
            doc.addPageTemplates([template])

            # Add headings
            lines = [["ID", "Item", "Referencia", "Cantidad", "Precio", "Subtotal"]]

            order = OrderSerializer(Order.objects.get(id=id)).data
            products = order["products"]

            for order_product in products:
                id = Paragraph(str(order_product["product"]["id"]), small_style)
                item = Paragraph(str(order_product["product"]["item"]), small_style)
                reference = Paragraph(
                    str(order_product["product"]["reference"]), small_style
                )
                quantity = Paragraph(str(order_product["quantity"]), small_style)
                price = Paragraph(str(order_product["price"]) + "$", small_style)
                cost = Paragraph(str(order_product["cost"]) + "$", small_style)

                lines.append((id, item, reference, quantity, price, cost))
            available_width = doc.width
            col_widths = [
                available_width * 0.1,
                available_width * 0.25,
                available_width * 0.2,
                available_width * 0.15,
                available_width * 0.15,
                available_width * 0.15,
            ]

            table = Table(lines, colWidths=col_widths)

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
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 10),
                        ("FONTSIZE", (0, 1), (-1, -1), 7),
                    ]
                )
            )

            drawing = svg2rlg(BASE_DIR / "static_root" / "assets" / "logodimpro.svg")
            if not drawing:
                raise FileNotFoundError(
                    "The file 'assets/logodimpro.svg' could not be found."
                )
            drawing.width = 100
            drawing.height = 0
            drawing.hAlign = "CENTER"

            # Parse the date string into a datetime object
            order_date = datetime.datetime.strptime(
                order["date"], "%Y-%m-%dT%H:%M:%S.%f%z"
            )
            formatted_date = order_date.strftime("%d %B %Y %H:%M")
            print(order)
            for field in order:
                if field == None:
                    order[field] = "Ninguno"
            information = Paragraph(
                f"<b>ID de pedido:</b> {order['id']}<br/><b>Tipo de precio:</b> {order['pricetype']['name'] if order['pricetype'] else 'Ninguno'}<br/><b>Cliente: </b>{order['contact_name']}<br/><b>Vendedor:</b> {order['user_name']}<br/><b>Email del Vendedor:</b> { order['user']['email'] }<br/><b>Items:</b> {len(products)}<br/><b>Total:</b> {order['total'] if order['total'] else '0'}$<br/><b>Fecha:</b> {formatted_date}",
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
                filename=f"order{order['id']}{order['contact_name']}-{order_date.strftime('%Y%m%d_%H%M%S')}.pdf",
            )  # The file response that returns a buffer as an attachment
        return Response(
            status=status.HTTP_400_BAD_REQUEST, data=serializer.error_messages()
        )


class ExportCatalogPDFView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        buf = io.BytesIO()
        doc = BaseDocTemplate(buf, pagesize=letter)
        frame = Frame(
            doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal"
        )

        small_style = ParagraphStyle(
            "small",
            parent=styles["Normal"],
            fontSize=7,
            leading=8,  # adjust as needed
            spaceBefore=0,
            spaceAfter=0,
        )
        template = PageTemplate(id="test", frames=frame)

        doc.addPageTemplates([template])

        lines = [["ID", "Item", "Detalles", "Referencia", "Cantidad"]]
        products = Product.objects.filter(active=True).order_by("item")
        if not products.exists():
            return Response({"error": "No products found."}, status=404)

        serialized_products = ProductSerializer(products, many=True).data

        for product in serialized_products:
            id = Paragraph(str(product["id"]), small_style)
            item = Paragraph(str(product["item"]), small_style)
            details = Paragraph(str(product["details"] or "Ninguno"), small_style)
            reference = Paragraph(str(product["reference"] or "Ninguno"), small_style)
            quantity = Paragraph(str(product["available_quantity"]), small_style)
            if product.get("prices") and len(product["prices"]) > 0:
                price_value = str(list(list(product["prices"])[0].values())[0]) + "$"
            else:
                price_value = "Ninguno"

            # price = Paragraph(price_value, small_style)

            lines.append((id, item, details, reference, quantity))

        available_width = doc.width
        col_widths = [
            available_width * 0.10,
            available_width * 0.20,
            available_width * 0.30,
            available_width * 0.2,
            available_width * 0.2,
            # available_width * 0.10,
        ]

        table = Table(lines, colWidths=col_widths)

        table.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 10),
                    ("FONTSIZE", (0, 1), (-1, -1), 7),
                ]
            )
        )

        drawing = svg2rlg(BASE_DIR / "static_root" / "assets" / "logodimpro.svg")
        if not drawing:
            raise FileNotFoundError(
                "The file 'assets/logodimpro.svg' could not be found."
            )
        drawing.width = 100
        drawing.height = 0
        drawing.hAlign = "CENTER"

        spacer = Spacer(1, 12)

        information = Paragraph(
            f"<p>Catálogo de productos actual</p>",
            styles["Normal"],
        )
        current_date = Paragraph(
            f"<h4><b>Fecha:</b> {str(datetime.datetime.today().strftime('%d/%m/%Y %H:%M'))}</h4>",
            styles["Normal"],
        )

        story = [drawing, spacer, information, current_date, spacer, table]

        doc.build(story)
        buf.seek(0)

        return FileResponse(
            buf,
            as_attachment=True,
            filename=f"catalog-{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        )


class UpdateDBView(AsyncAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            # Schedule the updatedb task asynchronously.
            updatedb()
            return Response(
                status=status.HTTP_200_OK,
                data={"message": "Database update updated successfully."},
            )
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=str(e))


class AlegraTokenView(APIView):
    serializer_class = AlegraAPITokenSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        alegra_object = AlegraUser.objects.get(id=1)
        alegra_serialized = AlegraAPITokenSerializer(alegra_object).data
        return Response(status=status.HTTP_200_OK, data=alegra_serialized)

    def patch(self, request):
        try:
            alegra_object = AlegraUser.objects.get(id=1)
        except AlegraUser.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "Alegra user not found."},
            )
        serializer = self.serializer_class(
            alegra_object, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class RequestPasswordResetView(generics.GenericAPIView):

    serializer_class = ResetPasswordEmailSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get("email", None)

        if User.objects.filter(email=email).exists():

            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(str(user.id).encode())
            token = PasswordResetTokenGenerator().make_token(user)

            current_site = FRONTEND_URL
            relativeLink = f"password-reset/{uidb64}/{token}"
            absurl = current_site + relativeLink

            email_body = (
                f"Hola {user.name.split()[0]}, \nUsa el enlace para reestablecer tu contraseña.  \n"
                + absurl
                + "\n\nSi no solicitaste este cambio, ignora este mensaje.  \n\nGracias por usar. Dimpro."
            )
            data = {
                "email_body": email_body,
                "to_email": user.email,
                "email_subject": "Dimpro | Reestablecer contraseña",
            }
            Util.send_email(data)
            return Response(
                {"message": "Password reset link has been sent to your email"},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"message": "Email not found"}, status=status.HTTP_400_BAD_REQUEST
        )


class PasswordTokenCheckView(generics.GenericAPIView):

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {"message": "Token is not valid", "uidb64": uidb64, "token": token},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(
                {"message": "Credentials are valid", "uidb64": uidb64, "token": token},
                status=status.HTTP_200_OK,
            )

        except DjangoUnicodeDecodeError as identifier:
            return Response(
                {"message": "Token is not valid", "uidb64": uidb64, "token": token},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = (AllowAny,)

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {"success": True, "message": "Password reset success"},
            status=status.HTTP_200_OK,
        )


class GroupViewSet(SafeViewSet):
    serializer_class = GroupSerializer
    permission_classes = (IsAdminUser,)
    queryset = Group.objects.all()


class PermissionViewSet(SafeViewSet):
    permission_classes = (IsAdminUser,)
    serializer_class = PermissionSerializer
    queryset = Permission.objects.filter(
        content_type__app_label__in=["auditlog", "dimpro"]
    )


class UserInvoiceViewSet(SafeViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        search = self.request.query_params.get('search', self.request.user.name).strip()
        return Invoice.objects.annotate(
            similarity=TrigramSimilarity('seller_name', search)
        ).filter(
            similarity__gte=0.5
        ).order_by("-date")
    

class ContactAddRequestViewSet(SafeViewSet):
    serializer_class = ContactAddRequestSerializer
    permission_classes = (IsAuthenticated, )
    queryset = ContactAddRequest.objects.filter(active=True).order_by("-date")


class ContactAddRequestApproval(APIView):
    serializer_class = ContactAddRequestAprovalSerializer
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            id = serializer.validated_data.get("id", None)
            if not id:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST, data={"Error": "Invalid ID, non present"}
                )
            elif not ContactAddRequest.objects.filter(id=id, active=True).exists():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST, data={"Error": "Invalid ID or Request"}
                )
        serializer_data = serializer.validated_data
        contact_add_request = ContactAddRequest.objects.get(id=serializer_data.get("id", ""))
        alegra_seller = AlegraSeller.objects.annotate(
            similarity=TrigramSimilarity('name', contact_add_request.user.name)
        ).filter(
            similarity__gte=0.5
        ).first()

        client = {'accept': 'application/json',  "content-type": "application/json",'authorization': f'Basic {encodeduser()}'}
        url = f"{ENDPOINT}contacts"
        payload = {
            "address": {
                "city": contact_add_request.city,
                "address": contact_add_request.address
            },
            "name": contact_add_request.name,
            "identification": contact_add_request.identification,
            "phonePrimary": contact_add_request.phonePrimary,
            "seller": alegra_seller.id if alegra_seller else None,
            "term": "1",
            "email": contact_add_request.email,
            "type": "client",
            "status": "active"
        }
        response = requests.post(url, json=payload, headers=client)
        if response.ok:
            data = response.json()
            Contact.objects.create(id=data.get("id",None), name=contact_add_request.name, active=True)
            contact = ContactAddRequest.objects.get(id=id)
            contact.status = "aprobado"
            contact.save()
            return Response(
                status=status.HTTP_200_OK, 
                data={"message": "Cliente agregado exitosamente"}
            ) 
        else:
            try:
                error_data = response.json()
                return Response(
                    status=status.HTTP_400_BAD_REQUEST, 
                    data=error_data
                )
            except ValueError:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST, 
                    data={"Error": "Unknown error occurred"}
                )
        
