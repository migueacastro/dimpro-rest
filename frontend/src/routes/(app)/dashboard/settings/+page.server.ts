import { checkAdminGroup, checkPermission, permissionError } from "$lib/auth";
import { redirect, type Actions } from "@sveltejs/kit";
import type { PageServerLoad } from "../$types";
import { apiURL } from "$lib/api_url";
import { fail } from "@sveltejs/kit";

export const load: PageServerLoad = async ({locals}) => {
  if (!checkPermission(locals.user, 'view_settings_user')) {
    return permissionError();
  }
};

export const actions: Actions = {
  updatedb: async ({fetch}) => {
    const response = await fetch(apiURL+'updatedb');
    if (response.ok) {
      return {
        success: true
      }
    } else {
      return fail(400, {
        error: await response.text(),
        success: false
      });
    }
  }
};