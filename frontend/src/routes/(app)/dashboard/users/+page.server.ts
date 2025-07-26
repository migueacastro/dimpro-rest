import { apiURL } from '$lib/api_url.js';
import { checkPermission, permissionError } from '$lib/auth.js';
import { redirect, type Actions } from '@sveltejs/kit';
import { transformInvoices } from '$lib/components/InvoiceChart.js';

export async function load({locals,fetch}) {
    let response = await fetch(apiURL+"users");
    if (!checkPermission(locals.user, "view_user")) {
        return permissionError();
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
        let response = await fetch(apiURL+`users/${id}/`,{
            method:"DELETE"
        });
        return {
            success:response.ok,
            error:response.statusText
        }
    }
}