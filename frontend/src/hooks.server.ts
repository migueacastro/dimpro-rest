import { apiURL } from '$lib/api_url';
import type { Handle, HandleFetch } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
  // and this, nothing else
  const sessionid = event.cookies.get('sessionid'); // get the sessionid cookie
  if (sessionid && !event.locals.user) {
    event.locals.user = await getUserFromCookie(event); // if there is a sessionid cookie, but no user in locals, then we retrieve the user from the sessionid cookie
  } else if (!sessionid) {
    event.locals.user = null; // if there is no sessionid cookie, then we set the user to null
  }

  
  await checkLogout({ event }); // huh, just checks if the page is /logout, it will remove the cookie and the locals about the user so that its just null

  // now, hear me out

  const response = await resolve(event); // this
  return response; // this
};

export const handleFetch: HandleFetch = async ({ request, fetch, event }) => {
  const body = request.method === 'GET' ? null : await request.text(); // Read the body if not a GET request
  const allCookies = event.cookies.getAll();
  let cookieHeader = allCookies.map((cookie: any) => `${cookie.name}=${cookie.value}`).join('; ');

  // Fetch CSRF token if needed
  let csrfToken = '';
  if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(request.method)) {
    try {
      const csrfResponse = await fetch(apiURL + 'csrf');
      if (csrfResponse.ok) {
        const csrfData = await csrfResponse.json();
        csrfToken = csrfData.csrftoken;

        // Update the cookie header with the new CSRF token
        cookieHeader = allCookies
          .map((cookie: any) => {
            if (cookie.name === 'csrftoken') {
              return `${cookie.name}=${csrfToken}`;
            }
            return `${cookie.name}=${cookie.value}`;
          })
          .join('; ');
      } else {
        console.error('Failed to fetch CSRF token:', csrfResponse.status);
      }
    } catch (error) {
      console.error('Error fetching CSRF token:', error);
    }
  }

  // Recreate the request with updated headers
  request = new Request(request.url, {
    headers: {
      ...Object.fromEntries(request.headers), // Preserve existing headers
      Cookie: cookieHeader, // Add the Cookie header
      ...(csrfToken && { 'X-CSRFToken': csrfToken }) // Add the CSRF token if available
    },
    credentials: 'include', // Ensure cookies are included
    method: request.method,
    body // Preserve the body for non-GET requests
  });
  request.headers.set('Content-Type', 'application/json'); // Set the content type to JSON

  return fetch(request);
};
export async function getUserFromCookie(event: { cookies: any; fetch: typeof fetch }) {
  const sessionid = event.cookies.get('sessionid'); // Get the sessionid cookie

  // first you retrieve the sessionid cookie

  if (!sessionid) {
    return null; // No session cookie, so no user
  }

  const response = await event.fetch(apiURL + 'user');
  // Since the cookie is actually in SSR, that means that if we do OUR SPECIAL "fetch" of the parameters (NOT THE NORMAL "fetch"), it will include our cookies automatically :D

  if (!response.ok) {
    return null; // if it gives an error, just return null for the user object
  }

  const data = await response.json();
  return data; // and here well, just return the user
}

export async function checkLogout({ event }: any) {
  if (event.url.pathname === '/logout') {
    event.cookies.delete('sessionid', { path: '/' });
    event.locals.user = null;
  }
}
