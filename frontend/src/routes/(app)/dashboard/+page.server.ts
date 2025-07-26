
import { apiURL } from '$lib/api_url';
import type { RequestEvent } from '@sveltejs/kit';
import { checkPermission} from '$lib/auth';

const endpoint = 'orders';

export const load = async ({ fetch, locals }: RequestEvent) => {
    if (checkPermission(locals.user, "view_advanced_homepage_user")) {
        let response = await fetch(apiURL + endpoint);
        const list = await response.json();
      
       
        return {
            list,
            endpoint,
        };
    }
};
