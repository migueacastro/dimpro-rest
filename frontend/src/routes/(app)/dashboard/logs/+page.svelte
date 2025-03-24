<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
	import { onMount } from 'svelte';
	import { user } from '../../../../stores/stores';
	import { goto } from '$app/navigation';
	import { authenticate } from '$lib/auth';

	onMount(async () => {
		await authenticate();
		let isAdmin = false;
		$user['groups'].forEach((group: any) => {
			if (group.name === 'admin') {
				isAdmin = true;
			}
		});
		if (!isAdmin) {
			goto('/dashboard');
		}
	});
</script>

<h1 class="h2 my-4">Registros</h1>
<Datatable
	editable={false}
	endpoint={{main:'logs'}}
	fields={['object_repr', 'changes_text','remote_addr', 'timestamp']}
	headings={['Autor', 'Cambios','Dirección IP', 'Tiempo de modificación']}
/>
