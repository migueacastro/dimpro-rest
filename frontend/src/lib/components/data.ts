import Cookies from "js-cookie";
import { apiURL } from "$lib/api_url";
export async function getData(endpoint: string): Promise<any> {
  endpoint = apiURL + endpoint;
  const token = Cookies.get("token");
  const response = await window.fetch(endpoint, {
    method: 'GET',
    headers: {
      'content-type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  });

  const data = await response.json();
  return data;
}

