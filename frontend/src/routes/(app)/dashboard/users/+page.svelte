<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
	export let data;
	let {user} = data;
	let {users} = data;
	let endpoint = {"main":"users","edit":"edit-user","add":"create-user"};
</script>

<h1 class="h2 my-4">Vendedores</h1>
<Datatable
	editable={true}
	endpoint={endpoint}
	source_data={users}
	table_name={'vendedor'}
	model_name={'user'}
	user={user}
	fields={['name', 'email', 'card_id','phonenumber']}
	headings={['Nombre', 'Email', 'Cédula','Teléfono']}
/>
