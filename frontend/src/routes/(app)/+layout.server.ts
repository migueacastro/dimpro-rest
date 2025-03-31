import { redirect } from '@sveltejs/kit';

export async function load({locals}) {
    if (!locals.user) {
        return redirect(303, '/start');
    }
    console.log(locals.user);
    return {
        user: locals.user
    };
}

