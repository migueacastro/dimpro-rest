import { apiURL } from "./api_url";
import { headers, refreshCSRFToken } from "./auth";

export async function fetchData(endpoint: string, method: string, body: any = null) {
  let url = apiURL + endpoint;
  if (Array.from(["POST", "PUT", "PATCH"]).includes(method.toUpperCase())) {
    url += '/';
  }
  const response = await fetch(url, {
    method: method,
    headers: headers,
    credentials: 'include',
    body: (body) ? JSON.stringify(body) : null,
  });
  await refreshCSRFToken();
  return response;
}

