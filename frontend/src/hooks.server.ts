import { apiURL } from '$lib/api_url';
import type { Handle, HandleFetch } from '@sveltejs/kit';
import { fetchCSRFToken } from '$lib/auth';

export const handle: Handle = async ({ event, resolve }) => { // and this, nothing else
  if (!event.locals.user) { // if there is no local with an user
    if (event.cookies.get('sessionid')) {
      event.locals.user = await getUserFromCookie(event); // but there is actually a session cookie, retrieve the user from the session cookie, and update the locals
    } else {
      event.locals.user = null; // then this means no sessionid cookie, so we are logged out
    }
  }
  await checkLogout({ event}); // huh, just checks if the page is /logout, it will remove the cookie and the locals about the user so that its just null


  // now, hear me out


  const response = await resolve(event); // this
  return response; // this
};

export const handleFetch: HandleFetch = async ({ request, fetch, event }) => {
    const body = await request.text(); 
    const allCookies = event.cookies.getAll(); // here i get an array of all the cookies as objects
    let cookieHeader = allCookies.map((cookie: any) => `${cookie.name}=${cookie.value}`).join('; '); // here i turn the cookies into one single string that can be used on the http headers, like this, see?

    request = new Request(request.url, {
      credentials: 'include',
      method: request.method,
      body: request.method === 'GET' ? null : body, // here i set the body of the request, if its a GET request, then no body
    });

    if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(request.method)) {
        // Fetch the CSRF token from the backend
        const csrfResponse = await fetch(apiURL + 'csrf');
        const csrfData = await csrfResponse.json();
        const csrfToken = csrfData.csrftoken;

        cookieHeader = allCookies.map((cookie: any) => {
          if (cookie.name === 'csrftoken') {
            return `${cookie.name}=${csrfToken}`; // Update the CSRF token cookie
          }
          return `${cookie.name}=${cookie.value}`; // Keep other cookies unchanged
        }).join('; ');
         // Set the updated cookie header
        request.headers.set('X-CSRFToken', csrfToken);
    }  
    request.headers.set('Cookie', cookieHeader);
    request.headers.set('Content-Type', 'application/json');
    return fetch(request);
};

export async function getUserFromCookie(event: { cookies: any; fetch: typeof fetch}) {
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
