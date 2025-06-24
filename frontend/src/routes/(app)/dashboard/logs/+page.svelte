<script lang="ts">
	import PaginationDatatable from '$lib/components/pagination/PaginationDatatable.svelte';
	export let data;
</script>

<h1 class="h2 my-4">Registros</h1>
<PaginationDatatable
	handler={data.handler}
	editable={false}
	endpoint={{main:'logs'}}
	not_system_toggle={true}
	filter_headings={['actor_id', 'actor_name', 'actor_email', 'changes_text', 'content_type_model', 'remote_addr', 'timestamp__date']}
	order_headings={['actor_id', 'actor__name', 'actor__email', 'changes_text', 'content_type__model', 'remote_addr', 'timestamp']}
	fields={['actor','actor_name','actor_email', 'changes_text','content_type_name','remote_addr', 'timestamp']}
	headings={['ID Autor', 'Nombre de Autor', 'Email de Autor', 'Acción','Cambios','Dirección IP', 'Tiempo de modificación']}
/>
