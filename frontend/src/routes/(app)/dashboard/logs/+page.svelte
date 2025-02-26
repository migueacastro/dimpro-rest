<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
	import { onMount } from 'svelte';
	import { user } from '../../../../stores/stores';
	import { goto } from '$app/navigation';
	import { authenticate } from '$lib/auth';

	onMount(async () => {
		await authenticate();
		let isStaffOrAdmin = false;
		$user['groups'].forEach((group: any) => {
			if (!group['name'] === 'admin') {
				goto('/dashboard');
			}
		});
	});
</script>

<h1 class="h2 my-4">Registros</h1>
<Datatable
	editable={true}
	endpoint={'logs'}
	fields={['name', 'email', 'phonenumber']}
	headings={['Nombre', 'Email', 'Teléfono']}
/>
