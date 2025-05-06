import { apiURL } from '$lib/api_url';
import { type Actions } from '@sveltejs/kit';

export const actions: Actions = {
    verifypassword: async ({ request, fetch,cookies }:any) => {
        const formData = await request.formData();
        const response = await fetch(apiURL + "user/verify_password", {
            method: "POST",
            body:JSON.stringify({"old_password":formData.get("old_password")})
        });
        if(response.ok){
            cookies.set('old_password',formData.get('old_password'),{
                path: '/dashboard/user/change-password',
                httpOnly: true,
                sameSite: 'lax',
                //secure: true <- specify in production
            });
        }
        return {
            success: response.ok
        }
    }
};
