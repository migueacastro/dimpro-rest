from django.contrib import admin
from dimpro.models import *
from django.contrib.auth.models import Group, ContentType
#
# Register your models here.
class ProductAdmin(admin.ModelAdmin): # Esto es para ver detalladamente la lista
  list_display = ('id', 'item', 'details', 'reference', 'prices', 'available_quantity',)
  list_filter = ('active',)
  search_fields = ('item', 'details', 'reference',)
  list_per_page = 25 

class UserAdmin(admin.ModelAdmin):
  list_display = ('id', 'email', 'name', 'phonenumber', 'active',)
  list_filter = ('active',)
  search_fields = ('email', 'name',)
  list_per_page = 25

admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(Order_Product)
# admin.site.register(LogEntry)
admin.site.register(Contact) # Esto es para ver solo los registros por el id, no muestra detalles a simple vista
admin.site.register(Note)
#admin.site.register(Image)
admin.site.register(PriceType)
#admin.site.register(ExchangeRate)
#admin.site.register(ExchangeCurrency)
admin.site.register(ContentType)