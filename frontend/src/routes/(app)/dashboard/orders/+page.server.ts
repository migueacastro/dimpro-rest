import { apiURL } from '$lib/api_url';
import type { Actions, RequestEvent } from '@sveltejs/kit';
import { handleDelete } from '$lib/components/Datatable';
import { checkPermission, checkStaffGroup, permissionError } from '$lib/auth';

export const load = async ({ fetch, locals }: RequestEvent) => {
	let endpoint: string;
	let response: any;
	let list_all: any = [];
	let list_user: any = [];
	if (checkPermission(locals.user, 'view_order')) {
		endpoint = 'orders';
		response = await fetch(apiURL + endpoint);
		list_all = await response.json();
	}
	if (checkPermission(locals.user, 'view_own_order')) {
		endpoint = 'user_orders';
		response = await fetch(apiURL + endpoint);
		list_user = await response.json();
	} else {
		return permissionError();
	}
	
	return {
		list_all,
		list_user
	};
};

export const actions: Actions = {
	delete: async ({ fetch, request }: RequestEvent) => {
		const formData = await request.formData();
		const id = formData.get('id');
		const result = await handleDelete({ fetch }, `orders/${id}`);
		return result; // Return the result of the delete operation
	}
};
