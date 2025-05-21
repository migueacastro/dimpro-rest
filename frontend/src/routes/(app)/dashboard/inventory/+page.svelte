<script>
	import { checkPermission } from '$lib/auth';
	import Datatable from '$lib/components/Datatable.svelte';
	export let data;
	let { products, user } = data;

</script>

<div class="flex items-center gap-4 my-4">
	<h1 class="h2">Inventario</h1>
	{#if checkPermission(user, 'view_export_order')}
		<form action="inventory/exportpdf" method="post">
			<button class="btn variant-filled max-w-fit px-6 h-full" type="submit">
				<i class="fa-solid fa-download"></i>
			</button>
		</form>
	{/if}
</div>

<Datatable
	source_data={products}
	editable={false}
	endpoint={{ main: 'products' }}
	fields={['id', 'reference', 'item', 'available_quantity']}
	headings={['ID', 'Referencia', 'item', 'Cantidad Disponible']}
/>
