import { apiURL } from "$lib/api_url";
import type { PageServerLoad } from "../$types";

export const load: PageServerLoad = async ({fetch}) => {
  const response = await fetch(apiURL + 'groups');
  const groups = await response.json();
  if (!response.ok) {
    return {
      groups: null
    };
  }
  return {
    groups
  };
};