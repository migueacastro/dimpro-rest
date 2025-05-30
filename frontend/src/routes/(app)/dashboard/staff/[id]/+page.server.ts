import { apiURL } from '$lib/api_url.js';
import { checkPermission, permissionError } from '$lib/auth.js';
import { redirect } from '@sveltejs/kit';

export async function load({ locals, fetch, params }) {
	let response = await fetch(apiURL + 'staff/' + params.id);
	if (!checkPermission(locals.user, 'view_staff_user')) {
		return permissionError();
	}
	let reqUser = await response.json();
	return {
		reqUser: reqUser
	};
}
