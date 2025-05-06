import { apiURL } from '$lib/api_url';
import { checkStaffGroup, login } from '$lib/auth';
import { fail, type Actions } from '@sveltejs/kit';

export const actions: Actions = {
	changepassword: async ({ request, fetch, locals, cookies }) => {
		const formData = await request.formData();
		const user: any = locals.user;
		const userFormData: FormData = new FormData();
		userFormData.append('email', user?.email);
		userFormData.append('password', formData.get('password') || '');
		const isStaff = checkStaffGroup(user);
		const response = await fetch(apiURL + 'user/change_password', {
			method: 'POST',
			body: JSON.stringify(Object.fromEntries(formData))
		});
		if (response.ok) {
			return login({
				fetch,
				locals,
				formData: userFormData,
				isStaff,
				cookies,
			});
		}
		console.log(await response.text())
		return fail(400, {
			error: 'Error al cambiar la contraseña',
			success: false
		});
	}
};
