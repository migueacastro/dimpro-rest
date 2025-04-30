import { apiURL } from "$lib/api_url";

export async function handleDelete({ fetch }:any, endpoint:any){
  const response = await fetch(apiURL+endpoint, {
    method: "DELETE",
  });
  if (response.ok) {
    return { success: true };
  } else {
    return { success: false };
  }
}