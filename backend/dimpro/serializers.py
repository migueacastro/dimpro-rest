from django.utils.regex_helper import Group
from rest_framework import serializers 
from django.contrib.auth import get_user_model
from dimpro.models import *
from drf_writable_nested.serializers import WritableNestedModelSerializer # java ahh class

class UserRegistrationSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True, style={"input_type":"password"}, min_length=8, max_length=100)
  confirmPassword = serializers.CharField(write_only=True, style={"input_type":"password"}, min_length=8, max_length=100)
  class Meta:
    model = get_user_model() 
    fields = ['email', 'name', 'password', 'confirmPassword','phonenumber']

  def create(self, validated_data):
    validated_data.pop('confirmPassword', None) # This field is validated, but wont be used for user creation
    user_instance = User.objects.create_user(**validated_data)
    user_instance.save()
    return user_instance



class UserLoginSerializer(serializers.ModelSerializer): 
  password = serializers.CharField(max_length=100, style={"input_type": "password"}, write_only=True)
  email = serializers.EmailField(max_length=100, write_only=True)
  class Meta:
    model = get_user_model()
    fields = ["email", "password"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
 

class UserSerializer(serializers.ModelSerializer):  
  password = serializers.CharField(max_length=100, style={"input_type":"password"}, write_only=True) 
  confirmPassword = serializers.CharField(max_length=100, style={"input_type":"password"}, write_only=True) 
  class Meta:
    model = get_user_model() 
    fields = ['id', 'email', 'name', 'password', 'confirmPassword', 'phonenumber', 'groups']

  def create(self, validated_data):
    validated_data.pop('confirmPassword')
    
    user_groups = validated_data.pop('groups')
    user_instance = User.objects.create_user(**validated_data) 
    user_instance.groups.set(user_groups)
    user_instance.save()
    return user_instance

  def update(self, instance, validated_data):

    user_groups = validated_data.pop('groups', None)
    validated_data.pop('confirmPassword')
    self.update(instance, validated_data)
    instance.groups.set(user_groups)
    instance.save()
    return instance 

  def to_representation(self, instance):
    self.fields['groups'] = GroupSerializer(many = True)
    return super().to_representation(instance)

class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields = ['id', 'item','details','reference','available_quantity', 'prices'] 

class PriceTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = PriceType
    fields = ['id', 'name']

class ContactSerializer(serializers.ModelSerializer):
  class Meta:
    model = Contact 
    fields = ['id','name','date_joined'] 

class OrderProductSerializer(WritableNestedModelSerializer): # Se crea completo, producto es obligatorio
  product = ProductSerializer()
  class Meta:
    model = Order_Product
    fields = ['product', 'price', 'quantity', 'cost', 'order']

class OrderSerializer(serializers.ModelSerializer): # Se crea, luego se añaden productos, cada producto no es obligatorio   
  total = serializers.FloatField(required=False)
  pricetype = serializers.IntegerField(required=False);
  date = serializers.DateTimeField(read_only=True)
  products = serializers.SerializerMethodField(required=False)   
  user_name = serializers.SerializerMethodField(read_only=True)
  contact_name = serializers.SerializerMethodField(read_only=True)
  product_count = serializers.SerializerMethodField(read_only=True)
  date_format = serializers.SerializerMethodField(read_only=True)
  class Meta:
    model = Order
    fields = ['id','status','contact','date','total','pricetype', 'products', 'user', 'user_name', 'contact_name', 'product_count', 'date_format']

  def get_products(self, obj):
    list_products = Order_Product.objects.filter(active=True, order=obj.id)
    if list_products:
        return OrderProductSerializer(list_products, many=True).data
    return [];

  def get_user_name(self, obj):
    return obj.user.name
    
  def get_contact_name(self,obj):
        if obj.contact:
            return obj.contact.name
        return 'Ninguno'

  def get_date_format(self,obj):
    return obj.date.strftime('%Y/%m/%d %H:%M')

  def get_product_count(self,obj):
    return Order_Product.objects.filter(active=True, order=obj.id).count()

  def to_representation(self, instance):
    self.fields['pricetype'] = PriceTypeSerializer();
    self.fields['user'] = UserSerializer();
    return super().to_representation(instance)

class AlegraUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = AlegraUser
    fields = ['email','token', 'active']

class WelcomeStaffSerializer(serializers.Serializer): # No es un modelo, es un simple Serializer
  orders = serializers.SerializerMethodField()
  users = serializers.SerializerMethodField()
  class Meta:
    fields = ['orders', 'users']
  
  def get_orders(self, obj):
    list_orders = Order.objects.filter(active=True, status="Pendiente") # En caso de error: Hay que ver si "Pendiente" es aceptado y no solo "pendiente"
    return OrderSerializer(list_orders, many=True).data # Retorna la data serializada de cada Orden
  
  def get_users(self, obj):
    list_users = User.objects.filter(active=True, is_staff=False, is_superuser=False)
    return UserSerializer(list_users, many=True).data # Ahorrara informacion pasada en la pantalla de inicio
  
class WelcomeSuperUserSerializer(WelcomeStaffSerializer): # Hereda WelcomeStaffSerializer
  staff_users = serializers.SerializerMethodField()
  class Meta:
    fields = ['orders', 'users', 'staff_users']
  def get_staff_users(self, obj):
    list_staff_users = User.objects.filter(active=True, is_staff=True)
    return UserSerializer(list_staff_users, many=True).data
  

class UserNestedSerializer(UserSerializer):
  orders = serializers.SerializerMethodField(read_only=True) # fiuh, no era necesario el WritableNestedSerializer
  date_joined_format = serializers.SerializerMethodField(read_only=True)
  last_login_format = serializers.SerializerMethodField(read_only=True) 
  class Meta:
    model = get_user_model()
    fields = ['id', 'email', 'name', 'password', 'confirmPassword', 'phonenumber', 'is_staff', 'is_superuser', 'orders', 'date_joined_format', 'last_login_format']

  def get_orders(self, obj):
    list_orders = Order.objects.filter(active=True, user=obj.id)
    return OrderSerializer(list_orders, many=True).data # Para esta vista, quiero omitir lo campos de productos, 
  def get_date_joined_format(self,obj):
        return obj.date_joined.strftime('%Y/%m/%d %H:%M') if obj.date_joined else ''
  def get_last_login_format(self, obj):
    return obj.last_login.strftime('%Y/%m/%d %H:%M') if obj.last_login else 'Ninguno'
class LogSerializer(serializers.ModelSerializer):
    pass
