import { apiURL } from '$lib/api_url.js';
import { checkPermission, permissionError } from '$lib/auth.js';
import { redirect, type Actions } from '@sveltejs/kit';

export async function load({ locals, fetch }) {
	if (!checkPermission(locals.user, 'add_user')) {
		return permissionError();
	}
	let response = await fetch(apiURL + 'groups/');
	let groups = await response.json();
	if (!checkPermission(locals.user, 'change_staff_user')) {
		groups = groups.filter((group: any) => group.name !== 'admin');
	}
	groups = groups.map((group: any) => {
		return {
			label: group.name,
			value: group.id
		};
	});
	return {
		groups
	};
}

export const actions: Actions = {
	add: async ({ request, fetch }) => {
		const formData = await request.formData();
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
		let response = await fetch(apiURL + endpoint, {
			method: 'POST',
			body: JSON.stringify(body)
		});

		const data = await response.json()
		return {
			success: response.ok,
			error: data.error
		};
	}
};
