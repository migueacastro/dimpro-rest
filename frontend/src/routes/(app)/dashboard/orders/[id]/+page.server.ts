import { apiURL } from "$lib/api_url.js";
import { checkPermission, permissionError } from "$lib/auth.js";
import type { Actions } from "@sveltejs/kit";

export async function load({ params, fetch, locals }) {
  if (!checkPermission(locals.user, "view_order")) {
    return permissionError();
  }
  const response = await fetch(apiURL + "orders/" + params.id);
  const order = await response.json();
  return {
    id: params.id,
    order,
  };
}

export const actions: Actions = {
  changestatus: async ({ fetch, request }: any) => {
    const formData: FormData = await request.formData();
  
    const orderStatus = formData.get('orderStatus') ?? '';
    const newOrderStatus = orderStatus === 'preparado' ? 'pendiente' : 'preparado';
  
    const orderId: any = formData.get('orderId') ?? '';
  
    const response = await fetch(apiURL + 'orders/' + orderId + '/', {
      method: 'PATCH',
      body: JSON.stringify({
        status: newOrderStatus
      })
    });
  
    if (response.ok) {
      const data = await response.json();
      return {
        success: true,
        data: data.status
      };
    }
  
    console.error('PATCH request failed:', response.status, await response.text());
    return {
      success: false
    };
  }
}

