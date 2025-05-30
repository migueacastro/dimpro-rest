import { apiURL } from '$lib/api_url';
import { checkStaffGroup, login } from '$lib/auth';
import { fail, redirect, type Actions } from '@sveltejs/kit';

export async function load({ cookies }: any) {
	if (cookies.get('password')) {
		const oldPassword = cookies.get('password');
		cookies.delete('password', { path: '/' });
		cookies.delete('redirectTo', { path: '/' });
		return {
			oldPassword
		};
	} else {
		cookies.set('redirectTo', '/dashboard/user/change-password', {
			path: '/',
			httpOnly: true,
			sameSite: 'lax',
			secure: import.meta.env.VITE_API_URL === 'production'
		});
		return redirect(303, '/dashboard/user/verify-password');
	}
}

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
				cookies
			});
		}
		return fail(400, {
			error: 'Error al cambiar la contraseña',
			success: false
		});
	}
};
