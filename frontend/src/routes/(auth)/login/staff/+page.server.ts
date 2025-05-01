import type { Actions } from './$types';
import { login } from '$lib/auth';

export const actions = {
	login: async ({ request, locals, fetch, cookies}) => {
		const formData = await request.formData();
		return await login({ fetch, locals, formData, isStaff: true, cookies});
	}
} satisfies Actions;


