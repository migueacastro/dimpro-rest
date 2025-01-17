import { apiURL } from './api_url';
import Cookies from 'js-cookie';


// Simplificar la solicitud http al iniciar sesión
export async function fetchLogin(data: any) { 
    const url = apiURL + "login";
    const response = await window.fetch(url, {
        method: 'POST',
        headers: {
            'content-type': 'application/json',
        },
        body: JSON.stringify(data)
    });
    return response;
} 

// Solicitar datos del usuario si hay una cookie de token Bearer, retornará el objeto de usuario
// De lo contrario, retornará null
export async function authenticate() {
    const url = apiURL + "user";
    const token = Cookies.get("token");
    console.log(token);
    if (token) {
        const response = await window.fetch(url, {
            method: 'GET',
            headers: {
                'content-type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
        });
        const data = await response.json()
        if (response.ok) {
            return data;
        }
        return null;
    }
}