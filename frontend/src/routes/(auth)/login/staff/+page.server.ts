import type { Actions } from './$types';
import { login } from '$lib/auth';

export const actions = {
	login: async ({ request, locals, cookies }) => {
		const formData = await request.formData();
		return await login({ cookies, locals, formData, isStaff: true });
	}
} satisfies Actions;


