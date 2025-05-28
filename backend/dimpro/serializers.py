from django.utils.regex_helper import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model
from dimpro.models import *
from auditlog.models import LogEntry
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from auditlog.models import LogEntry
from drf_writable_nested.serializers import (
    WritableNestedModelSerializer,
)  # java ahh class
from django.utils.encoding import force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext
from dimpro.helpers import translate_permission_name, translate_permission_content_type



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, style={"input_type": "password"}, min_length=8, max_length=100
    )
    confirmPassword = serializers.CharField(
        write_only=True, style={"input_type": "password"}, min_length=8, max_length=100
    )

    class Meta:
        model = get_user_model()
        fields = ["email", "name", "password", "confirmPassword", "phonenumber"]

    def create(self, validated_data):
        validated_data.pop(
            "confirmPassword", None
        )  # This field is validated, but wont be used for user creation
        user_instance = User.objects.create_user(**validated_data)
        user_instance.save()
        return user_instance


class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=100, style={"input_type": "password"}, write_only=True
    )
    email = serializers.EmailField(max_length=100, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ["email", "password"]


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=100, style={"input_type": "password"}, write_only=True
    )
    confirm_password = serializers.CharField(
        max_length=100, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = get_user_model()
        fields = ["password", "confirm_password"]


class VerifyPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=100, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = get_user_model()
        fields = ["password"]


class PermissionSerializer(serializers.ModelSerializer):
    translated_name = serializers.SerializerMethodField()
    translated_content_type = serializers.SerializerMethodField()
    class Meta:
        model = Permission
        fields = ["id", "codename","name", "translated_name", "translated_content_type"]

    def get_translated_name(self, obj):
        return translate_permission_name(obj.name) if obj.name else ""
    def get_translated_content_type(self, obj):
        return translate_permission_content_type(obj.codename) if obj.codename else ""
      


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ["id", "name", "permissions"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        data["permissions"] = PermissionSerializer(instance.permissions.all(), many=True).data
        return data


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=100, style={"input_type": "password"}, write_only=True
    )

    confirmPassword = serializers.CharField(
        max_length=100, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "email",
            "name",
            "password",
            "confirmPassword",
            "phonenumber",
            "groups",
            "date_joined",
            "last_login",
        ]
        

    def update(self, instance, validated_data):
        
        if validated_data.get("confirmPassword"):
            validated_data.pop("confirmPassword")
        if "name" in validated_data:
            instance.name = validated_data.get("name")
        if "email" in validated_data:
            instance.email = validated_data.get("email")
        if "password" in validated_data:
            instance.set_password(validated_data.get("password"))
        if "phonenumber" in validated_data:
            instance.phonenumber = validated_data.get("phonenumber")
        if "groups" in validated_data:
            instance.groups.set(validated_data.pop("groups", None))
        return instance

    def to_representation(self, instance):
        self.fields["groups"] = GroupSerializer(many=True)
        return super().to_representation(instance)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "item", "details", "reference", "available_quantity", "prices"]


class PriceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceType
        fields = ["id", "name"]


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id","note", "name", "date","active"]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "name", "date_joined"]


class OrderProductSerializer(
    WritableNestedModelSerializer
):  # Se crea completo, producto es obligatorio
    active = serializers.BooleanField()

    class Meta:
        model = Order_Product
        fields = ["id", "product", "price", "quantity", "cost", "order", "active"]

    def create(self, validated_data):
        product = validated_data.pop("product")
        order = validated_data.pop("order")
        order_product_instance, created = Order_Product.objects.get_or_create(
            product=product, order=order, defaults=validated_data
        )
        if not created:
            for key, value in validated_data.items():
                setattr(order_product_instance, key, value)
            order_product_instance.save()
        return order_product_instance

    def to_representation(self, instance):
        self.fields["product"] = ProductSerializer()
        return super().to_representation(instance)


