import { apiURL } from '$lib/api_url.js';
import { checkPermission, permissionError } from '$lib/auth.js';

export async function load({ locals, fetch, params }) {
    if (!checkPermission(locals.user, "view_logentry")) {
        return permissionError();
    }
    let response = await fetch(apiURL + "logs/" + params.id);
    let log = await response.json();
    response = await fetch(apiURL + "staff/" + log.actor);
    if (!response.ok) {
        response = await fetch(apiURL + "users/" + log.actor);
    }
    let reqUser = await response.json();
    log.actor = reqUser.email;
    const keys: string[] = Object.keys(log);
    keys.forEach((e: any) => {
        if (log[e]) {
            log[e] = JSON.stringify(log[e]);
        }
    });
    return {
        user: locals.user,
        log
    };
}
