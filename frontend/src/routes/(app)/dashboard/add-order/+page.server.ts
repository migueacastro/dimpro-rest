import { apiURL } from '$lib/api_url';
import { checkPermission, permissionError } from '$lib/auth';
import { type Actions } from '@sveltejs/kit';

export async function load({ fetch, locals}: any) {
  let response = await fetch(apiURL + 'contacts');
  let contacts = await response.json();
  let contactList = contacts.map((contact: any) => {
    return { label: contact.name, value: contact.id };
  });

  if (!checkPermission(locals.user,"add_order")) {
    return permissionError();
  }

  return {
    contactList
  };
}

export const actions: Actions = {
  create: async ({ request, locals, fetch }) => {
    const formData = await request.formData();
    const contact: any = parseInt(formData.get('contact') as string);
    const user = locals?.user?.id;
    const response = await fetch(apiURL + 'orders' + '/', {
      method: 'POST',
      body: JSON.stringify({
        contact,
        user,
        status: 'pendiente'
      })
    });
    const data = await response.json();
    if (response.ok) {
      return {
        success: true,
        data,
      }
    } else {
      return {
        success: false,
        error: { data }
      };
    }
  }
};
