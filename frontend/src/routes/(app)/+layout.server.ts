import { redirect } from '@sveltejs/kit';

export async function load({ locals, url }) { //This is +layout.server.ts, it passes the data into every children page without needing to redefine it, so remember this whenever you use user
  if (!locals.user ) {

    return redirect(303, '/start');
  }
  return {
    user: locals.user, // this one
     show_back_button: url.pathname !== '/dashboard',
  };
}
