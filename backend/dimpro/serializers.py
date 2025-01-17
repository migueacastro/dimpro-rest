from rest_framework import serializers 
from django.contrib.auth import get_user_model
from dimpro.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
  pass

class UserRegistrationSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True, style={"input_type":"password"}, min_length=8, max_length=100)
  confirmPassword = serializers.CharField(write_only=True, style={"input_type":"password"}, min_length=8, max_length=100)
  class Meta:
    model = get_user_model() 
    fields = ['email', 'name', 'password', 'confirmPassword']

  def create(self, validated_data):
    user_password = validated_data.get('password', None)
    user_instance = self.Meta.model(email = validated_data.get('email'), name = validated_data.get('name'))
    user_instance.set_password(user_password)
    user_instance.save()
    return user_instance



class UserLoginSerializer(serializers.ModelSerializer): 
  password = serializers.CharField(max_length=100, style={"input_type": "password"}, write_only=True)
  email = serializers.EmailField(max_length=100, write_only=True)
  class Meta:
    model = get_user_model()
    fields = ["email", "password"]
  
class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(max_length=100, style={"input_type":"password"}, write_only=True) 
  confirmPassword = serializers.CharField(max_length=100, style={"input_type":"password"}, write_only=True) 
  class Meta:
    model = get_user_model() 
    fields = ['id', 'email', 'name', 'password', 'confirmPassword', 'is_staff', 'is_superuser']

  def create(self, validated_data):
    user_password = validated_data.get('password', None) 
    user_instance = self.Meta.model(email= validated_data.get('email'), name = validated_data.get('name')) 
    user_instance.set_password(user_password) 
    user_instance.is_staff = validated_data.get('is_staff', False)
    user_instance.is_superuser = validated_data.get('is_superuser', False)
    user_instance.save()
    return user_instance

  def update(self, instance, validated_data): 
    user_password = validated_data.get('password', None) 
    instance.set_password(user_password)
    instance.email = validated_data.get('email', instance.email)
    instance.name = validated_data.get('name', instance.name) 
    instance.is_staff = validated_data.get('is_staff', instance.is_staff)
    instance.is_superuser = validated_data.get('is_superuser',instance.is_superuser)
    instance.save()
    return instance 
    
  
class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields = ['id', 'item','details','reference','available_quantity'] 

class ContacSerializer(serializers.ModelSerializer):
  class Meta:
    model = Contact 
    fields = ['id','name','date_joined'] 

class OrderSerializer(serializers.ModelSerializer):
  class Meta:
    model = Order
    fields = ['id','status','contact','date','total','pricetype']

