import { apiURL } from "./api_url";

export async function fetchData(endpoint: string, method: string, body: any = null) {
  let url = apiURL + endpoint;
  if (Array.from(["POST", "PUT", "PATCH"]).includes(method)) {
    url += '/';
  }
  const response = await fetch(url, {
    method: method,
    headers: {
      'Content-Type': 'application/json;charset=UTF-8',
    },
    credentials: 'include',
    body: (body) ? JSON.stringify(body) : null,
  });
  return response;
}

