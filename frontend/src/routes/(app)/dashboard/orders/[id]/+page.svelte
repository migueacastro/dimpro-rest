<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
	import { goto } from '$app/navigation';
	import StatusButton from '$lib/components/StatusButton.svelte';
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import { checkPermission, checkStaffGroup } from '$lib/auth';
	export let data: any;
	let order = data.order;
	let products: Array<any> = order?.products.map((item: any) => {
		return {
			id: item.product.id,
			item: item.product.item,
			reference: item.product.reference,
			quantity: item.quantity,
			price: item.price,
			cost: item.cost
		};
	});
	let loaded = true;
	async function downloadPDF() {
		const response = await fetch(
			'/dashboard/orders/exportpdf?order_id='+order?.id,
			{
				method: 'GET',
			}
		);
		if (response.ok) {
			const blob = await response.blob();
			const url = URL.createObjectURL(blob);
			window.open(url, '_blank');
			setTimeout(() => URL.revokeObjectURL(url), 10000);
		} else {
			console.log('Error al exportar PDF');
		}
	}
</script>

<div class="flex flex-col">
	{#if loaded}
		<div class="flex flex-col lg:flex-row">
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
						<a class="text-primary-500" href={`/dashboard/${checkStaffGroup(order?.user)?"staff":"users"}/` + order?.user?.id}
							>Email: {order?.user?.email}</a
						>
					</h4>
				</div>
			</div>
		</div>
		<div class="flex flex-row flex-wrap justify-between mb-[2rem]">
			<h2 class="h2 lg:my-0 my-2">Items: {order?.products?.length}</h2>
			<div class="flex flex-row">
				{#if checkPermission(data.user, 'change_status_order')}
					<StatusButton {order} />
				{/if}

				{#if checkPermission(data.user, 'change_order')}
				<button
					class="btn variant-filled max-w-fit px-[2rem] mx-2"
					on:click={() => goto('/dashboard/edit-order/' + order?.id)}
				>
					<i class="fa-solid fa-pen-to-square"></i>
				</button>
				{/if}
				{#if checkPermission(data.user, 'view_export_order')}
					<button class="btn variant-filled max-w-fit px-[2rem] ml-2 h-full" type="button" on:click={downloadPDF}>
						<i class="fa-solid fa-download"></i>
					</button>
				{/if}
			</div>
		</div>
		<Datatable
			source_data={products}
			headings={['ID', 'Item', 'Referencia', 'Cantidad', 'Precio', 'Costo']}
			fields={['id', 'item', 'reference', 'quantity', 'price', 'cost']}
		/>
	{:else}
		<div class="flex justify-center mt-[8rem]">
			<div class="my-auto">
				<ProgressRadial />
			</div>
		</div>
	{/if}
</div>
