import { apiURL } from '$lib/api_url.js';
import { checkPermission, permissionError } from '$lib/auth.js';

export async function load({locals,fetch}) {
    let response = await fetch(apiURL+"products/");
    if (!checkPermission(locals.user, "view_product")) {
        return permissionError();
    }
    let products = await response.json();
    return {
        user: locals.user,
        products
    };
}