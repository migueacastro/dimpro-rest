<script>
	import Datatable from '$lib/components/Datatable.svelte';
</script>

<h1 class="h2 my-4">Inventario</h1>
<Datatable
	editable={false}
	endpoint={{main:'products'}}
	fields={['id', 'reference', 'item', 'available_quantity']}
	headings={['ID', 'Referencia', 'item', 'Cantidad Disponible']}
/>
