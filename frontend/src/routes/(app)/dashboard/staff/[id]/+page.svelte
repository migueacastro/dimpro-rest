<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	export let data: any;
	let {user} = data;
	let {reqUser} = data;
	let staff: any = reqUser;
	$: loaded = true;

</script>

<div class="flex flex-col">
	{#if loaded}
		<div class="flex flex-col lg:flex-row">
			<div class="card p-[3rem] w-full mb-[2rem] mr-[2rem]">
				<div class="flex flex-col">
					<h4 class="h2 font-bold capitalize my-2">{staff?.name ?? 'No definido'}</h4>
					<h4 class="h4 capitalize my-2">Email: {staff?.email ?? 'No definido'}</h4>
					<h4 class="h4 capitalize my-2">Teléfono: {staff?.phonenumber ?? 'No definido'}</h4>
					<h4 class="h4 capitalize my-2">Cédula: {staff?.card_id ?? 'No definido'}</h4>
					<h4 class="h4 capitalize my-2">Dirección: {(String(user?.address)?.length > 0 && user?.address?.length) ? user?.address : 'No definida'}</h4>
				</div>
			</div>
			<div class="card p-[3rem] w-full mb-[2rem]">
				<div class="flex flex-col">
					<h4 class="h5 font-bold capitalize my-2">Empleado</h4>
					<h4 class="h4 my-2">Se unió en: {staff?.date_joined_format}</h4>
					<h4 class="h4 my-2">Último inicio de sesión: {staff?.last_login_format}</h4>
				</div>
			</div>
		</div>
		<div class="flex flex-row justify-between mb-[2rem]">
			<h2 class="h2">Pedidos: {staff?.orders?.length}</h2>
		</div>
		<Datatable
			endpoint={{ main: 'orders' }}
			source_data={staff?.orders}
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
