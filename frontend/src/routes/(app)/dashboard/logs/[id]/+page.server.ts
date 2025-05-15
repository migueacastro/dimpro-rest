import { apiURL } from '$lib/api_url.js';
import { redirect } from '@sveltejs/kit';

export async function load({locals,fetch,params}) {
    if (!locals.user) {
        return redirect(303, '/start');
    }
    let response = await fetch(apiURL+"logs/"+params.id);
    let log = await response.json();
    response = await fetch(apiURL+"staff/"+log.actor);
    if(!response.ok){
        response = await fetch(apiURL+"users/"+log.actor);
    }
    let reqUser = await response.json();
    log.actor = reqUser.email;
    const keys: string[] = Object.keys(log);
    keys.forEach((e:any) => {
        log[e] = JSON.stringify(log[e]);
    });
    return {
        user: locals.user,
        keys,
        log
    };
}
