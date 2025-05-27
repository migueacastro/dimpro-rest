import { apiURL } from '$lib/api_url.js';
import { checkStaffGroup } from '$lib/auth';
import { redirect, type Actions } from '@sveltejs/kit';

export async function load({ fetch, locals }: any) {
    if (!locals.user) {
        return redirect(303, '/start');
    }
    return {
        user: locals.user
    };
    
}

export const actions: Actions = {
    edit: async ({ request, fetch, locals, cookies }) => {
        const formData = await request.formData();
        const id = formData.get("id");
        let endpoint = "";
        if (checkStaffGroup(locals.user)) {
            endpoint = "staff";
        } else {
            endpoint = "users";
        }
        formData.delete("endpoint");
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

        let response = await fetch(apiURL + endpoint + `/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify(body)
        });
        return {
            success: response.ok,
            error: response.statusText
        }
    }
}