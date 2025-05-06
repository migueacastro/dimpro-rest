import { apiURL } from "$lib/api_url.js";

export async function load({ params, fetch }) {
  const response = await fetch(apiURL + "orders/" + params.id);
  const order = await response.json();
  return {
    id: params.id,
    order,
  };
}

