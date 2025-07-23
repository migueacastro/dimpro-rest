<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
	export let data;
	let {user} = data;
	let {users} = data;
	let endpoint = {"main":"staff","edit":"edit-staff","add":"create-staff"};
</script>

<h1 class="h2 my-4">Empleados/Administradores</h1>
<Datatable
	editable={true}
	endpoint={endpoint}
	source_data={users}
	table_name={'empleado/administrador'}
	fields={['name', 'email', 'card_id','phonenumber']}
	headings={['Nombre', 'Email', 'Cédula','Teléfono']}
	model_name={'staff_user'}
	user={user}
/>
