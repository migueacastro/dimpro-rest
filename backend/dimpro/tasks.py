from .models import *
from alegra.client import Client as c
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
import base64


EXCLUDED_PRICETYPE_NAMES = ['EPA']


def encodeduser():
    alegra_user = AlegraUser.objects.get(id=1)
    original_string = f"{alegra_user.email}:{alegra_user.token}"
    encoded_bytes = base64.b64encode(original_string.encode("utf-8"))
    encoded_string = encoded_bytes.decode("utf-8")
    return encoded_string

def updatedb():
    alegra_user = AlegraUser.objects.get(id=1)
    client = c(alegra_user.email, alegra_user.token)

    with transaction.atomic():
        update_products(client)
        update_contacts(client)


def update_products(client):
    items = fetch_all_items(client)
    deactivate_all_products()

    for row in items:
        process_product(row)

def update_contacts(client):
    contacts = fetch_all_contacts(client)
    
    for row in contacts:
        process_contact(row)


def fetch_all_items(client):
    items = []
    i = 0
    while True:
        dictu = client.list_items(start=(30*i), order='ASC')
        if not dictu:
            break
        items.extend(dictu)
        i += 1
    return items


def fetch_all_contacts(client):
    contacts = []
    i = 0
    while True:
        dictu = client.list_contacts(start=(30*i), order='ASC')
        if not dictu:
            break
        contacts.extend(dictu)
        i += 1
    return contacts


def deactivate_all_products():
    Product.objects.all().update(active=False)


def process_product(row):
    id = row['id']
    item = row['name']
    details = row.get('description', '')
    reference = row.get('reference', '')
    prices = extract_prices(row.get('price', []))
    available_quantity = extract_available_quantity(row.get('inventory', {}))

    active = available_quantity > 0 and row['price'][0]['price'] > 0
    if item == 'BOMBILLO LED 12W':
        update_price_types(row['price'])

    update_or_create_product(id, item, details, reference, available_quantity, prices, active)


def extract_prices(price_list):
    return [{price_dict['name']: price_dict['price']} for price_dict in price_list if price_dict['name'] not in EXCLUDED_PRICETYPE_NAMES]
   

def extract_available_quantity(inventory):
    try:
        return inventory['warehouses'][0]['availableQuantity']
    except KeyError:
        return 0


def update_price_types(price_list):
    PriceType.objects.all().update(active=False)
    for price_dict in price_list:
        if price_dict['name'] in EXCLUDED_PRICETYPE_NAMES:
            continue
        name = price_dict['name']
        PriceType.objects.update_or_create(
            name=name,  # Usar 'name' como clave única
            defaults={'active': True}
        )


def update_or_create_product(product_id, item, details, reference, available_quantity, prices, active):
    try:
        product = Product.objects.get(reference=reference)
        product.item = item
        product.details = details
        product.reference = reference
        product.available_quantity = available_quantity
        product.prices = prices
        product.active = active
        product.save()
    except ObjectDoesNotExist:
        Product.objects.update_or_create(
            id=product_id,
            defaults={
                'item': item,
                'details': details,
                'reference': reference,
                'available_quantity': available_quantity,
                'prices': prices,
                'active': active
            }
        )

def process_contact(row):
    name = row['name']
    Contact.objects.update_or_create(name=name, defaults={'active': True})
        



