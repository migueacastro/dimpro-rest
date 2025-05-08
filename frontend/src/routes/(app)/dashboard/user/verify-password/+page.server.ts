import { apiURL } from '$lib/api_url';
import { type Actions } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';


export const load: PageServerLoad = async ({cookies}) => {
    const redirectTo = cookies.get("redirectTo") ?? "";
    return {
        redirectTo
    }
};
export const actions: Actions = {
    verifypassword: async ({ request, fetch,cookies }:any) => {
        const formData = await request.formData();
        const response = await fetch(apiURL + "user/verify_password", {
            method: "POST",
            body:JSON.stringify({"password":formData.get("old_password")})
        });
        if(response.ok){
            cookies.set('password',formData.get('password'),{
                path: '/',
                httpOnly: true,
                sameSite: 'lax',
                secure: import.meta.env.VITE_API_URL === "production"
            });
        } 
        return {
            success: response.ok
        }
    }
};
