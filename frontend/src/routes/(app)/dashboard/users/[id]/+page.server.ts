import { apiURL } from '$lib/api_url.js';
import { redirect } from '@sveltejs/kit';

export async function load({locals,fetch,params}) {
    let response = await fetch(apiURL+"users/"+params.id);
    if (!locals.user) {
        return redirect(303, '/start');
    }
    let reqUser = await response.json();
    return {
        user: locals.user,
        reqUser: reqUser
    };
}