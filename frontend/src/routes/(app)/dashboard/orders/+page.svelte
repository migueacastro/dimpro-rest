<script>
	import { checkStaffGroup } from '$lib/auth';
  import Datatable from '$lib/components/Datatable.svelte';
  import { user } from '../../../../stores/stores';
</script>

<h1 class="h2 my-4">{(checkStaffGroup($user)) ? "Pedidos" : "Mis Pedidos" }</h1>
<Datatable
	editable={false}
	endpoint={(checkStaffGroup($user)) ? {main:'orders'} : {main:'user_orders', secondary:'orders'}}
	headings={['ID', 'Usuario', 'Contacto', 'Cantidad productos', 'Estado', 'Realización']}
	fields={['id', 'user_name', 'contact_name', 'product_count', 'status', 'date_format']}
/>
