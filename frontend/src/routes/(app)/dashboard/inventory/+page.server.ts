import { apiURL } from '$lib/api_url.js';
import { redirect } from '@sveltejs/kit';

export async function load({locals,fetch}) {
    let response = await fetch(apiURL+"products/");
    if (!locals.user) {
        return redirect(303, '/start');
    }
    let products = await response.json();
    return {
        user: locals.user,
        products
    };
}