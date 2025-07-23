import { apiURL } from "$lib/api_url";
import { checkPermission, permissionError } from "$lib/auth";
import type { PageServerLoad } from "../../catalog/$types";

export const load: PageServerLoad = async ({fetch, params, locals}: any) => {
  if (!checkPermission(locals.user, 'view_product')) {
    return permissionError();
  }
  const response = await fetch(apiURL+'products/'+ params.id);
  const product = await response.json();
  return {
    product,
  }
};