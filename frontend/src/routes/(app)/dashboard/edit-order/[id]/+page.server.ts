import { browser } from '$app/environment';
import { apiURL } from '$lib/api_url';
import { checkPermission, permissionError } from '$lib/auth';
import { changestatus } from '$lib/components/StatusButton';
import { getCurrentDateTime } from '$lib/datetime';
import type { Actions } from '@sveltejs/kit';

export async function load({ params, fetch, locals }: any) {

  if (!checkPermission(locals.user, 'change_order')) {
    return permissionError();
  }

  let response = await fetch(apiURL + 'products');
  let products = await response.json();
  response = await fetch(apiURL + 'orders/' + params.id);
  let order = await response.json();
  response = await fetch(apiURL + 'orders');
  let orders = await response.json();
  response = await fetch(apiURL + 'contacts');
  let contacts = await response.json();
  response = await fetch(apiURL + 'pricetypes');
  let pricetypes = await response.json();

  response = await fetch(apiURL + 'notes');
  let reminders = await response.json();

  let items =
    (order?.products?.length > 0) ? Array.from(order.products).map((product: any, index: any) => {
      const row = {
        id: product.product.id,
        item: product.product.id,
        reference: product.product.reference,
        quantity: product.quantity,
        availability: product.product.available_quantity,
        price: product.price,
        cost: product.cost,
        item_label: product.product.item,
        index: index,
        search_error: false,
        input_disabled: true,
        hover: false,
        product_object: null
      };
      return row;
    }) : [];
  let selectedPricetypeId = order?.pricetype?.id ?? pricetypes[0]?.id;
  let selectedContactId = order?.contact;
  let productAutoCompleteList = products.map((product: any) => {
    return { label: product.item, value: product.id };
  });
  let contactAutoCompleteList = contacts.map((contact: any) => {
    return { label: contact.name, value: contact.id };
  });
  let inputContact = order?.contact_name

  if (browser) {
    if (!order) {
      window.history.back();
    }
  }

  return {
    id: params.id,
    products,
    order,
    orders,
    contacts,
    pricetypes,
    inputContact,
    contactAutoCompleteList,
    selectedPricetypeId,
    productAutoCompleteList,
    selectedContactId,
    items,
    reminders
  };
}

export const actions: Actions = {
  changestatus,
  save: async ({ request, fetch }) => {
    const formData = await request.formData();
    let order: any = JSON.parse(formData.get('order') as string);
    order.pricetype = formData.get('pricetype');
    order.contact = formData.get('contact');
    order.user = order.user.id;
    order.total = formData.get('total');

    let items: Array<any> = JSON.parse(formData.get('items') as string);

    await disableInitialItems(order, fetch);
    let response;
    for (const row of items) {
      response = await fetch(apiURL + 'order_products/', {
        method: 'POST',
        body: JSON.stringify({
          order: order.id,
          product: row.item,
          price: row.price,
          quantity: row.quantity,
          cost: row.cost,
          active: true
        })
      });
      if (!response.ok) {
        console.log(response.text())
      }
    }

    response = await fetch(apiURL + 'orders/' + order.id + '/', {
      method: 'PATCH',
      body: JSON.stringify(order)
    });
    if (response.ok) {
      const data = await response.json();
      return {
        success: true,
        data: data
      };
    } else {

      console.log(await response.text());
      return {
        success: false,

      };
    }
  },
  delete: async ({ request, fetch }) => {
    const formData = await request.formData();
    const id = formData.get('id');
    const response = await fetch(apiURL + 'orders/' + id + '/', {
      method: 'DELETE'
    });
    if (response.ok) {
      return {
        success: true
      };
    } else {
      const data = await response.json();
      console.log(data);
      return {
        success: false,
        error: { data }
      };
    }
  },
  addReminder: async ({ request, fetch, locals }) => {
    let formData = await request.formData();
    let body = { note: formData.get('note'), name: locals.user?.name };
    let response = await fetch(apiURL + "notes/", {
      method: "POST",
      body: JSON.stringify(body)
    });
    const data = await response.json();
    response = await fetch(apiURL+"notes");
    const reminders = await response.json();
    return {
      success: response.ok,
      action: "agreg",
      error: { data },
      reminders,
    };
  },
  deleteReminder: async ({ request, fetch }) => {
    let formData = await request.formData();
    const id = formData.get('id');
    let response = await fetch(apiURL + 'notes/' + id + '/', {
      method: 'DELETE'
    });
    if (response.ok) {
      response = await fetch(apiURL+"notes");
      const reminders = await response.json();
      return {
        success: true,
        action: "elimin",
        reminders
      };
    } else {
      const data = await response.json();
      return {
        success: false,
        action: "elimin",
        error: { data }
      };
    }
  },
  editReminder: async ({ request, fetch }) => {
    const formData = await request.formData();
    const id = formData.get("id");
    const name = formData.get("name");
    const note = formData.get("note");
    let body: any = { note: note, name: name, date: getCurrentDateTime() };
    let response = await fetch(apiURL + "notes" + `/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(body)
    });
    let fetchResponse = await fetch(apiURL+"notes");
    const reminders = await fetchResponse.json();
    return {
      success: response.ok,
      error: response.statusText,
      action: "actualiz",
      reminders,
    }

  }
};

async function disableInitialItems(orderObject: any, fetch: any) {
  let data: any;
  let response: any;
  for (const product of orderObject.products) {
    response = await fetch(apiURL + 'order_products/' + product.id + '/', {
      method: 'PATCH',
      body: JSON.stringify({
        active: false
      })
    });
    if (!response.ok) {
      data = await response.json();
      console.log(data);
    }
  }
}
