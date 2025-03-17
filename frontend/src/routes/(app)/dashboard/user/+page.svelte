<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
	import { onMount } from 'svelte';
	import { fetchData } from '$lib/utils';
	import { goto } from '$app/navigation';
	import { authenticate } from '$lib/auth';
	import { user } from '../../../../stores/stores';

	onMount(async () => {
		await authenticate();
		console.log($user);
	});
</script>

<div class="flex flex-col">
	<h4 class="h2 font-bold capitalize my-4">Perfil</h4>
	<div class="flex flex-row">
		<div class="card p-[3rem] w-full mb-[2rem] mr-[2rem]">
			<div class="flex flex-col">
				<h4 class="h2 font-bold capitalize my-2">{$user?.name ?? 'No definido'}</h4>
				<h4 class="h4 capitalize my-2">Email: {$user?.email ?? 'No definido'}</h4>
				<h4 class="h4 capitalize my-2">Teléfono: {$user?.phonenumber ?? 'No definido'}</h4>
			</div>
		</div>
	</div>
</div>
