import { apiURL } from '$lib/api_url';

export async function changestatus({ fetch, request }: any) {
	const formData: FormData = await request.formData();

	const orderStatus = formData.get('orderStatus') ?? '';
	const newOrderStatus = orderStatus === 'preparado' ? 'pendiente' : 'preparado';

	const orderId: any = formData.get('orderId') ?? '';

	const response = await fetch(apiURL + 'orders/' + orderId + '/', {
		method: 'PATCH',
		body: JSON.stringify({
			status: newOrderStatus
		})
	});

	if (response.ok) {
		const data = await response.json();
		return {
			success: true,
			data: data.status
		};
	}

	console.error('PATCH request failed:', response.status, await response.text());
	return {
		success: false
	};
}
