import type { Actions } from '@sveltejs/kit';
import { login, fetchRegister } from '$lib/auth';

export const actions: Actions = {
	register: async ({ request, locals, cookies }) => {
		const formData = await request.formData();
        const response = await fetchRegister(formData);
        console.log(formData)
        const data = await response.json();
        console.log(data);
        formData.delete('confirmPassword');
        formData.delete('phonenumber');
        formData.delete('name');
        console.log(formData);
        return login({ cookies, locals, formData, isStaff: false});
	}
};


