import { apiURL } from '$lib/api_url';
import type { Actions, RequestEvent } from '@sveltejs/kit';
import { handleDelete } from '$lib/components/Datatable';
import { checkPermission, permissionError } from '$lib/auth';

export const load = async ({ fetch, locals }: RequestEvent) => {
  let endpoint: string;
  let response: any;
  let list_all: any = [];
  if (checkPermission(locals.user, 'view_contactaddrequest')) {
    endpoint = 'contact_add_requests';
    response = await fetch(apiURL + endpoint);
    list_all = await response.json();
  } else {
    return permissionError();
  }
  
  return {
    list_all,
  };
};

export const actions: Actions = {
  delete: async ({ fetch, request }: RequestEvent) => {
    const formData = await request.formData();
    const id = formData.get('id');
    const result = await handleDelete({ fetch }, `contact-add-request/${id}`);
    return result; // Return the result of the delete operation
  }
};
