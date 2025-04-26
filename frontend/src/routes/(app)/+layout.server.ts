import { redirect } from '@sveltejs/kit';

export async function load({locals, cookies}) {
    if (!locals.user) {
        return redirect(303, '/start');
    }
    
    return {
        user: locals.user
    };
}
