<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
	import { onMount } from 'svelte';
	import { fetchData } from '$lib/utils';
	import { goto } from '$app/navigation';
	import { authenticate } from '$lib/auth';
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	export let data: any;
	let user: any;
	$: loaded = false;
	onMount(async () => {
		await authenticate();
		let response = await fetchData('users/' + data.id, 'GET', null, data.id);
		user = await response.json();
		if (user['detail'] === 'No posee los permisos necesarios') {
			goto('/dashboard');
		}
		loaded = true;
	});
</script>

<div class="flex flex-col">
	{#if loaded}
		<div class="flex flex-col lg:flex-row">
			<div class="card p-[3rem] w-full mb-[2rem] mr-[2rem]">
				<div class="flex flex-col">
					<h4 class="h2 font-bold capitalize my-2">{user?.name ?? 'No definido'}</h4>
					<h4 class="h4 capitalize my-2">Email: {user?.email ?? 'No definido'}</h4>
					<h4 class="h4 capitalize my-2">Teléfono: {user?.phonenumber ?? 'No definido'}</h4>
				</div>
			</div>
			<div class="card p-[3rem] w-full mb-[2rem]">
				<div class="flex flex-col">
					<h4 class="h5 font-bold capitalize my-2">Vendedor</h4>
					<h4 class="h4 my-2">Se unió en: {user?.date_joined_format}</h4>
					<h4 class="h4 my-2">Último inicio de sesión: {user?.last_login_format}</h4>
				</div>
			</div>
		</div>
		<div class="flex flex-row justify-between mb-[2rem]">
			<h2 class="h2">Pedidos: {user?.orders?.length}</h2>
		</div>
		<Datatable
			endpoint={{ secondary: 'orders' }}
			source_data={user?.orders}
			headings={['ID', 'Contacto', 'Cantidad productos', 'Estado', 'Realización']}
			fields={['id', 'contact_name', 'product_count', 'status', 'date_format']}
		/>
	{:else}
		<div class="flex justify-center mt-[8rem]">
			<div class="my-auto">
				<ProgressRadial />
			</div>
		</div>
	{/if}
</div>
