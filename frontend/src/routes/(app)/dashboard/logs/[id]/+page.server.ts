import { apiURL } from '$lib/api_url.js';
import { redirect } from '@sveltejs/kit';
import {checkStaffGroup} from "$lib/auth.js";

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
    let logStr = JSON.stringify(log);
    return {
        user: locals.user,
        logStr
    };
}
