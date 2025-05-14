import { apiURL } from "$lib/api_url";
import { redirect } from "@sveltejs/kit";

export async function load({ locals, fetch, url }) {
    if (!locals.user) {
        return redirect(303, '/start');
    }
    const date: any = url.searchParams.get('date');
    const action: any = url.searchParams.get('action');
    const systemParse: any = url.searchParams.get('systemLogs');
    const systemLogs: boolean = JSON.parse(systemParse);
    let response = await fetch(apiURL + "logs");
    let logs = await response.json();
    logs.forEach((e: any) => {
        switch (e.action) {
            case 0:
                e.changes_text = "creación";
                break;
            case 1:
                e.changes_text = "actualización";
                break;
            case 2:
                e.changes_text = "eliminación";
                break;
        }
    });
    logs.forEach((e: any) => {
        if (e.changes) {
            const keys: string[] = Object.keys(e.changes);
            if (keys[0] === "id") {
                e.changes = `ID: ${e['changes'][keys[0]][0]}`
            } else {
                e.changes = keys[0];
            }

        }
    });
    if (date?.length > 0) {
        logs = logs.filter((e: any) => e.timestamp.includes(date));

    } else if (action?.length > 0) {
        if (action !== "pet") {
            logs = logs.filter((e: any) => e.changes_text === action);
        } else {
            logs = logs.filter((e: any) => !["actualización", "eliminación", "creación"].includes(e.changes_text));
        }
    }
    if (systemLogs) {
        logs = logs.filter((e: any) => e.actor);
    }
    return {
        user: locals.user,
        logs
    };
}
