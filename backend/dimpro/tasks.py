from .models import *
from alegra.client import Client as c
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, connection
from auditlog.models import LogEntry
from django.utils import timezone
from datetime import timedelta
import base64
from django.db import OperationalError
import pprint
import time
import requests


EXCLUDED_PRICETYPE_NAMES = ["EPA"]
ENDPOINT = "https://api.alegra.com/api/v1/"

def encodeduser():
    alegra_user = AlegraUser.objects.get(id=1)
    original_string = f"{alegra_user.email}:{alegra_user.token}"
    encoded_bytes = base64.b64encode(original_string.encode("utf-8"))
    encoded_string = encoded_bytes.decode("utf-8")
    return encoded_string

def remove_six_months_logs():
    time_ago = timezone.now() - timedelta(days=30*6)
    deleted_count, _ = LogEntry.objects.filter(timestamp__lt=time_ago).delete()
    print("Removed entries from more than a month ago")

def updatedb():
    client = {'accept': 'application/json', 'authorization': f'Basic {encodeduser()}'}

    update_products_atomic(client)
    update_contacts_atomic(client)
    update_invoices_atomic(client)

def update_products_atomic(client):
    items = fetch_all_items(client)  # Fetch outside transaction
    with transaction.atomic():
        # Only DB operations here
        deactivate_all_products()

        # Collect product data for each item
        product_data_list = []
        for row in items:
            data = extract_product_data(row)
            product_data_list.append(data)

        # Bulk update/create products
        bulk_update_or_create_products(product_data_list)
    
def update_invoices_atomic(client):
    items = fetch_all_invoices(client)
    
    with transaction.atomic():
        invoice_data_list = []
        for row in items:
            data = extract_invoice_data(row)
            invoice_data_list.append(data)
        bulk_create_invoices(invoice_data_list)


def extract_invoice_data(row):
    id = row.get("id", "")
    seller_name = row["seller"]["name"] if row["seller"] else ""
    date = row.get("date", "")
    total = row.get("total", 0)

    return {
        "id": id,
        "seller_name": seller_name,
        "date": date,
        "total": total,
        "active": True,
    }


def bulk_create_invoices(invoice_data_list):
    to_create = []
    for data in invoice_data_list:
        new_invoice = Invoice(
            id=data["id"],  # Optional, if id is provided
            seller_name=data["seller_name"] if "seller_name" in data else "",
            date=data["date"],
            total=data["total"],
            active=data["active"],
        )
        to_create.append(new_invoice)

    if to_create:
        Invoice.objects.bulk_create(to_create)
    

def update_contacts_atomic(client):
    with transaction.atomic():
        update_contacts(client)

def update_products(client):
    items = fetch_all_items(client)
    # Mark all products as inactive first if needed
    deactivate_all_products()

    # Collect product data for each item
    product_data_list = []
    for row in items:
        data = extract_product_data(row)
        product_data_list.append(data)

    # Bulk update/create products
    bulk_update_or_create_products(product_data_list)


def extract_product_data(row):
    """
    Extract structured product data from a row.
    """
    product_id = row.get("id", "")
    item = row.get("name", "")
    details = row.get("description", "")
    reference = row.get("reference", "")
    prices = extract_prices(row.get("price", []))
    available_quantity = extract_available_quantity(row.get("inventory", {}))
    try:
        active = available_quantity > 0 and row["price"][0]["price"] > 0
    except Exception:
        active = False

    # You can also update price types if needed:
    if item == "BOMBILLO LED 12W":
        update_price_types(row["price"]) if row.get("price") else None

    return {
        "id": product_id,
        "item": item,
        "details": details,
        "reference": reference,
        "available_quantity": available_quantity,
        "prices": prices,
        "active": active,
    }


def bulk_update_or_create_products(product_data_list):
    # Get the list of references for incoming products
    list_ids = [data["id"] for data in product_data_list]

    # Query existing products that match any of those references
    existing_products = Product.objects.filter(id__in=list_ids)
    existing_products_list = [prod.id for prod in existing_products]
    existing_products_map = {prod.id: prod for prod in existing_products}

    to_create = []
    to_update = []

    for data in product_data_list:

        # Check if product with the same reference already exists
        if int(data["id"]) in existing_products_list:
            prod = existing_products_map[int(data["id"])]
            prod.item = data["item"]
            prod.details = data["details"]
            prod.available_quantity = data["available_quantity"]
            prod.prices = data["prices"]
            prod.active = data["active"]
            to_update.append(prod)
        else:
            new_prod = Product(
                id=data["id"],  # Optional, if id is provided
                item=data["item"],
                details=data["details"],
                reference=data["reference"],
                available_quantity=data["available_quantity"],
                prices=data["prices"],
                active=data["active"],
            )
            to_create.append(new_prod)

    if to_create:
        Product.objects.bulk_create(to_create)
    if to_update:
        # Specify the fields you want to update
        Product.objects.bulk_update(
            to_update,
            fields=["item", "details", "available_quantity", "prices", "active"],
        )


