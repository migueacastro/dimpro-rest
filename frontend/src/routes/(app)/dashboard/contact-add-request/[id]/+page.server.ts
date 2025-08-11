import { apiURL } from '$lib/api_url.js';
import { checkPermission, permissionError } from '$lib/auth.js';
import { approve } from '$lib/components/RequestStatusButton.js';
import RequestStatusButton from '$lib/components/RequestStatusButton.svelte';
import { redirect, type Actions } from '@sveltejs/kit';


export async function load({ locals, fetch, params }) {
	if (!checkPermission(locals.user, 'change_contactaddrequest')) {
		return permissionError();
	}

	let response: any;
	let users: any = [];
	if (checkPermission(locals.user, 'view_user')) {
		// Fetch the list of users if the user has permission to view them
		response = await fetch(apiURL + 'users');
		users = await response .json();
	}
	let staff: any = [];
	if (checkPermission(locals.user, 'view_staff_user')) {
		response = await fetch(apiURL + 'staff');
		staff = await response.json();
	}

	

  users = [...users,...staff];

  users.sort((a: any, b: any) => a.name.localeCompare(b.name)); 
	response = await fetch(apiURL + 'users');



	let endpoint = `contact_add_requests/${params.id}`;
	response = await fetch(apiURL + endpoint);
	let request = await response.json();
	response = await fetch(apiURL+'users/'+request.user);
	let request_user = await response.json();
	if (!users.find((user: any) => user.id === request.user)) {
		users.push(request_user);
	}
	users = users.map((user: any) => {
		return {
			label: user.name,
			value: user.id,
		}
	});
	return {
		request,
		users,
	}

}

export const actions: Actions = {
	edit: async ({ request, fetch, params }) => {
		const formData = await request.formData();
		let response = await fetch(apiURL + 'contact_add_requests/'+params.id+'/', {
			method: 'PATCH',
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
	},
	approve,
	delete: async ({ request, fetch, params }) => {
    const id =  params.id;
    const response = await fetch(apiURL + 'contact_add_requests/' + id + '/', {
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
};
