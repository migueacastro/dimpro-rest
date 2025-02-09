import { apiURL } from "./api_url";
import Cookies from 'js-cookie';

export async function postData(endpoint: string, body: any) {
  let url = apiURL + endpoint + '/';
  let token = Cookies.get("token");
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json;charset=UTF-8',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(body)
  });
  return response;
}

export async function putData(endpoint: string, body: any) {
  let url = apiURL + endpoint + '/';
  let token = Cookies.get("token");
  const response = await fetch(url, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json;charset=UTF-8',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(body)
  });
  return response;
}

export async function patchData(endpoint: string, body: any) {
  let url = apiURL + endpoint + '/';
  let token = Cookies.get("token");
  const response = await fetch(url, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json;charset=UTF-8',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(body)
  });
  return response;
}

export async function deleteData(endpoint: string) {
  let url = apiURL + endpoint;
  let token = Cookies.get("token");
  const response = await fetch(url, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json;charset=UTF-8',
      'Authorization': `Bearer ${token}`
    }
  });
  return response;
}

export async function getData(endpoint: string) {
  let url = apiURL + endpoint;
  let token = Cookies.get("token");
  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json;charset=UTF-8',
      'Authorization': `Bearer ${token}`
    }
  });
  return response;
}
