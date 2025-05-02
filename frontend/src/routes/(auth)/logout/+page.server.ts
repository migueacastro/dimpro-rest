import { redirect } from '@sveltejs/kit';

export async function load({locals, cookies}) {
    throw redirect(303, '/start');
}