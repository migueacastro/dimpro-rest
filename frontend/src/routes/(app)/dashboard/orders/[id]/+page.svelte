<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
	import { goto } from '$app/navigation';
	import StatusButton from '$lib/components/StatusButton.svelte';
	import { getToastStore, ProgressRadial } from '@skeletonlabs/skeleton';
	import { checkStaffGroup } from '$lib/auth';
	import { enhance } from '$app/forms';
	export let data: any;
	let order = data.order;
	const toastStore = getToastStore();

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

	async function handleExportPDFEnhance() {
		return async ({ result }: any) => {
			if (result.type === 'success') {
				// Extract the file from the response
				const file = result.data.file;

				// Create a Blob from the file
				const blob = new Blob([file], { type: 'application/pdf' });

				// Create a URL for the Blob
				const url = URL.createObjectURL(blob);

				// Create a temporary anchor element to trigger the download
				const a = document.createElement('a');
				a.href = url;
				a.download = `pedido_${Date.now()}.pdf`; // Set the filename
				document.body.appendChild(a);
				a.click();

				// Clean up
				document.body.removeChild(a);
				URL.revokeObjectURL(url);
			} else {
				console.error('Failed to download the file.');
			}
		};
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
						<a class="text-primary-500" href={'/dashboard/users/' + order?.user?.id}
							>Email: {order?.user?.email}</a
						>
					</h4>
				</div>
			</div>
		</div>
		<div class="flex flex-row flex-wrap justify-between mb-[2rem]">
			<h2 class="h2 lg:my-0 my-2">Items: {order?.products?.length}</h2>
			<div class="flex flex-row">
				{#if checkStaffGroup(data.user)}
					<StatusButton {order} />
				{/if}

				<button
					class="btn variant-filled max-w-fit px-[2rem] mx-2"
					on:click={() => goto('/dashboard/edit-order/' + order?.id)}
				>
					<i class="fa-solid fa-pen-to-square"></i>
				</button>
				<form action="/dashboard/orders/exportpdf" method="post">
					<input type="hidden" name="order_id" value={order?.id} />
					<button class="btn variant-filled max-w-fit px-[2rem] ml-2 h-full" type="submit">
						<i class="fa-solid fa-floppy-disk"></i>
					</button>
				</form>
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
