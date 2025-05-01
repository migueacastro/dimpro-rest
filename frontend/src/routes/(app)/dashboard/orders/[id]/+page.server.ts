import { apiURL } from "$lib/api_url.js";
import { changestatus } from "$lib/components/StatusButton.js";
import type { Actions } from "@sveltejs/kit";

export async function load({ params, fetch }) {
  const response = await fetch(apiURL + "orders/" + params.id);
  const order = await response.json();
  console.log(order);
  return {
    id: params.id,
    order,
  };
}

export const actions: Actions = {
  changestatus: changestatus,
};