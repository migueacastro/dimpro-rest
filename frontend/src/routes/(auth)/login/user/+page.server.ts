import type { Actions } from './$types';
import { login } from '$lib/auth';

export const actions: Actions = {
	login: async ({ request, locals, fetch, cookies }) => {
		const formData = await request.formData();
		return login({ fetch, locals, formData, isStaff: false, cookies });
	}
} satisfies Actions;


