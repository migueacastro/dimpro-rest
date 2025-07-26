import { apiURL } from "$lib/api_url.js";
import { checkPermission, permissionError } from "$lib/auth";
import type { RequestHandler } from "@sveltejs/kit";

export const GET: RequestHandler = async ({ fetch, locals }) => {
    if (!checkPermission(locals.user, "view_export_order")) {
        return permissionError();
    }
    const response = await fetch(apiURL + 'export_catalog_pdf', {
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
                "Content-Disposition": `attachment; filename="catalog_${Date.now().toString()}.pdf"`,
            },
        });
    } else {
        const errorText = await response.text();
        return new Response(errorText, { status: response.status });
    }
};