<script>
	import Datatable from '$lib/components/Datatable.svelte';
</script>

<h1 class="h2 my-4">Pedidos</h1>
<Datatable
	editable={false}
	endpoint={{main:'orders'}}
	headings={['ID', 'Usuario', 'Contacto', 'Cantidad productos', 'Estado', 'Realización']}
	fields={['id', 'user_name', 'contact_name', 'product_count', 'status', 'date_format']}
/>
