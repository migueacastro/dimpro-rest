import { apiURL } from "$lib/api_url.js";
import type { RequestHandler } from "@sveltejs/kit";

export const POST: RequestHandler = async ({ fetch }) => {
    const response = await fetch(apiURL + 'export_inventory_pdf', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
    });

    if (response.ok) {
        const pdfBlob = await response.blob();


        return new Response(pdfBlob, {
            headers: {
                "Content-Type": "application/pdf",
                "Content-Disposition": `attachment; filename="inventory_${Date.now().toString()}.pdf"`,
            },
        });
    } else {
        const errorText = await response.text();
        return new Response(errorText, { status: response.status });
    }
};