import type { Actions } from '@sveltejs/kit';
import { login, fetchRegister } from '$lib/auth';
import { apiURL } from '$lib/api_url';
import { fail, redirect } from '@sveltejs/kit';

export const load = async () => {
    return redirect(303, '/');
}

export const actions: Actions = {
	register: async ({ request, locals, fetch, cookies }) => {
		const formData = await request.formData();
        const response = await fetch(apiURL + "register", {
            method: 'POST',
            body: JSON.stringify(Object.fromEntries(formData)),
        });
        if (!response.ok) {
            const data = await response.json();
            console.log(data);
            return fail(400, {
                error: data,
                success: false
            });
        }
        console.log(await response.text());

        formData.delete('confirmPassword');
        formData.delete('phonenumber');
        formData.delete('name');
        return login({ cookies, locals, formData, isStaff: false, fetch});
	}
};


