import { apiURL } from '$lib/api_url.js';
import { redirect, type Actions } from '@sveltejs/kit';

export async function load({ fetch,locals,params }:any) {
    const response = await fetch(apiURL + `staff/${params.id}`);
    const data = await response.json();
    if (!locals.user) {
        return redirect(303, '/start');
    }
    return {
        user: locals.user,
        reqUser:data
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
            error:response.statusText
        }
    }
}