import { apiURL } from './api_url';
import { fail } from '@sveltejs/kit';
import { user, users } from '../stores/stores';
import { redirect } from '@sveltejs/kit';
import Cookies from 'js-cookie';

// Simplificar la solicitud http al iniciar sesión
export let headers: any = {
	'X-CSRFToken': Cookies.get('csrftoken') ?? '',
	'content-type': 'application/json'
};

export async function fetchCSRFToken() {
	const response = await fetch(apiURL + 'csrf');
	const data = await response.json();
	return data;
}

export async function fetchLogin(data: any) {
	const url = apiURL + 'login';
	const response = await fetch(url, {
		method: 'POST',
		body: data
	});
	return response;
}

export async function fetchRegister(data: any) {
	const url = apiURL + 'register';
	const response = await fetch(url, {
		method: 'POST',
		body: data
	});
	return response;
}

export async function fetchUsers() {
	const url = apiURL + 'users';
	const response = await fetch(url, {
		method: 'GET'
	});
	const data = await response.json();
	if (response.ok) {
		users.set(data);
		return data;
	}

	users.set(null);
	return null;
}

export function checkStaffGroup(user: any) {
	if (!user?.groups) {
		return false;
	}
	for (let group of user?.groups) {
		if (group?.name === 'staff') {
			return true;
		}
	}
	return false;
}

export function checkAdminGroup(user: any) {
	if (!user?.groups) {
		return false;
	}
	for (let group of user?.groups) {
		if (group?.name === 'admin') {
			return true;
		}
	}
}

export async function login({ fetch, locals, formData, isStaff, cookies }: any) {
	let url = isStaff ? apiURL + 'login/staff' : apiURL + 'login';


	const response = await fetch(url, {
		method: 'POST',
		body: JSON.stringify(Object.fromEntries(formData))
	});

	if (!response.ok) {
		const data = await response.json();
		console.log(data);
		return fail(400, { error: data, success: false });
	}
  
	const data = await response.json();
	const setCookieHeader = response.headers.get('set-cookie');
	if (setCookieHeader) {
		// Split the Set-Cookie header into individual cookies
		const cookiePairs = setCookieHeader.split(',').map((cookie: any) => cookie.split(';')[0]); // Extract only the key=value part

		// Set each cookie in the browser
		for (const cookiePair of cookiePairs) {
			const [cookieName, cookieValue] = cookiePair.split('=');
			if (cookieName && cookieValue) {
				cookies.set(cookieName.trim(), cookieValue.trim(), {
					httpOnly: true,
					path: '/',
					sameSite: 'lax',
					secure: true, // Use secure cookies if your app is served over HTTPS
					maxAge: 60 * 60 * 24 * 30 // Example: 7 days
				});
			}
		}
	}

	locals.user = data;
	return {
		success: true
	};
	//return redirect(303, '/dashboard');
}
