import { apiURL } from '$lib/api_url';
import { fail, type Actions } from '@sveltejs/kit';


export const actions: Actions = {
	send: async ({ request, locals, fetch, params }) => {
		const formData = await request.formData();
    const token = params.token ??'';
    formData.set('token', token);
		const response = await fetch(apiURL + 'request-reset-email', {
			method: 'POST',
			body: JSON.stringify(Object.fromEntries(formData))
		});
		if (response.ok) {
      console.log('Password reset email sent successfully.');
			return {
				success: true,
				message: 'Password reset email sent successfully.'
			};
		} else {
			console.log('Error: ', await response.text());
			return fail(400, {
				success: false,
				error: 'Failed to send password reset email. Please try again.'
			});
		}
	}
};