def update_contacts(client):
    contacts = fetch_all_contacts(client)

    for row in contacts:
        process_contact(row)


def fetch_all_items(client):
    items = []
    i = 0
    while True:
        try:
            response = requests.get(
                url=ENDPOINT + f"items?start={str(30*i)}&order_direction=ASC",
                headers=client
            )
            
            # Handle rate limiting (429)
            if response.status_code == 429:
                time_remaining = int(response.headers.get("x-rate-limit-reset", 10))
                print(f"Rate limit exceeded. Waiting for {time_remaining} seconds.")
                time.sleep(time_remaining)
                continue  # Retry the same request
                
            # Handle other errors
            if response.status_code != 200:
                print(f"Error fetching items: {response.status_code} - {response.text}")
                break
                
            # Process successful response
            data = response.json()
            if not data:
                break  # No more items
                
            items.extend(data)
            i += 1
            
        except Exception as e:
            print(f"Request failed: {str(e)}")
            break
            
    return items


def fetch_all_contacts(client):
    contacts = []
    i = 0
    while True:
        response = requests.get(url=ENDPOINT+f"contacts?start={str(30*i)}&order_direction=ASC", headers=client)
        if response.status_code != 200:
                response = response.json()
                response_headers = response.get("headers", {})
                response_code = int(response.get("code", 500))
                if response_code == 429:
                    time_remaining = response_headers.get("x-rate-limit-reset", 0)
                    print(f"Rate limit exceeded. Waiting for {time_remaining} seconds.")
                    time.sleep(time_remaining)
                print(f"Error fetching items: {str(response.get('code', 'No code'))} - {response.get('message', 'No message provided')}")
        else:
            dictu = response.json()
            if not dictu:
                break
            contacts.extend(dictu) if dictu and response.status_code == 200 else None
            i += 1
        
    return contacts

def fetch_all_invoices(client):
    start_id = Invoice.objects.order_by('id').last().id if Invoice.objects.exists() else 1
    invoices = []
    i = 0
    while True:
        response = requests.get(url=ENDPOINT+f"invoices?start={str(start_id + 30*i)}&order_direction=ASC", headers=client)
        if response.status_code != 200:
            response = response.json()
            response_headers = response.get("headers", {})
            response_code = int(response.get("code", 500))
            if response_code == 429:
                time_remaining = response_headers.get("x-rate-limit-reset", 0)
                print(f"Rate limit exceeded. Waiting for {time_remaining} seconds.")
                time.sleep(time_remaining)
            print(f"Error fetching invoices: {str(response.get('code', 'No code'))} - {response.get('message', 'No message provided')}")
        else:
            dictu = response.json()
            if not dictu:
                break
            invoices.extend(dictu) if dictu and response.status_code == 200 else None
            i += 1
    return invoices



def deactivate_all_products():
    with connection.cursor() as cursor:
        cursor.execute("UPDATE dimpro_product SET active = false")


def extract_prices(price_list):
    return [
        {price_dict["name"]: price_dict["price"]}
        for price_dict in price_list
        if price_dict["name"] not in EXCLUDED_PRICETYPE_NAMES
    ]


def extract_available_quantity(inventory):
    try:
        return inventory["warehouses"][0]["availableQuantity"]
    except KeyError:
        return 0


def update_price_types(price_list):
    PriceType.objects.all().update(active=False)
    for price_dict in price_list:
        if price_dict["name"] in EXCLUDED_PRICETYPE_NAMES:
            continue
        name = price_dict["name"]
        PriceType.objects.update_or_create(
            name=name, defaults={"active": True}  # Usar 'name' como clave única
        )


def process_contact(row):
    try:
        contact_id = row.get("id", "")
        name = row["name"]
        Contact.objects.update_or_create(
            id=contact_id, defaults={"name": name, "active": True}
        )
    except Exception as e:
        print("KeyError processing contact row:")
        pprint.pprint(row)
        print(f"Error: {e}")


def safe_update_products(client, retries=3):
    for attempt in range(retries):
        try:
            update_products_atomic(client)
            break
        except OperationalError as e:
            if 'deadlock' in str(e).lower() and attempt < retries - 1:
                time.sleep(1)
                continue
            raise
