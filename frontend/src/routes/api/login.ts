import { fetchLogin } from "$lib/auth";
// src/routes/api/login.js
export async function post({ request }) {
  const formData = await request.json();
  const response = await fetchLogin(formData);

  const data = await response.json();
  if (response.ok) {
    return {
      status: 200,
      headers: {
        'Set-Cookie': `token=${data.token}; Path=/; Max-Age=${365 * 24 * 60 * 60}; Secure; HttpOnly; SameSite=Strict`
      },
      body: {
        message: 'Login successful'
      }
    };
  } else {
    return {
      status: 401,
      body: {
        data
      }
    };
  }
}
