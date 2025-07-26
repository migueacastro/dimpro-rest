<script>
	import { checkPermission } from '$lib/auth';
	import Datatable from '$lib/components/Datatable.svelte';
	export let data;
	let { products, user } = data;
	async function downloadPDF() {
		const response = await fetch('/dashboard/catalog/exportpdf', {
			method: 'GET'
		});
		if (response.ok) {
			const blob = await response.blob();
			const url = URL.createObjectURL(blob);
			window.open(url, '_blank');
			setTimeout(() => URL.revokeObjectURL(url), 10000);
		} else {
			console.log('Error al exportar PDF');
		}
	}
</script>

<div class="flex items-center gap-4 my-4">
	<h1 class="h2">Catálogo</h1>
	{#if checkPermission(user, 'view_export_order')}
		<button class="btn variant-filled max-w-fit px-6 h-full" type="button" on:click={downloadPDF}>
			<i class="fa-solid fa-download"></i>
		</button>
	{/if}
</div>

<Datatable
	source_data={products}
	editable={false}
	endpoint={{ main: 'products' }}
	fields={['id', 'reference', 'item', 'available_quantity']}
	headings={['ID', 'Referencia', 'item', 'Cantidad Disponible']}
/>
