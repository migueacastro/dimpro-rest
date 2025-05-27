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
        user = self.model(email=email,phonenumber=phonenumber, **extra_fields)
        user.set_password(password)
        user.phonenumber = phonenumber
        user.save(using=self._db)
        return user # I dont know why this method is here, but it isnt bothering anyone, so it stays. It's django's primitive _create user iirc
    
    def create_user(self, email=None, password=None, phonenumber=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.phonenumber = phonenumber
        user.save(using=self._db)
        user_group, created = Group.objects.get_or_create(name="user")        
        user.groups.add(user_group)
        return user

    def create_superuser(self, email=None, password=None, phonenumber=None, **extra_fields):
        user = self.create_user(email, password, phonenumber,**extra_fields)
        superuser_group, created = Group.objects.get_or_create(name="admin") # it lacked staff group     
        user.groups.add(superuser_group)
        return user

    def create_staff(self, email=None, password=None, phonenumber=None, **extra_fields):
        user = self.create_user(email, password, phonenumber,**extra_fields)
        staff_group, created = Group.objects.get_or_create(name="staff")  
        user.groups.add(staff_group)
        return user


class ExchangeCurrency(models.Model):
    iso_code = models.CharField(max_length=10)
    name = models.CharField(max_length=32)


class ExchangeRate(models.Model):
    from_currency = models.ForeignKey(ExchangeCurrency, on_delete=models.DO_NOTHING, null=False, blank=False, related_name="exchange_rates_from_currency")
    to_currency = models.ForeignKey(ExchangeCurrency, on_delete=models.DO_NOTHING, null=False, blank=False, related_name="exchange_rates_to_currency")
    datetime = models.DateTimeField(auto_now_add=True)
    rate = models.FloatField(null=False, blank= False)

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
        permissions = [
            ("view_staff_user", "Can view staff user"),
            ("change_staff_user", "Can change staff user"),
            ("delete_staff_user", "Can delete staff user"),
            ("add_staff_user", "Can add staff user"),
            ("view_settings_user", "Can view settings"),
            ("view_advanced_homepage_user", "Can view advanced homepage"),
        ]

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
        return self.groups.filter(name="admin").exists()
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
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        permissions = [
            ("view_updatedb_product", "Can update database"),
        ]
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


#class Image(models.Model):
#    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
#    url = models.CharField(max_length=256)
#auditlog.register(Image)


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


class PriceType(models.Model):
    name = models.CharField(max_length = 128)
    active= models.BooleanField(default=True)
auditlog.register(PriceType)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True)
    status = models.CharField(max_length=16,choices= [
        ('preparado', 'Preparado'),
        ('pendiente', 'Pendiente')
    ])
    exchange_rate = models.ForeignKey(ExchangeRate, on_delete=models.DO_NOTHING, null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='orders', null=True)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    pricetype = models.ForeignKey(PriceType, blank=True, null=True, on_delete=models.DO_NOTHING)
    active = models.BooleanField(null = False, default=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        permissions = [
            ("view_own_order", "Can view its own order"),
            ("change_status_order", "Can change order status"),
            ("view_export_order", "Can export order"),
        ]
    def product_categories(self):
        return Order_Product.objects.filter(order_id=self.id).count()

    def __str__(self):
        return str(self.id)
auditlog.register(Order)


class Order_Product(models.Model):
    order =  models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    price = models.DecimalField(max_digits=7,decimal_places=2, default=0)
    cost = models.DecimalField(max_digits=7,decimal_places=2, default=0)
    quantity = models.IntegerField(validators = [
        MinValueValidator(1)
    ])
    active = models.BooleanField(default=True, blank=False, null=False)
    def __str__(self):
        return str(self.id)
auditlog.register(Order_Product)


class Note(models.Model):
    id = models.AutoField(primary_key=True)
    note = models.TextField()
    name = models.CharField(max_length=128)
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True, blank=False, null=False)
auditlog.register(Note)


#class PasswordResetToken(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
#    token = models.CharField(max_length=256)
#    date = models.DateTimeField(auto_now_add=True)
#    active = models.BooleanField(default=True)

# class Receivable(models.Model):
#     active = models.BooleanField(default=False)
#     seller = models.CharField(max_length=128, blank=True, null=True)
#     client = models.CharField(max_length=128, blank=True, null=True)
#     total = models.DecimalField(max_digits=7, decimal_places=2)
#     date = models.DateField(auto_now_add=False)
#     number = models.CharField(max_length=128, blank=True, null=True)
# auditlog.register(Receivable)
#
