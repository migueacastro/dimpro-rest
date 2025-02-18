<script lang="ts">
	import { checkAdminGroup } from '$lib/auth';
	import { onMount } from 'svelte';
	import { user } from '../../../../../stores/stores';
	import { getData } from '$lib/utils.js';
	import { Autocomplete } from '@skeletonlabs/skeleton';
	import { popup } from '@skeletonlabs/skeleton';
	import type { PopupSettings } from '@skeletonlabs/skeleton';
	let popupSettings: PopupSettings = {
		event: 'focus-click',
		target: 'popupAutocomplete',
		placement: 'bottom'
	};

	let products: any = [{}];
	let contacts: any = [{}];
	let productBlacklist: any = [{}];

	let productAutoCompleteList: any = [{}];
	let contactAutoCompleteList: any = [{}];
	export let data;

	$: items = [
		{
			id: null,
			item: '',
			reference: '',
			quantity: null,
			availability: null,
			price: null,
			cost: null,
			item_label: '',
			index: 0,
			search_error: false
		}
	];

	function addProductToBlacklist(id: any) {
		let product = products.find((product: any) => product.id == id);
		productBlacklist = [...productBlacklist, product];
	}

	function removeProductFromBlacklist(id: any) {
		let product = productBlacklist.find((product: any) => product.id == id);
		products = products.filter((p: any) => p.id != product.id);
	}

	function unloadRowItemValues(row: any) {
		row.id = null;
		row.availability = null;
		row.price = null;
		row.cost = 0;
		row.quantity = 0;
		if (row.item) {
			removeProductFromBlacklist(row.item);
		}
		row.item = null;
		row.search_error = true;
	}
	function loadRowItemValues(row: any, id: any) {
		let item_object = products.find((product: any) => product.id === id);
		row.id = item_object.id;
		row.availability = item_object.available_quantity;
		row.item = item_object.id;
		row.item_label = item_object.item;
		row.price = Object.values(item_object.prices[0])[0];
		/*row.price =
				item_object.prices[0].key; */ /*product_object.prices.find((pricetype: any) => {
      pricetype.trim() === selectedPriceType.label;
    }*/
		row.quantity = 1;
		row.search_error = false;
		calculateCost(row);
		addProductToBlacklist(row.item);
	}

	function checkError(row: any) {}

	function addRow() {
		// carefull here, reactiviy works this way
		let index = items[items.length - 1].index + 1;
		let newRow: any = {
			id: null,
			item: '',
			reference: '',
			quantity: null,
			availability: null,
			price: null,
			cost: null,
			item_label: '',
			index: index,
			search_error: false
		};

		items = [...items, newRow]; // Here the array value is changed to another array with different  content
		//items.push(newRow); // You see? this just updates the content, not the value
	}

	function removeRow(index: number) {
		items = items.filter((item: any) => item.index !== index);
		updateIndex();
		//items.splice(index,1); // this would work well if instead of id, it would be the current index inside of the items array
	}

	function calculateCost(row: any) {
		if (row.quantity < 1) {
			row.quantity = 1;
			calculateCost(row);
			return;
		}
		if (row.quantity && row.price) {
			row.cost = (row.quantity * row.price).toFixed(2);
		} else {
			row.cost = null;
		}
	}

	function updateIndex() {
		items.forEach((item: any, index: any) => {
			item.index = index;
		});
	}

	function checkErrors(row: any) {
		if (listAutocompleteOptions(row.item_label).length < 1) {
			return true;
		}
		return false;
	}

	function listAutocompleteOptions(input: string) {
		return productAutoCompleteList.map((item: any) => {
			if (item.label.includes(input)) {
				return item;
			}
		});
	}

	function findItemByName(row: any) {
		return productAutoCompleteList.find((p: any) => p.item == row.item_label);
	}

	onMount(async () => {
		let response = await getData('products');
		products = await response.json();
		productAutoCompleteList = products.map((product: any) => {
			return { label: product.item, value: product.id };
		});
		response = await getData('contacts');
		contacts = await response.json();
	});
	// id does not depend on the table, it merely depends on the item
</script>

<title>Editar Pedidos</title>

<h1 class="h2 my-4">
	Editar Pedido #{data.id}
</h1>

<div class="flex flex-row justify-between">
	<h3 class="h3 my-[2rem]">Items: {items.length}</h3>
	<div class="flex flex-col">
		<label for="" class="h4 my-2">Tipo de precio</label>
		<select class="select" name="pricetype" id="pricetype"> </select>
	</div>
</div>
<!-- Responsive Container (recommended) -->
<div class="table-container">
	<!-- Native Table Element -->
	<table class="table table-hover">
		<thead>
			<tr>
				<th>ID</th>
				<th>Item</th>
				<th>Referencia</th>
				<th>Cantidad</th>
				<th>Disponibilidad</th>
				<th>Precio</th>
				<th>Costo</th>
				<th></th>
			</tr>
		</thead>
		<tbody>
			{#each items as row}
				<tr>
					<td>{row.id || ''}</td>
					<td>
						<input
							class="input autocomplete my-2"
							class:input-error={row.search_error}
							type="search"
							name="autocomplete-search"
							bind:value={row.item_label}
							placeholder="Buscar..."
							use:popup={popupSettings}
						/>
						<div data-popup="popupAutocomplete" class="max-w-md w-full card">
							<Autocomplete
								bind:input={row.item_label}
								options={productAutoCompleteList}
								on:selection={(e) => {
									row.item_label = e.detail.label;
									row.item = e.detail.value;
									loadRowItemValues(row, e.detail.value);
								}}
								}}
							/>
						</div>
					</td>
					<td>{row.reference || ''}</td>
					<td
						><input
							type="number"
							class="input"
							min="1"
							bind:value={row.quantity}
							on:input={() => calculateCost(row)}
						/></td
					>
					<td>{row.availability || ''}</td>
					<td>{row.price || ''}</td>
					<td>{row.cost || ''}</td>
					<td class="flex flex-row">
						<button class="btn variant-filled" on:click={() => removeRow(row.index)}>
							<i class="fa-solid fa-trash"></i>
						</button>
						<button class="btn ml-2 variant-filled" on:click={addRow}>
							<i class="fa-solid fa-plus"></i>
						</button>
					</td>
				</tr>
			{/each}
		</tbody>
		<tfoot>
			<tr>
				<th colspan="3">Totales</th>
				<td class="font-bold">45</td>
				<td></td>
				<td class="font-bold">6.5</td>
				<td class="font-bold">245.4</td>
				<td></td>
			</tr>
		</tfoot>
	</table>
	<div class="flex flex-row justify-center mt-[2rem]">
		<button class="btn ml-2 variant-filled" on:click={addRow}>
			<i class="fa-solid fa-plus mr-2"></i> Añadir item
		</button>
		<button class="btn ml-2 variant-filled" on:click={addRow}>
			<i class="fa-solid fa-floppy-disk mr-2"></i> Guardar
		</button>
		<button class="btn ml-2 variant-filled" on:click={addRow}>
			<i class="fa-solid fa-trash mr-2"></i> Eliminar Pedido
		</button>
	</div>
	<div class="flex justify-end flex-row">
		<h1 class="h2 mt-[2rem]">Total: 9.40$</h1>
	</div>
	<div class="card p-[2rem] mt-[2rem]">
		<h1 class="h3">Recordatorio</h1>
		<p class="p">Texto de ejemplo</p>
		{#if checkAdminGroup($user)}
			<button class="btn mt-[2rem] variant-filled" on:click={addRow}>
				<i class="fa-solid fa-floppy-disk"></i>
			</button>
		{/if}
	</div>
</div>
