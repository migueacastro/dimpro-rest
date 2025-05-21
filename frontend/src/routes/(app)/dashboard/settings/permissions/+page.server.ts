import { apiURL } from '$lib/api_url';
import { fail, type Actions } from '@sveltejs/kit';
import type { PageServerLoad } from '../$types';

export const load: PageServerLoad = async ({ fetch }) => {
	let response = await fetch(apiURL + 'groups');
	const groups = await response.json();
	const groupsObject = groups.map((group: any) => {
		return {
			id: group.id,
			name: group.name,
			permissions: group.permissions.map((permission: any) => {
				return permission.id;
			})
		};
	});
	response = await fetch(apiURL + 'permissions');
	const permissions = await response.json();
	const listPermissionNames = permissions.reduce((acc: any, permission: any) => {
		const parts = permission.codename.split('_');
		const modelName = parts[parts.length - 1];
		if (!Array.from(acc).find((item: any) => item === modelName)) {
			acc.push(modelName);
		}
		return acc;
	}, []);
	const permissionsObject = permissions.reduce((acc: any, permission: any) => {
		const parts = permission.codename.split('_');
		const modelName = parts[parts.length - 1];
		if (!acc[modelName]) {
			acc[modelName] = [];
		}
		acc[modelName].push({
			id: permission.id,
			name: permission.name,
			codename: permission.codename
		});
		return acc;
	}, {});
	console.log('permissionsObject', permissionsObject);
	console.log('listPermissionNames', listPermissionNames);
	return {
		groupsObject,
		listPermissionNames,
		permissionsObject
	};
};

export const actions: Actions = {
	save: async ({ request, fetch }) => {
		const data = await request.formData();
		const groups = JSON.parse(data.get('groups') as string);
    let response: Response;
		for (const group of groups) {
			response = await fetch(apiURL + 'groups/' + group.id+'/', {
				method: 'PATCH',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ ...group })
			});
      if (!response.ok) {
        return fail(500, {
          error: 'Error al actualizar el grupo '+group.name,
        });
      }
		}
    return {
      success: true
    };
		
	}
};
