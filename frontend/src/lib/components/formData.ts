import { getData, deleteData, patchData, putData, postData } from '$lib/utils'

export async function formData(endpoint: string, body: any, method: string) {
    switch (method.toUpperCase()) {
        case 'GET':
            getData(endpoint);
            break;
        case 'POST':
            postData(endpoint, body);
            break;
        case 'PUT':
            putData(endpoint, body);
            break;
        case 'PATCH':
            patchData(endpoint, body);
            break;
        case 'DELETE':
            deleteData(endpoint);
            break;
    }
}