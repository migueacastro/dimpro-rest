import type { Actions } from '@sveltejs/kit';

export const actions: Actions = {
	changepassword: async ({ request, fetch }) => {
		const formaData = await request.formData();
		const oldPassword = formaData.get('oldPassword');
		const password = formaData.get('password');
		const confirmPassword = formaData.get('confirmPassword');
		const response = await fetch('/api/user/change_password', {
			method: 'POST',
			body: JSON.stringify({
				password: oldPassword,
				newPassword: password,
				confirmPassword: confirmPassword
			})
		});
    if (response.ok) {
      return { success: true };
    }
    const data = await response.json();
      return { error: data, succcess: false };

	}
};
