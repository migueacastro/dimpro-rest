import { apiURL } from "./api_url";
import { headers } from "./auth";

export async function fetchData(endpoint: string, method: string, body: any = null) {
  let url = apiURL + endpoint;
  if (Array.from(["POST", "PUT", "PATCH", "DELETE"]).includes(method)) {
    url += '/';
  }
  const response = await fetch(url, {
    method: method,
    headers: headers,
    credentials: 'include',
    body: (body) ? JSON.stringify(body) : null,
  });
  return response;
}

