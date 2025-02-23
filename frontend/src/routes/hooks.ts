// src/hooks.js
export async function handle({ request, resolve }) {
  // Leer la cookie 'token' de la solicitud
  const cookies = request.headers.get('cookie') || '';
  const token = cookies.split(';').find(c => c.trim().startsWith('token='))?.split('=')[1];

  // Añadir el token al objeto `request.locals` para usarlo en cualquier parte
  request.locals.token = token;

  // Continuar con la solicitud
  const response = await resolve(request);

  return response;
}

export function getSession(request) {
  // Devolver el token en la sesión para que esté disponible en el frontend
  return {
    token: request.locals.token
  };
}
