<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { checkAdminGroup } from '$lib/auth';
	export let data;
	let {user} = data;

	onMount(() => {
		if (!checkAdminGroup(user)) {
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
