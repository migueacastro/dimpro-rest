import { apiURL } from '$lib/api_url.js';
import { checkPermission, checkStaffGroup, permissionError } from '$lib/auth';
import { redirect, type Actions } from '@sveltejs/kit';

export async function load({ fetch, locals }: any) {
    if (!locals.user) {
        return redirect(303, '/start');
    }
    let fields: any = [];
    if (checkPermission(locals.user, 'change_own_cardid_user')) {
        fields.push({ type: 'text', value: '', name: 'card_id', label: 'Cédula' });
    }
    if (checkPermission(locals.user, 'change_own_email_user')) {
		fields.push({ type: 'email', value: '', name: 'email', label: 'Email' });
	}
	if (checkPermission(locals.user, 'change_own_name_user')) {
		fields.push({ type: 'text', value: '', name: 'name', label: 'Nombre' });
	}
	if (checkPermission(locals.user, 'change_own_phonenumber_user')) {
		fields.push({ type: 'text', value: '', name: 'phonenumber', label: 'Telefono' });
	}
    if (checkPermission(locals.user, 'change_own_address_user')) {
        fields.push({ type: 'longtext', value: '', name: 'address', label: 'Dirección' });
    }
    
	if (fields.length < 1) {
		return permissionError();
	}
    return {
        user: locals.user,
        fields
    };
    
}

export const actions: Actions = {
    edit: async ({ request, fetch, locals, cookies }) => {
        const formData = await request.formData();
        const id = formData.get("id");
        let endpoint = "";
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

        let response = await fetch(apiURL + 'user', {
            method: 'PATCH',
            body: JSON.stringify(body)
        });
        return {
            success: response.ok,
            error: response.statusText
        }
    }
}
