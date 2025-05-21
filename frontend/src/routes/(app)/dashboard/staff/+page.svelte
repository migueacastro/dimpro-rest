<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { checkAdminGroup } from '$lib/auth';
	export let data;
	let {user} = data;
	let {users} = data;
	let endpoint = {"main":"staff","edit":"edit-staff","add":"create-staff"};
	onMount(async () => {
		if (!checkAdminGroup(user)) {
			goto('/dashboard');
		}
	});
</script>

<h1 class="h2 my-4">Empleados/Administradores</h1>
<Datatable
	editable={true}
	endpoint={endpoint}
	source_data={users}
	table_name={'empleado/administrador'}
	fields={['name', 'email', 'phonenumber']}
	headings={['Nombre', 'Email', 'Teléfono']}
	model_name={'staff_user'}
	user={user}
/>
