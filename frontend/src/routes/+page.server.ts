import { redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({locals}: any) => {
  if (locals.user) {
    return redirect(303, "/dashboard/");
  }
  return redirect(303, "/start");
};