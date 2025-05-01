<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	export let data: any;
	$: loaded = false;
	let {user} = data;
	let {reqUser} = data;
	onMount(async () => {
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
					<h4 class="h2 font-bold capitalize my-2">{reqUser?.name ?? 'No definido'}</h4>
					<h4 class="h4 capitalize my-2">Email: {reqUser?.email ?? 'No definido'}</h4>
					<h4 class="h4 capitalize my-2">Teléfono: {reqUser?.phonenumber ?? 'No definido'}</h4>
				</div>
			</div>
			<div class="card p-[3rem] w-full mb-[2rem]">
				<div class="flex flex-col">
					<h4 class="h5 font-bold capitalize my-2">Vendedor</h4>
					<h4 class="h4 my-2">Se unió en: {reqUser?.date_joined_format}</h4>
					<h4 class="h4 my-2">Último inicio de sesión: {reqUser?.last_login_format}</h4>
				</div>
			</div>
		</div>
		<div class="flex flex-row justify-between mb-[2rem]">
			<h2 class="h2">Pedidos: {reqUser?.orders?.length}</h2>
		</div>
		<Datatable
			endpoint={{ secondary: 'orders' }}
			source_data={reqUser?.orders}
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
