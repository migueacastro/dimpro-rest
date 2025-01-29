from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin, Group, timezone
from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from auditlog.registry import auditlog
# Create your models here.
class CustomUserManager(UserManager): 
    def _create_user(self, email, password, phonenumber, **extra_fields):
        if not email:
            raise ValueError("No has ingresado una direccion e-mail valida.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.phonenumber = phonenumber
        user.save(using=self._db)
        return user # I dont know why this method is here, but it isnt bothering anyone, so it stays. It's django's primitive _create user iirc
    
    def create_user(self, email=None, password=None, phonenumber=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        user_group, created = Group.objects.get_or_create(name="user")        
        user.groups.add(user_group)
        return user

    def create_superuser(self, email=None, password=None, phonenumber=None, **extra_fields):
        user = self.create_user(email, password, phonenumber,**extra_fields)
        staff_group, created = Group.objects.get_or_create(name="staff")
        superuser_group, created = Group.objects.get_or_create(name="admin") # it lacked staff group
        user_group, created = Group.objects.get_or_create(name="user")        
        user.groups.add(superuser_group)
        user.groups.add(staff_group)
        user.groups.add(user_group)
        return user

    def create_staff(self, email=None, password=None, phonenumber=None, **extra_fields):
        user = self.create_user(email, password, phonenumber,**extra_fields)
        staff_group, created = Group.objects.get_or_create(name="staff")
        user_group, created = Group.objects.get_or_create(name="user")        
        user.groups.add(staff_group)
        user.groups.add(user_group)
        return user

class User(AbstractBaseUser, PermissionsMixin): 
    id = models.AutoField(primary_key=True)
    email = models.EmailField(blank=True, default='', unique=True)
    name = models.CharField(max_length=255, blank=True, default='')
    last_name = models.CharField(max_length=255, blank=True, default='')
    phoneregex = RegexValidator(regex=r"^\+?58?\d{11,15}$")
    phonenumber = models.CharField(
        validators=[phoneregex], max_length=17, blank=True, null=True # Usar este campo. el regex ya esta en los validadores xd
    )
    active = models.BooleanField(default=True) # lo modifique para que se adapte al SafeViewSet
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name or self.email.split('@')[0]

    def user_orders(self):
        return Order.objects.filter(user_email=self.email).count()

    # Properties used only during admin interface
    @property
    def is_staff(self):
        return User.objects.get(id=self.id).groups.filter(name="staff").exists()

    @property
    def is_superuser(self):
        return User.objects.get(id=self.id).groups.filter(name="admin").exists()

auditlog.register(User, exclude_fields=["password"]) #adding this will log the model

class Product(models.Model): 
    item = models.CharField(max_length=64, unique=False)
    active = models.BooleanField(null = False, default=True) 
    prices = models.JSONField(blank=True, default=dict)
    details = models.CharField(max_length=128, null = True)
    reference = models.CharField(max_length=64, unique=True, null = True)
    available_quantity = models.IntegerField(validators = [
        MinValueValidator(1)
    ])

    def __str__(self):
        return str(self.id)

    # Create a dictionary based on the product
    def to_dict(self):
        return {
            'id': self.id,
            'item': self.item,
            'details': self.details,
            'reference': self.reference,
            'prices': self.prices,
            'available_quantity': self.available_quantity
        }
auditlog.register(Product)

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    url = models.CharField(max_length=256)
auditlog.register(Image)

class AlegraUser(models.Model):
    email = models.CharField(max_length=128)
    token = models.CharField(max_length=256)
    active = models.BooleanField(null = False, default=True) 
auditlog.register(AlegraUser)

class Contact(models.Model): 
    name = models.CharField(max_length=128)
    date_joined = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(null = False, default=True)
    def __str__(self):
        return str(self.id)
auditlog.register(Contact)

# TODO: viewset para Order
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True)
    status = models.CharField(max_length=16,choices= [
        ('preparado', 'Preparado'),
        ('pendiente', 'Pendiente')
    ])
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='orders', null=True)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=7, decimal_places=2)
    pricetype = models.CharField(max_length=128, null=True)
    active = models.BooleanField(null = False, default=True)
    def product_categories(self):
        return Order_Product.objects.filter(order_id=self.id).count()

    def __str__(self):
        return str(self.id)
auditlog.register(Order)


class PriceType(models.Model):
    name = models.CharField(max_length = 128)
    default = models.BooleanField(default=False)
auditlog.register(PriceType)

class Order_Product(models.Model):
    id = models.AutoField(primary_key=True)
    order =  models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    dprice = models.DecimalField(max_digits=7,decimal_places=2, default=0)
    cost = models.DecimalField(max_digits=7,decimal_places=2, default=0)
    quantity = models.IntegerField(validators = [
        MinValueValidator(1)
    ])
    def __str__(self):
        return str(self.id)
auditlog.register(Order_Product)


class Note(models.Model):
    note = models.TextField()
    name = models.CharField(max_length=128)
    date = models.DateTimeField(auto_now_add=True)
auditlog.register(Note)


class Receivable(models.Model):
    active = models.BooleanField(default=False)
    seller = models.CharField(max_length=128, blank=True, null=True)
    client = models.CharField(max_length=128, blank=True, null=True)
    total = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateField(auto_now_add=False)
    number = models.CharField(max_length=128, blank=True, null=True)
auditlog.register(Receivable)

