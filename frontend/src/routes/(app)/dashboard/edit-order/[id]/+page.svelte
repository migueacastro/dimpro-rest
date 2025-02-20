<script lang="ts">
	import { checkAdminGroup } from '$lib/auth';
	import { onMount } from 'svelte';
	import { user } from '../../../../../stores/stores';
	import { fetchData } from '$lib/utils.ts';
	import { Autocomplete } from '@skeletonlabs/skeleton';
	import { popup } from '@skeletonlabs/skeleton';
	import type { AutocompleteOption, PopupSettings } from '@skeletonlabs/skeleton';

	let products: any = [{}];
	let contacts: any = [{}];
	let productBlacklist: any = [];
	let productAutoCompleteList: AutocompleteOption[];
	let contactAutoCompleteList: AutocompleteOption[];
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
			search_error: false,
			input_disabled: true
		}
	];

	function addProductToBlacklist(id: any) {
		let product = products.find((product: any) => product.id == id);
		productBlacklist = [...productBlacklist, product];
		productAutoCompleteList = productAutoCompleteList.filter((p: any) => {
			return p.value != product.id;
		});
	}

	function removeProductFromBlacklist(id: any) {
		let product = productBlacklist.find((product: any) => product.id == id);
		productBlacklist = products.filter((p: any) => p.id != product.id);
		productAutoCompleteList = [
			...productAutoCompleteList,
			{ label: product.item, value: product.id }
		];
	}

	function unloadRowItemValues(row: any) {
		row.id = null;
		row.availability = null;
		row.price = null;
		row.cost = 0;
		row.quantity = '';
		if (row.item) {
			removeProductFromBlacklist(row.item);
		}
		row.input_disabled = true;
		row.item = null;
	}
	function loadRowItemValues(row: any, id: any) {
		let item_object = products.find((product: any) => product.id == id);

		if (item_object) {
			// Actualizar las propiedades del objeto original
			row.id = item_object.id;
			row.availability = item_object.available_quantity;
			row.item = item_object.id;
			row.item_label = item_object.item;
			row.price = Object.values(item_object.prices[0])[0];
			row.quantity = 1;
			row.input_disabled = false;

			calculateCost(row);
			addProductToBlacklist(row.item);
		} else {
		}
	}

	function addRow() {
		// carefull here, reactiviy works this way
		let index;
		if (items.length > 0) {
			index = items[items.length - 1].index + 1;
		} else {
			index = 0;
		}

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
			search_error: false,
			input_disabled: true
		};
		items = [...items, newRow]; // Here the array value is changed to another array with different  content
	}

	function removeRow(index: number) {
		items = items.filter((item: any) => item.index !== index);
		updateIndex();
	}

	function calculateCost(row: any) {
		let item_object = products.find((product: any) => product.id === row.item);
		if (row.quantity < 1) {
			row.quantity = 1;
			calculateCost(row);
			return;
		} else if (item_object && row.quantity > item_object?.available_quantity) {
			row.quantity = item_object?.available_quantity;
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
		if (listAutocompleteOptions(row.item_label).length < 1 && !row.item) {
			return true;
		}
		return false;
	}

	function listAutocompleteOptions(input: string) {
		let list = productAutoCompleteList.filter((item: any) => {
			if (item.label.toLowerCase().trim().includes(input.toLowerCase().trim())) {
				return item;
			}
		});
		return list;
	}

	function findItemByName(row: any) {
		return productAutoCompleteList.find(
			(p: any) => p.label?.toLowerCase()?.trim() == row.item_label?.toLowerCase()?.trim()
		);
	}

	function markSearchError(row: any) {
		row.search_error = true;
	}

	function unmarkSearchError(row: any) {
		row.search_error = false;
	}

	function handleItemInput(row: any) {
		if (checkErrors(row)) {
			markSearchError(row);
			unloadRowItemValues(row);
		} else {
			unmarkSearchError(row);
			let item = findItemByName(row);
			if (item) {
				loadRowItemValues(row, item?.value);
			} else {
				unloadRowItemValues(row);
			}
		}
	}

	function clearItemInput(row: any) {
		row.item = null;
		row.item_label = '';
		unloadRowItemValues(row);
		items = items;
	}

	function handleItemInputBlur(row: any) {
		if (checkErrors(row)) {
			clearItemInput(row);
			unmarkSearchError(row);
		}
	}

	function handleItemEnterPress(row: any, event: any) {
		if (event.key === 'Enter') {
			row.item_label = listAutocompleteOptions(row.item_label)[0].label;
			items = items;
			handleItemInput(row);
		}
	}

	onMount(async () => {
		let response = await fetchData('products', 'GET');
		products = await response.json();
		productAutoCompleteList = products.map((product: any) => {
			return { label: product.item, value: product.id };
		});
		response = await fetchData('contacts', 'GET');
		contacts = await response.json();
	});
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
			{#each items as row, index}
				<tr>
					<td>{row.id || ''}</td>
					<td>
						<div class="input-group input-group-divider grid-cols-[1fr_auto] p-0">
							<input
								class="input autocomplete"
								class:input-error={row.search_error}
								type="search"
								name="autocomplete-search"
								bind:value={row.item_label}
								placeholder="Buscar..."
								use:popup={{
									event: 'focus-click',
									target: `popupAutocomplete-${index}`,
									placement: 'bottom'
								}}
								on:input={() => handleItemInput(row)}
								on:blur={() => handleItemInputBlur(row)}
								on:keydown={(e) => handleItemEnterPress(row, e)}
							/>
							<button type="button" class="input-group-shim" on:click={() => clearItemInput(row)}>
								<i class="fa-solid fa-xmark"></i>
							</button>
						</div>
						<div data-popup={`popupAutocomplete-${row?.index}`} class="max-w-md w-full card">
							<Autocomplete
								bind:input={row.item_label}
								options={productAutoCompleteList}
								on:selection={(e) => {
									row.item_label = e.detail.label;
									row.item = e.detail.value;
									loadRowItemValues(row, e.detail.value);
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
							disabled={row.input_disabled}
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
