import { checkAdminGroup } from "$lib/auth";
import { redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "../$types";
import { apiURL } from "$lib/api_url";

export const load: PageServerLoad = async ({ locals,fetch }) => {
  if (!locals.user) {
    return redirect(303, '/start');
  } else if (!checkAdminGroup(locals.user)) {
    return redirect(303, '/dashboard');
  }
  let response = await fetch(apiURL+"users");
  let users = await response.json();
  response = await fetch(apiURL+"staff");
  let staff = await response.json();
  users = [...users,...staff];
  return {
    users
  }
};
