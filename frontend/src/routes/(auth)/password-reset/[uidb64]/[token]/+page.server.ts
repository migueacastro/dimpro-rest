import { apiURL } from '$lib/api_url';
import { fail, redirect, type Actions } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, fetch }) => {
	const token = params.token;
	const uidb64 = params.uidb64;
	const response = await fetch(apiURL + 'password-reset/' + uidb64 + '/' + token);

	if (!response.ok) {
		return redirect(302, '/start');
	}
};

export const actions: Actions = {
	changepassword: async ({ request, fetch, params }) => {
		const formData = await request.formData();
		const password = formData.get('password');
		const token = params.token;
		const uidb64 = params.uidb64;
		const respones = await fetch(apiURL + 'password-reset-complete', {
			method: 'PATCH',
			body: JSON.stringify({
				password: password,
				token: token,
				uidb64: uidb64
			})
		});

		if (respones.ok) {
			return {
				success: true,
				message: 'Password changed successfully.'
			};
		} else {
			console.log('Error: ', await respones.text());
			return fail(400, {
				error: 'Failed to change password. Please try again.'
			});
		}
	}
};
