import { apiURL } from '$lib/api_url.js';
import { checkPermission, permissionError } from '$lib/auth.js';
import { redirect } from '@sveltejs/kit';
import { transformInvoices } from '$lib/components/InvoiceChart.js';

export async function load({ locals, fetch, params }) {
	let response = await fetch(apiURL + 'users/' + params.id);
	let reqUser = await response.json();
	let invoices;
	if (checkPermission(locals.user, "view_invoice")) {
		response = await fetch(apiURL + 'invoices/?search=' + reqUser?.name);
		invoices = await response.json();
		const transformedInvoices = transformInvoices(invoices);
		invoices = transformedInvoices;
	}

	if (!checkPermission(locals.user, 'view_user')) {
		return permissionError();
	}
	
	return {
		reqUser: reqUser,
		invoices: invoices || [],
	};
}
