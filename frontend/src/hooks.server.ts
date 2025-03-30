import { apiURL } from '$lib/api_url';
import type { Handle } from '@sveltejs/kit';
import { fetchData } from '$lib/utils';

import dns from "node:dns";
//dns.setDefaultResultOrder("ipv4first");


export const handle: Handle = async ({ event, resolve }) => {
  //if (event.url.pathname.startsWith('/custom')) {
  //	return new Response('custom response');
  //}
  //
  if (!event.locals.user) {
    if (event.cookies.get('sessionid')) {
      event.locals.user = await getUserFromCookie();
    }
  }
  console.log("event.locals.user", event.locals.user);

  const response = await resolve(event);
  return response;
};


export async function getUserFromCookie() {
  console.log(apiURL);

  const response: any = await fetchData('user', 'GET');
  if (response.ok) {
    const data = await response.json();
    console.log(data);
    return {data};

  }
  console.log(response);
  return null;
  
};

