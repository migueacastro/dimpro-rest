import { apiURL } from '$lib/api_url.js';
import { checkPermission, permissionError } from '$lib/auth';
import { redirect, type Actions } from '@sveltejs/kit';

export async function load({ fetch, locals, params }: any) {
	let response = await fetch(apiURL + `users/${params.id}`);
	const data = await response.json();

	if (!checkPermission(locals.user, 'change_user')) {
		return permissionError();
	}
	data.groups = data.groups.map((group: any) => {
		return group.id;
	});
	const reqUser = data;
	response = await fetch(apiURL + 'groups/');
	let groups = await response.json();
	if (!checkPermission(locals.user, 'change_staff_user')) {
		groups = groups.filter((group: any) => 
			group.name !== 'admin');
	}
	groups = groups.map((group: any) => {
		return {
			label: group.name,
			value: group.id
		};
	});
	return {
		reqUser,
		groups
	};
}

export const actions: Actions = {
	edit: async ({ request, fetch }) => {
		const formData = await request.formData();
		const id = formData.get('id');
		const endpoint = formData.get('endpoint');
		formData.delete('endpoint');
		const keys = Array.from(formData.keys());
		const values: any = Array.from(formData.values());
		let body: any = {};
		for (let i = 0; i < keys.length; i++) {
			if (values[i].toString().trim() !== '') {
				if (keys[i].toString().trim() === 'groups') {
					body[keys[i]] = [parseInt(values[i])];
					continue; // skip the JSON.parse step for groups
				}
				try {
					body[keys[i]] = JSON.parse(values[i] as string);
				} catch {
					body[keys[i]] = values[i];
				}
			}
		}

		let response = await fetch(apiURL + endpoint + `/${id}/`, {
			method: 'PATCH',
			body: JSON.stringify(body)
		});
		if (!response.ok) {
			console.log("Error");
		}
		const data = await response.json()
		return {
			success: response.ok,
			error: data.error
		};
	}
};
