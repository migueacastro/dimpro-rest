import { apiURL } from "$lib/api_url.js";
import type { RequestHandler } from "@sveltejs/kit";

export const GET: RequestHandler = async ({ request, fetch, locals, url  }) => {
  const order_id = url.searchParams.get('order_id');
  

  // Forward the request to the actual API
  const response = await fetch(apiURL+'export_order_pdf', {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ order_id }),
  });

  if (response.ok) {
    // Stream the PDF file back to the client
    const pdfBlob = await response.blob(); // here you transform your response into a blob, but you cant serialize that,
    //if you try to pass that in result, it would be lost


    return new Response(pdfBlob, { // instead, return a response, that mimics the fileResponse
      headers: {
        "Content-Type": "application/pdf",
        "Content-Disposition": `attachment; filename="pedido_${order_id}_${Date.now().toString()}.pdf"`,
      },
    });
  } else {
    const errorText = await response.text(); // also, response.text() gives you data about 500 internal server error
    return new Response(errorText, { status: response.status });
  }
};