class OrderSerializer(
    serializers.ModelSerializer
):  # Se crea, luego se añaden productos, cada producto no es obligatorio
    total = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    date = serializers.DateTimeField(read_only=True)
    products = serializers.SerializerMethodField(required=False)
    user_name = serializers.SerializerMethodField(read_only=True)
    contact_name = serializers.SerializerMethodField(read_only=True)
    product_count = serializers.SerializerMethodField(read_only=True)
    date_format = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "contact",
            "date",
            "total",
            "pricetype",
            "products",
            "user",
            "user_name",
            "contact_name",
            "product_count",
            "date_format",
        ]

    def get_products(self, obj):
        list_products = Order_Product.objects.filter(active=True, order=obj.id)
        if list_products:
            return OrderProductSerializer(list_products, many=True).data
        return []

    def get_user_name(self, obj):
        return obj.user.name

    def get_contact_name(self, obj):
        if obj.contact:
            return obj.contact.name
        return "Ninguno"

    def get_date_format(self, obj):
        return obj.date.strftime("%Y/%m/%d %H:%M")

    def get_product_count(self, obj):
        return Order_Product.objects.filter(active=True, order=obj.id).count()

    def to_representation(self, instance):
        self.fields["pricetype"] = PriceTypeSerializer()
        self.fields["user"] = UserSerializer()
        return super().to_representation(instance)


class AlegraUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlegraUser
        fields = ["email", "token", "active"]


class WelcomeStaffSerializer(
    serializers.Serializer
):  # No es un modelo, es un simple Serializer
    orders = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()

    class Meta:
        fields = ["orders", "users"]

    def get_orders(self, obj):
        list_orders = Order.objects.filter(
            active=True, status="Pendiente"
        )  # En caso de error: Hay que ver si "Pendiente" es aceptado y no solo "pendiente"
        return OrderSerializer(
            list_orders, many=True
        ).data  # Retorna la data serializada de cada Orden

    def get_users(self, obj):
        list_users = User.objects.filter(
            active=True, is_staff=False, is_superuser=False
        )
        return UserSerializer(
            list_users, many=True
        ).data  # Ahorrara informacion pasada en la pantalla de inicio


class WelcomeSuperUserSerializer(
    WelcomeStaffSerializer
):  # Hereda WelcomeStaffSerializer
    staff_users = serializers.SerializerMethodField()

    class Meta:
        fields = ["orders", "users", "staff_users"]

    def get_staff_users(self, obj):
        list_staff_users = User.objects.filter(active=True, is_staff=True)
        return UserSerializer(list_staff_users, many=True).data


class UserNestedSerializer(UserSerializer):
    orders = serializers.SerializerMethodField(
        read_only=True
    )  # fiuh, no era necesario el WritableNestedSerializer
    date_joined_format = serializers.SerializerMethodField(read_only=True)
    last_login_format = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "email",
            "name",
            "password",
            "confirmPassword",
            "phonenumber",
            "is_staff",
            "is_superuser",
            "orders",
            "date_joined_format",
            "last_login_format",
            "groups",
        ]

    def get_orders(self, obj):
        list_orders = Order.objects.filter(active=True, user=obj.id)
        return OrderSerializer(
            list_orders, many=True
        ).data  # Para esta vista, quiero omitir lo campos de productos,

    def get_date_joined_format(self, obj):
        return obj.date_joined.strftime("%Y/%m/%d %H:%M") if obj.date_joined else ""

    def get_last_login_format(self, obj):
        return (
            obj.last_login.strftime("%Y/%m/%d %H:%M") if obj.last_login else "Ninguno"
        )


class ExportOrderPDFSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()

    class Meta:
        fields = ["order_id"]


class LogSerializer(serializers.ModelSerializer):
    actor_name = serializers.SerializerMethodField(read_only=True)
    actor_email = serializers.SerializerMethodField(read_only=True)
    content_type_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = LogEntry
        fields = "__all__"
    
    def get_actor_name(self, obj):
        if obj.actor:
            return User.objects.get(id=obj.actor.id).name
        return None
    def get_content_type_name(self, obj):
        if obj.content_type:
            return obj.content_type.model
        return None
    def get_actor_email(self, obj):
        if obj.actor:
            return User.objects.get(id=obj.actor.id).email
        return None


class AlegraAPITokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlegraUser
        fields = ["email", "token"]


class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ["email"]


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=100, style={"input_type": "password"}, write_only=True
    )
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ["password", "token", "uidb64"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")

            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("The reset link is invalid", 401)

            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise AuthenticationFailed("The reset link is invalid", 401)
