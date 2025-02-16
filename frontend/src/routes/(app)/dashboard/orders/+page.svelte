<script>
	import Datatable from '$lib/components/Datatable.svelte';
</script>

<h1 class="h2 my-4">Pedidos</h1>
<Datatable
	editable={false}
	endpoint={'orders'}
	fields={['ID', 'Usuario', 'Contacto', 'Cantidad productos', 'Estado', 'Realización']}
/>
