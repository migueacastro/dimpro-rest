<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
	import { getData } from '$lib/utils';
	import { onMount } from 'svelte';
	export let data;
	import { goto } from '$app/navigation';
	let order: any;

	onMount(async () => {
		let response = await getData('orders/' + data.id);
		order = await response.json();
	});
</script>

<div class="flex flex-col">
	<div class="flex flex-row">
		<div class="card p-[3rem] w-full mb-[2rem]">
			<div class="flex flex-col">
				<h1 class="h1 mb-[3rem] font-bold">Pedido #{order?.id}</h1>
				<h4 class="h4 capitalize my-2">Cliente: {order?.contact_name}</h4>
				<h4 class="h4 capitalize my-2">Vendedor: {order?.user_name}</h4>
				<h4 class="h4 capitalize my-2">Items: {order?.products?.length}</h4>
				<h4 class="h4 capitalize my-2">Tipo de precio: {order?.pricetype?.name}</h4>
				<h4 class="h4 capitalize my-2">Total: {order?.total}$</h4>
				<h4 class="h4 capitalize my-2">Fecha: {order?.date_format}</h4>
				<h4 class="h4 my-2">
					<a class="text-primary-500" href={'/dashboard/users/' + order?.user?.id}
						>Email: {order?.user?.email}</a
					>
				</h4>
			</div>
		</div>
	</div>
	<div class="flex flex-row justify-between mb-[2rem]">
		<h2 class="h2">Items: {order?.products?.length}</h2>
		<div class="flex flex-row">
			<button
				class="capitalize btn variant-filled max-w-fit px-[2rem] mx-2"
				on:click={() => createOrder()}
			>
				{order?.status}
			</button>

			<button
				class="btn variant-filled max-w-fit px-[2rem] mx-2"
				on:click={() => goto('/dashboard/edit-order/' + order?.id)}
			>
				<i class="fa-solid fa-pen-to-square"></i>
			</button>
			<button class="btn variant-filled max-w-fit px-[2rem] ml-2" on:click={() => createOrder()}>
				<i class="fa-solid fa-floppy-disk"></i>
			</button>
		</div>
	</div>
	<Datatable
		use_array={true}
		source_data={order?.products}
		fields={['id', 'item', 'reference', 'quantity', 'price', 'cost']}
	/>
</div>
