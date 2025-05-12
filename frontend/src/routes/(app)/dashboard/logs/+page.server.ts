import { apiURL } from "$lib/api_url";
import { redirect } from "@sveltejs/kit";

export async function load({ locals,fetch,url }) {
    if (!locals.user) {
        return redirect(303, '/start');
    }
    const date = url.searchParams.get('date');
    let response = await fetch(apiURL+"logs");
    let logs = await response.json();
    logs = logs.filter((e:any) => e.timestamp.includes(date));
    return {
        user: locals.user,
        logs
    };
}
