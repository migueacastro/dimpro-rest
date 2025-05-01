import { apiURL } from "$lib/api_url";
import type { Actions, RequestEvent } from "@sveltejs/kit";
import { handleDelete } from "$lib/components/Datatable";
import { checkStaffGroup } from "$lib/auth";



export const load = async ({ fetch, locals }: RequestEvent) => {
  const endpoint = checkStaffGroup(locals.user) ? "orders" : "user_orders";
  const response = await fetch(apiURL + endpoint);
  const list = await response.json();

  return {
    list,
    endpoint,
  };
};

export const actions: Actions = {
  delete: async ({ fetch, request }: RequestEvent) => {
    const formData = await request.formData();
    const id = formData.get("id");
    const result = await handleDelete({ fetch }, `orders/${id}`);
    return result; // Return the result of the delete operation
  },
};