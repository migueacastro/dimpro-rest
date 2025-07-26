export function transformInvoices(invoices: any) {
    let result: {[key: string]: any[]} = {};
    
    invoices.forEach((invoice: any) => {
        const date = new Date(invoice.date);
        const year = date.getFullYear().toString();
        const total = parseFloat(invoice.total);
        
        if (!result[year]) {
            result[year] = [];
        }
        
        result[year].push({
            ...invoice, // Include all original invoice properties
            date: invoice.date.split('T')[0], // Format date as YYYY-MM-DD
            value: total, // Add value field
            group: 'Total Facturado' // Add group field
        });
    });
    
    // Sort invoices within each year by date
    for (const year in result) {
        result[year].sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
    }
    
    return result;
}
