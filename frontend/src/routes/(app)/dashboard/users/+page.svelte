<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { checkAdminGroup, checkStaffGroup } from '$lib/auth.js';

	export let data;
	let {user} = data;
	let {users} = data;
	let endpoint = {"main":"users","edit":"edit-user","add":"create-user"};
	onMount(async () => {
		if (!(checkStaffGroup(user) || checkAdminGroup(user))) {
			goto('/dashboard');
		}
	});
</script>

<h1 class="h2 my-4">Vendedores</h1>
<Datatable
	editable={true}
	endpoint={endpoint}
	source_data={users}
	table_name={'vendedor'}
	model_name={'user'}
	user={user}
	fields={['name', 'email', 'phonenumber']}
	headings={['Nombre', 'Email', 'Teléfono']}
/>
