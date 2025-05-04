import { apiURL } from "$lib/api_url.js";
import { changestatus } from "$lib/components/StatusButton.js";
import type { Actions } from "@sveltejs/kit";

export async function load({ params, fetch }) {
  const response = await fetch(apiURL + "orders/" + params.id);
  const order = await response.json();
  return {
    id: params.id,
    order,
  };
}

export const actions: Actions = {
  changestatus: changestatus,
  export_pdf: async ({fetch, request}: any) => {
    const formData = await request.formData();
    const orderId = formData.get('order_id') ?? '';
    const response = await fetch(apiURL+'export_order_pdf', {
      method: 'POST',
      body: JSON.stringify({
        order_id: orderId
      }),
    });

    if (response.ok) {
      // Get the PDF file as a Blob or Buffer
      const pdfBlob = await response

      // Return the PDF file as a response
      /*
      return new Response(pdfBlob, {
        headers: {
          'Content-Type': 'application/pdf',
          'Content-Disposition': `attachment; filename="pedido_${orderId}_${Date.now().toString()}.pdf"`,
        },
      });
        */
      return {
        success: true,
        file: pdfBlob,
      }

    } else {
      console.log(await response.text());
      return {
        success: false,
        error: "Error al imprimir archivo"
      };
    }
  }
};