import type { Actions } from './$types';
import { login } from '$lib/auth';

export const actions: Actions = {
	login: async ({ request, locals, cookies }) => {
		const formData = await request.formData();
		return login({ cookies, locals, formData, isStaff: false });
	}
} satisfies Actions;


