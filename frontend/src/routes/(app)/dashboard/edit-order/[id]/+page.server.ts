import { browser } from "$app/environment";
import { apiURL } from "$lib/api_url";
import { changestatus } from "$lib/components/StatusButton";
import type { Actions } from "@sveltejs/kit";

export async function load({ params, fetch }: any) {

  let response = await fetch(apiURL + 'products');
  let products = await response.json();
  response = await fetch(apiURL + 'orders/' + params.id);
  let order = await response.json();
  response = await fetch(apiURL + 'orders')
  let orders = await response.json();
  response = await fetch(apiURL + 'contacts');
  let contacts = await response.json();
  response = await fetch(apiURL + 'pricetypes');
  let pricetypes = await response.json();

  let items = order.products.map((product: any, index: any) => {
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
  }) ?? [];



  let selectedPricetypeId = order?.pricetype?.id ?? pricetypes[0]?.id;
  let productAutoCompleteList = products.map((product: any) => {
    return { label: product.item, value: product.id };
  });
  let contactAutoCompleteList = contacts.map((contact: any) => {
    return { label: contact.name, value: contact.id };
  });
  let inputContact = contacts.find((contact: any) => contact.id == order?.contact)?.name;

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
    items,
  };
}

export const actions: Actions = {
  changestatus,
};

