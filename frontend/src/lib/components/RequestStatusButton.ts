import { apiURL } from '$lib/api_url';

export async function approve({ fetch, request }: any) {
	const formData: FormData = await request.formData();

	const requestId: any = formData.get('requestId') ?? '';
	console.log(requestId)
	const response = await fetch(apiURL + 'contact_add_request_approval', {
		method: 'POST',
		body: JSON.stringify({
			id: requestId,
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
