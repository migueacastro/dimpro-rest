import { apiURL } from '$lib/api_url.js';
import { redirect, type Actions } from '@sveltejs/kit';

export async function load({locals,fetch}) {
    if (!locals.user) {
        return redirect(303, '/start');
    }
    return {
        user: locals.user
    };
}