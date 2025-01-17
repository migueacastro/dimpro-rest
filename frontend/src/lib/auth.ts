import { apiURL } from './api_url';


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
