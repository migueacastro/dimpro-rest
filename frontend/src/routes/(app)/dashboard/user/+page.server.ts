
import { apiURL } from '$lib/api_url';
import type { RequestEvent } from '@sveltejs/kit';
import { checkPermission} from '$lib/auth';
import { transformInvoices } from '$lib/components/InvoiceChart';

export const load = async ({ fetch, locals }: RequestEvent) => {
    if (checkPermission(locals.user, "view_invoice")) {
       
        
        let response = await fetch(apiURL + 'invoices/?search=' + locals.user?.name);
        const invoices = await response.json();
				

        // Transformar las facturas
        const transformedInvoices = transformInvoices(invoices);
        return {  
            invoices: transformedInvoices,
        };
    }
};

