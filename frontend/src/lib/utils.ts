import { apiURL } from "./api_url";
import Cookies from 'js-cookie';

// Fetch that includes bearer auth cookie inside headers
export async function fetchData(endpoint: string, method: string, body: any = null) {
  let url = apiURL + endpoint;
  if (Array.from(["POST", "PUT", "PATCH"]).includes(method)) {
    url += '/';
  }
  let token = Cookies.get("token");
  const response = await fetch(url, {
    method: method,
    headers: {
      'Content-Type': 'application/json;charset=UTF-8',
      'Authorization': `Bearer ${token}`
    },
    body: (body) ? JSON.stringify(body) : null,
  });
  return response;
}

