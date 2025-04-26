<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
	import { onMount } from 'svelte';
	import { user } from '../../../../stores/stores';
	import { goto } from '$app/navigation';

	let endpoint = {"main":"staff","edit":"edit-staff","add":"create-staff"};
	onMount(async () => {
		let isAdmin = false;
		$user['groups'].forEach((group: any) => {
			if (group['name'] === 'admin') {
				isAdmin = true;
			}
		});
		if (!isAdmin) {
			goto('/dashboard');
		}
	});
</script>

<h1 class="h2 my-4">Empleados/Administradores</h1>
<Datatable
	editable={true}
	endpoint={endpoint}
	table_name={'empleado/administrador'}
	fields={['name', 'email', 'phonenumber']}
	headings={['Nombre', 'Email', 'Teléfono']}
/>
