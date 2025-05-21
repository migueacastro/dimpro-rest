import { checkAdminGroup } from "$lib/auth";
import { redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "../$types";

export const load: PageServerLoad = async ({locals}) => {
  //if (!checkAdminGroup(locals.user)) {
  //  return redirect(303, "/dashboard");
  //}
};