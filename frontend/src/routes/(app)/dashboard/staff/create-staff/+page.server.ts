import { apiURL } from '$lib/api_url.js';
import { redirect, type Actions } from '@sveltejs/kit';

export async function load({ locals }) {
    if (!locals.user) {
        return redirect(303, '/start');
    }
    return {
        user: locals.user
    };
}

export const actions: Actions = {
    add: async ({ request, fetch }) => {
        const formData = await request.formData();
        formData.delete("endpoint");
        formData.set("groups","[2,3]");
        const keys = Array.from(formData.keys());
        const values = Array.from(formData.values());
        let body: any = {};
        for (let i = 0; i < keys.length; i++) {
            try {
                body[keys[i]] = JSON.parse(values[i] as string);
            } catch {
                body[keys[i]] = values[i];
            }
        }
        let response = await fetch(apiURL + "users/", {
            method: 'POST',
            body: JSON.stringify(body)
        });
        return {
            success: response.ok,
            error:response.statusText
        }
    }
}