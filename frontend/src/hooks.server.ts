import { apiURL } from '$lib/api_url';
import type { Handle, HandleFetch } from '@sveltejs/kit';
import { fetchData } from '$lib/utils';

import dns from "node:dns";
import { fetchCSRFToken } from '$lib/auth';
//dns.setDefaultResultOrder("ipv4first");


export const handle: Handle = async ({ event, resolve }) => {
  //if (event.url.pathname.startsWith('/custom')) {
  //	return new Response('custom response');
  //}
  //
  if (!event.locals.user) {
    if (event.cookies.get('sessionid')) {
      event.locals.user = await getUserFromCookie(event);
    } else {
      event.locals.user = null;
    }
  }
  
  await checkLogout({ event});

  const response = await resolve(event);
  return response;
};

export const handleFetch: HandleFetch = async ({ request, fetch, event }) => {
    const allCookies = event.cookies.getAll();
    const cookieHeader = allCookies.map((cookie: any) => `${cookie.name}=${cookie.value}`).join('; ');
    request = new Request(request.url, {
      headers: {
        Cookie: cookieHeader,

      }, credentials: 'include'
    });
    if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(request.method)) {
        // Fetch the CSRF token from the backend
        const csrfResponse = await fetch(apiURL + 'csrf');
        const csrfData = await csrfResponse.json();
        const csrfToken = csrfData.csrfToken || (await fetchCSRFToken());

        // Set headers for the request
        request.headers.set('X-CSRFToken', csrfToken);
        request.headers.set('content-type', 'application/json');
       
    }

    // Forward the request to the backend
    return fetch(request);
};

export async function getUserFromCookie(event: { cookies: any; fetch: typeof fetch}) {
  const sessionid = event.cookies.get('sessionid'); // Get the sessionid cookie
  if (!sessionid) {
    return null; // No session cookie, so no user
  }
 

  const response = await event.fetch(apiURL + 'user');

  if (!response.ok) {
    return null;
  }

  const data = await response.json();
  return data;
}

export async function checkLogout({ event }: any) {
  if (event.url.pathname === '/logout') {
    event.cookies.delete('sessionid', { path: '/' });
    event.locals.user = null;
  }
}