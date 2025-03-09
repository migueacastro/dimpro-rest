<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
	import { onMount } from 'svelte';
	import { user } from '../../../../stores/stores';
	import { goto } from '$app/navigation';
	import { authenticate } from '$lib/auth';

	let endpoint = {"main":"users","edit":"edit-user","add":"create-user"};
	onMount(async () => {
		await authenticate();
		let isStaffOrAdmin = false;
		$user['groups'].forEach((group: any) => {
			if (group['name'] === 'staff' || group['name'] === 'admin') {
				isStaffOrAdmin = true;
			}
		});
		if (!isStaffOrAdmin) {
			goto('/dashboard');
		}
	});
</script>

<h1 class="h2 my-4">Vendedores</h1>
<Datatable
	editable={true}
	endpoint={endpoint}
	table_name={'vendedor'}
	fields={['name', 'email', 'phonenumber']}
	headings={['Nombre', 'Email', 'Teléfono']}
/>
