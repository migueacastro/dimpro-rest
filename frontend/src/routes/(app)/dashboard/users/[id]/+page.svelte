<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	export let data: any;
	$: loaded = true;
	let {user} = data;
	let {reqUser} = data;
</script>

<div class="flex flex-col">
	{#if loaded}
		<div class="flex flex-col lg:flex-row">
			<div class="card p-[3rem] w-full mb-[2rem] mr-[2rem]">
				<div class="flex flex-col">
					<h4 class="h2 font-bold capitalize my-2">{reqUser?.name ?? 'No definido'}</h4>
					<h4 class="h4 capitalize my-2">Email: {reqUser?.email ?? 'No definido'}</h4>
					<h4 class="h4 capitalize my-2">Teléfono: {reqUser?.phonenumber ?? 'No definido'}</h4>
					<h4 class="h4 capitalize my-2">Cédula: {reqUser?.card_id ?? 'No definido'}</h4>
					<h4 class="h4 capitalize my-2">Dirección: {(String(user?.address)?.length > 0 && user?.address?.length) ? user?.address?.length : 'No definida'}</h4>
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
			endpoint={{ main: 'orders' }}
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
