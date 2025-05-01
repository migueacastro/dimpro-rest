import { apiURL } from "$lib/api_url";

export async function handleDelete({ fetch }: any, endpoint: any) {
  const response = await fetch(apiURL + endpoint, {
    method: "DELETE",
  });
  if (response.ok) {
    return { success: true }; // this is the result, you can also pass data inside it
  } else {
    return { success: false };
  }
}
