import { redirect } from '@sveltejs/kit';
import { apiURL } from '$lib/api_url';
import type { Actions, RequestEvent } from '@sveltejs/kit';
import { checkStaffGroup } from '$lib/auth';

const endpoint = 'orders';

export const load = async ({ fetch, locals }: RequestEvent) => {
	if (checkStaffGroup(locals.user)) {
		const response = await fetch(apiURL + endpoint);
		const list = await response.json();

		return {
			// not this one
			list,
			endpoint
		};
	}

};
