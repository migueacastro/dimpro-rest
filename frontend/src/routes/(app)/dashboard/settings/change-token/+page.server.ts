import { apiURL } from '$lib/api_url';
import { redirect } from '@sveltejs/kit';

export async function load({ cookies, fetch }: any) {
	if (cookies.get('password')) {
		const response = await fetch(apiURL + 'alegratoken');
		const alegratoken = await response.json();
		const password = cookies.get('password');
		cookies.delete('password', { path: '/' });
		cookies.delete('redirectTo', { path: '/' });
		return {
			alegratoken,
			password
		};
	} else {
		cookies.set('redirectTo', '/dashboard/settings/change-token', {
			path: '/',
			httpOnly: true,
			sameSite: 'lax',
			secure: import.meta.env.VITE_API_URL === 'production'
		});
		return redirect(303, '/dashboard/user/verify-password');
	}
}
