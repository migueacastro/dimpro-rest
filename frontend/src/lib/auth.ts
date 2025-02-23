import { apiURL } from './api_url';
import { goto } from '$app/navigation';
import { user, users } from '../stores/stores';


// Simplificar la solicitud http al iniciar sesión
export async function fetchLogin(data: any) {
  const url = apiURL + "login";
  const response = await window.fetch(url, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
    },
    credentials: "include",
    body: JSON.stringify(data)
  });
  return response;
}

export async function fetchLogout() {
  const url = apiURL + "logout";
  await window.fetch(url, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
    },
    credentials: "include",
  });
}


export async function fetchStaff(data: any) {
  const url = apiURL + "login/staff";
  const response = await window.fetch(url, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
    },
    body: JSON.stringify(data),
    credentials: "include",
  });
  return response;
}

export async function fetchRegister(data: any) {
  const url = apiURL + "register";
  const response = await window.fetch(url, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
    },
    credentials: "include",
    body: JSON.stringify(data)
  });
  return response;
}

// Solicitar datos del usuario si hay una cookie de token Bearer, retornará el objeto de usuario
// De lo contrario, retornará null
export async function authenticate() {
  const url = apiURL + "user";
  const response = await window.fetch(url, {
    method: 'GET',
    headers: {
      'content-type': 'application/json',
    },
    credentials: "include",
  });
  const data = await response.json()
  if (response.ok) {
    user.set(data);
    return data;
  }


  user.set(null);
  return null;
}

export async function fetchUsers() {
  const url = apiURL + "users";
  const response = await window.fetch(url, {
    method: 'GET',
    headers: {
      'content-type': 'application/json',
    },
    credentials: "include",
  });
  const data = await response.json()
  if (response.ok) {
    users.set(data);
    return data;
  }

  users.set(null);
  return null;
}

export function checkStaffGroup(user: any) {
  if (!user.groups) {
    return false;
  }
  console.log(user.groups);
  for (let group of user?.groups) {
    if (group?.name === "staff") {
      return true;
    }
  }
  return false;
}

export function checkAdminGroup(user: any) {
  if (!user.groups) {
    return false;
  }
  for (let group of user?.groups) {
    if (group?.name === "admin") {
      return true;
    }
  }
}
