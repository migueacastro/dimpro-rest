import { redirect } from '@sveltejs/kit';
import { apiURL } from "$lib/api_url";
import type { Actions, RequestEvent } from "@sveltejs/kit";

const endpoint = "orders";


export const load = async ({ fetch }: RequestEvent) => {
    
    const response = await fetch(apiURL + endpoint);
    const list = await response.json();
  
    return {
      list,
      endpoint,
    };
  };
  
