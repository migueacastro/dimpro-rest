import { redirect } from '@sveltejs/kit';

export async function load({locals, cookies}) {
    return redirect(303, '/start');
}