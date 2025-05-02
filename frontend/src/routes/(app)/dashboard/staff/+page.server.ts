import { apiURL } from '$lib/api_url.js';
import { redirect, type Actions } from '@sveltejs/kit';

export async function load({locals,fetch}) {
    let response = await fetch(apiURL+"staff");
    if (!locals.user) {
        return redirect(303, '/start');
    }
    let users = await response.json();
    return {
        user: locals.user,
        users: users
    };
}
export const actions: Actions = {
    handleDelete: async ({request,fetch}) => {
        const formData = await request.formData();
        const id = formData.get("id");
        let response = await fetch(apiURL+`staff/${id}/`,{
            method:"DELETE"
        });
        return {
            success:response.ok,
            error:response.statusText
        }
    }
}