from .models import *
from alegra.client import Client as c
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
import base64

def encodeduser():
    alegra_user = AlegraUser.objects.get(id=1)
    original_string = f"{alegra_user.email}:{alegra_user.token}"
    encoded_bytes = base64.b64encode(original_string.encode("utf-8"))
    encoded_string = encoded_bytes.decode("utf-8")
    return encoded_string

def updatedb():
    # TODO: Adapt updatedb here

    def add_contact(name):
        instance, created = Contact.objects.get_or_create(name=name)
        return instance
    def add_data(product_id, item, details, reference, available_quantity, prices):
        instance, created = Product.objects.get_or_create(id=product_id, item=item, details=details, reference=reference, available_quantity=available_quantity, prices=prices)
        return instance

    alegra_user = AlegraUser.objects.get(id=1)
    client = c(alegra_user.email, alegra_user.token)

    items = []

    i = 0
    while (True):
        
        dictu = client.list_items(start=(30 * i), order="ASC")
        if not dictu:
            break
        items = items + dictu
        i += 1
    
    productsArray = Product.objects.all()
    for item in productsArray:
        item.active = False
        item.save()

    for row in items:
        id = row['id']
        item = row['name']
        details = row['description']
        reference = row['reference']
        
        prices = []
        for price_dict in row['price']:
            if price_dict['name'] != 'EPA':
                prices.append({price_dict['name']: price_dict['price']})
        try:
            available_quantity = row['inventory']
            available_quantity = available_quantity['warehouses'][0]
            available_quantity = available_quantity['availableQuantity']
        except KeyError:
            available_quantity = 0
        
        
        active = False if available_quantity == 0 or row['price'][0]['price'] == 0 else True
        
        
        # Add the current prices of Alegra
        if row['name'] == 'BOMBILLO LED 12W':
            # Delete all prices
            PriceType.objects.all().delete()
            for i in range(len(row["price"])):
                # Check if the price is from EPA
                if row['price'][i]['name'] == 'EPA':
                    continue

                name = row['price'][i]['name']
                PriceType.objects.create(id=i, name=name)
        
        try:
            selecteditem = Product.objects.get(reference=reference)
            selecteditem.item = item
            
            try:
                selecteditem.details = details
            except Product.IntegrityError as e:
                continue
        
            selecteditem.reference = reference
            selecteditem.available_quantity = available_quantity
            selecteditem.prices = prices
            selecteditem.active = active
            selecteditem.save()
        except ObjectDoesNotExist:
            try:
                add_data(id, item, details, reference, available_quantity, prices)
                
            except IntegrityError as e:
                continue

    contacts = []
    
    i = 0
    while (True):
        
        dictu = client.list_contacts(start=(30 * i), order="ASC")
        if not dictu:
            break
        contacts = contacts + dictu
        i += 1
    
    for row in contacts:
        name = row['name']

        # Check if contact is in alegra db
        list_contacts = Contact.objects.all()
        for contact in list_contacts:
            if not contact in row:
                row['active'] = False
            row['active'] = False

        try:
            selectedcontact = Contact.objects.get(name=name)
        except ObjectDoesNotExist:
            try:
                add_contact(name) 
            except Exception as e:
                continue
