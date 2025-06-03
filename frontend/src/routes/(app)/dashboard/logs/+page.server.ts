import { apiURL } from '$lib/api_url';
import { checkPermission, permissionError } from '$lib/auth.js';
import { CustomDataHandler } from '$lib/components/pagination/PaginationDatatable.js';
import { formatDateTime, getCurrentDateTime } from '$lib/datetime.js';

export async function load({ locals, fetch, url }) {
	if (!checkPermission(locals.user, 'view_logentry')) {
		return permissionError();
	}
	const qs = url.searchParams.toString() ? `?${url.searchParams.toString()}` : '';
	console.log(qs);
	let response = await fetch(apiURL + 'logs' + qs);
	let query: any = await response.json();
    query.results = query.results.map((result:any) => {
        if (!result.actor) {
            result.actor_name = "Sistema";
        }
        return {...result, timestamp: formatDateTime(result.timestamp as string)}
    })

	/*
    const date: any = url.searchParams.get('date');
    const action: any = url.searchParams.get('action');
    const systemParse: any = url.searchParams.get('systemLogs');
    const selectedUser:any = url.searchParams.get('user');
    const systemLogs: boolean = JSON.parse(systemParse);
    let response = await fetch(apiURL + "logs");
    let logs = await response.json();
    logs = logs.results;
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

    }
    if (action?.length > 0) {
        if (action !== "pet") {
            logs = logs.filter((e: any) => e.changes_text === action);
        } else {
            logs = logs.filter((e: any) => !["actualización", "eliminación", "creación"].includes(e.changes_text));
        }
    }
    if(selectedUser?.length>0){
        logs = logs.filter((e:any) => e.actor===parseInt(selectedUser));
    }
    if (systemLogs) {
        logs = logs.filter((e: any) => e.actor);
    }
    return {
        user: locals.user,
        logs
    };
    */
   return {
    handler: new CustomDataHandler({url, query}).serialize(),
   }
}


