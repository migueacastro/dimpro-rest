import { apiURL } from '$lib/api_url.js';
import { checkPermission, permissionError } from '$lib/auth.js';
import { transformInvoices } from '$lib/components/InvoiceChart.js';

export async function load({ locals, fetch, params }) {
	let response = await fetch(apiURL + 'staff/' + params.id);
	if (!checkPermission(locals.user, 'view_staff_user')) {
		return permissionError();
	}
	let reqUser = await response.json();
	let invoices;
	if (checkPermission(locals.user, "view_invoice")) {
		response = await fetch(apiURL + 'invoices/?search=' + reqUser?.name);
		invoices = await response.json();
		const transformedInvoices = transformInvoices(invoices);
		invoices = transformedInvoices;
	}
	
	return {
		reqUser: reqUser,
		invoices: invoices || [],
	};
}
