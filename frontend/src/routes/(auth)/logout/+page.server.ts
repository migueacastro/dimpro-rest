import { fetchLogout } from '$lib/auth';
import { redirect } from '@sveltejs/kit';

export async function load({locals, cookies}) {
    await fetchLogout();
    throw redirect(303, '/start');
}