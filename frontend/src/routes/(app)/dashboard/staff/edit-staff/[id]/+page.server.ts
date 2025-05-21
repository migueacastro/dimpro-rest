import { apiURL } from '$lib/api_url.js';
import { checkPermission, permissionError } from '$lib/auth';
import { redirect, type Actions } from '@sveltejs/kit';

export async function load({ fetch, locals, params }: any) {
    const response = await fetch(apiURL + `staff/${params.id}`);
    const data = await response.json();
    if (!checkPermission(locals.user, "change_staff_user")) {
        return permissionError();
    }

    return {
        user: locals.user,
        reqUser: data
    };
}

export const actions: Actions = {
    edit: async ({ request, fetch }) => {
        const formData = await request.formData();
        const id = formData.get("id");
        const endpoint = formData.get("endpoint");
        formData.delete("endpoint");
        const keys = Array.from(formData.keys());
        const values = Array.from(formData.values());
        let body: any = {};
        for (let i = 0; i < keys.length; i++) {
            if (values[i].toString().trim() !== "") {
                try {
                    body[keys[i]] = JSON.parse(values[i] as string);
                } catch {
                    body[keys[i]] = values[i];
                }
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