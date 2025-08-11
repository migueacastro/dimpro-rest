import { apiURL } from '$lib/api_url.js';
import { checkPermission, permissionError } from '$lib/auth.js';
import { redirect, type Actions } from '@sveltejs/kit';

export async function load({ locals, fetch }) {
	if (!checkPermission(locals.user, 'add_contactaddrequest')) {
		return permissionError();
	}
}

export const actions: Actions = {
	add: async ({ request, fetch }) => {
		const formData = await request.formData();
		let response = await fetch(apiURL + 'contact_add_requests/', {
			method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
			body: JSON.stringify(Object.fromEntries(formData))
		});
    let data: any;  
		data = await response.json()
		return {
			success: response.ok,
			error: data.error
		};
	}
};
