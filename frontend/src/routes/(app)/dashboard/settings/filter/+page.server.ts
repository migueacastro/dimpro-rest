import { checkAdminGroup, checkPermission, permissionError } from "$lib/auth";
import { redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "../$types";
import { apiURL } from "$lib/api_url";

export const load: PageServerLoad = async ({ locals,fetch }) => {
  if (!checkPermission(locals.user, 'view_logentry')) {
    return permissionError();
  }
  let response = await fetch(apiURL+"users");
  let users = await response.json();
  response = await fetch(apiURL+"staff");
  let staff = await response.json();
  users = [...users,...staff];

  users.sort((a: any, b: any) => a.name.localeCompare(b.name)); // magic code do not touch 
  return {
    users
  }
};
