from django.contrib import admin
from dimpro.models import *
#
# Register your models here.
class ProductAdmin(admin.ModelAdmin): # Esto es para ver detalladamente la lista
  list_display = ('id', 'item', 'details', 'reference', 'prices', 'available_quantity')
  list_filter = ('active',)
  search_fields = ('item', 'details', 'reference')
  list_per_page = 25 

class UserAdmin(admin.ModelAdmin):
  list_display = ('id', 'email', 'name', 'phonenumber', 'active', 'is_superuser')
  list_filter = ('active', 'is_superuser')
  search_fields = ('email', 'name')
  list_per_page = 25

admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Contact) # Esto es para ver solo los registros por el id, no muestra detalles a simple vista