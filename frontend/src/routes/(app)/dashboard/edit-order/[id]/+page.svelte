<script lang="ts">
	//@ts-nocheck
	import { checkAdminGroup } from '$lib/auth';
	import { onMount } from 'svelte';
	import { user } from '../../../../../stores/stores';
	import { fetchData } from '$lib/utils.ts';
	import { Autocomplete, getModalStore, getToastStore } from '@skeletonlabs/skeleton';
	import { popup } from '@skeletonlabs/skeleton';
	import { goto } from '$app/navigation';
	import type { AutocompleteOption, PopupSettings } from '@skeletonlabs/skeleton';

	export let data;
	let products: any = [];
	let contacts: any = [];
	let pricetypes: Array<any> = [];
	let productBlacklist: any = [];
	let productAutoCompleteList: AutocompleteOption[] = [];
	let selectedPricetypeId: any;
	let order: any = {};
	let initialItemsList: Array<any> = [];
	let toastStore = getToastStore();
	let modalStore = getModalStore();
	let inputContact: string = '';
	let selectedContactId: number;
	let contactAutoCompleteList: AutocompleteOption<number, string>[] = [];
	let popupSettings: PopupSettings = {
		event: 'focus-click',
		target: 'popupAutocomplete',
		placement: 'bottom'
	};

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
			input_disabled: true,
			hover: false,
			product_object: null
		}
	];

	$: totalQuantity = items
		.reduce((accumulator: number, item: any) => accumulator + (Number(item.quantity) || 0), 0)
		.toFixed(2);

	$: totalPrice = items
		.reduce((accumulator: number, item: any) => accumulator + (Number(item.price) || 0), 0)
		.toFixed(2);

	$: totalCost = items
		.reduce((accumulator: number, item: any) => accumulator + (Number(item?.cost) || 0), 0)
		.toFixed(2);

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
		row.cost = null;
		row.reference = '';
		row.quantity = '';
		if (row.item) {
			removeProductFromBlacklist(row.item);
		}
		row.input_disabled = true;
		row.item = null;
		row.product_object = null;
	}
	function loadRowItemValues(row: any, id: any) {
		let item_object = products.find((product: any) => product.id == id);

		if (item_object) {
			// Actualizar las propiedades del objeto original
			if (!row.id == id) {
				row.quantity = 1;
			}
			row.id = item_object.id;
			row.availability = item_object.available_quantity;
			row.item = item_object.id;
			row.item_label = item_object.item;
			let selectedPricetypeName = pricetypes.find(
				(pricetype: any) => pricetype.id === selectedPricetypeId
			).name;
			row.price = Object.values(
				item_object.prices.find(
					(pricetype: any) => Object.keys(pricetype)[0] === selectedPricetypeName
				)
			)[0];
			row.reference = item_object.reference;
			row.input_disabled = false;
			row.product_object = item_object;

			calculateCost(row);
			addProductToBlacklist(row.item);
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
			input_disabled: true,
			hover: false,
			product_object: null
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
			row.cost = parseFloat((row.quantity * row.price).toFixed(2));
		} else {
			row.cost = null;
		}
		items = items;
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

	function updateTablePrices() {
		items = items.map((row: any) => {
			if (row.item) {
				let itemId = row.item;
				loadRowItemValues(row, itemId);
			}
			return row;
		});
		items = [...items];
	}

	function loadItems(orderObject: any) {
		// Create a new array for items
		items = orderObject.products.map((product: any, index: any) => {
			const row = {
				id: product.product.id,
				item: product.product.id,
				reference: product.product.reference,
				quantity: product.quantity,
				availability: product.product.available_quantity,
				price: product.price,
				cost: product.cost,
				item_label: product.product.item,
				index: index,
				search_error: false,
				input_disabled: true,
				hover: false,
				product_object: null
			};
			// Load row values (e.g., price, cost) based on the selected pricetype

			return row;
		});
		initialItemsList = items;
		items.forEach((item: any) => {
			loadRowItemValues(item, item.id);
		});
		items = items;
	}

	async function disableInitialItems(orderObject: any) {
		let data: any;
		let response: any;
		for (const product of orderObject.products) {
			response = await fetchData('order_products', 'PATCH', {
				active: false
			}, product.id);
			if (!response.ok) {
				data = await response.json();
				console.log(data);
			}
		}
	}

	async function handleSave() {
		await disableInitialItems(order);
		order = {
			...order,
			//contact: selectedContactId
			total: totalCost,
			pricetype: selectedPricetypeId ?? pricetypes[0]?.id,
			user: order.user.id,
			contact: selectedContactId ?? order.contact.id
		};

		for (const row of items) {
			console.log(row.cost);
			let response = await fetchData('order_products', 'POST', {
				order: parseInt(data.id),
				product: row.item,
				price: row.price,
				quantity: row.quantity,
				cost: row.cost,
				active: true
			});
			if (!response.ok) {
				let data = await response.json();
				console.log(data);
			}
		}
		let response = await fetchData(`orders`, 'PATCH', order, data.id);
		if (response.ok) {
			const toast: ToastSettings = {
				message: 'El pedido se guardó con exito.',
				background: 'variant-ghost-success',
				timeout: 7000
			};
			toastStore.trigger(toast);
			console.log('Successfully saved');
			goto(`/dashboard/orders/${data.id}`);
		} else {
			let errorData = await response.json();
			const toast: ToastSettings = {
				message: `¡ERROR! El pedido no se pudo guardar.
							\nmensaje:${response.statusText}`,
				background: 'variant-ghost-error',
				timeout: 7000
			};
			toastStore.trigger(toast);
			console.log(errorData);
		}
	}
	async function handleDelete() {
		const modal: ModalSettings = {
			type: 'confirm',
			title: `Eliminar pedido`,
			body: `¿Está seguro de querer eliminar este pedido?`,
			response: async (r: boolean) => {
				if (r) {
					let response = await fetchData('orders/' + data.id, 'DELETE');
					if (response.ok) {
						const toast: ToastSettings = {
							message: `El pedido se eliminó con exito.`,
							background: 'variant-ghost-success',
							timeout: 7000
						};
						toastStore.trigger(toast);
					} else {
						const toast: ToastSettings = {
							message: `¡ERROR! El pedido no se pudo eliminar.
							\nmensaje:${response.statusText}`,
							background: 'variant-ghost-error',
							timeout: 7000
						};
						toastStore.trigger(toast);
					}
				}
				//goto('/dashboard/orders');
			}
		};
		modalStore.trigger(modal);
	}

	async function confirmation() {
		const modal: ModalSettings = {
			type: 'confirm',
			title: `Modificar Pedido`,
			body: `¿Está seguro de querer modificar este Pedido?`,
			response: async (r: boolean) => {
				if (r) {
					handleSave();
				}
				
			}
		};
		modalStore.trigger(modal);
	}

	onMount(async () => {
		let response = await fetchData('products', 'GET');
		products = await response.json();
		response = await fetchData('orders/' + data.id, 'GET');
		order = await response.json();
		response = await fetchData('orders', 'GET');
		let orders = await response.json();

		if (!order) {
			goto('/dashboard/orders');
		}
		response = await fetchData('contacts', 'GET');
		contacts = await response.json();
		response = await fetchData('pricetypes', 'GET');
		pricetypes = await response.json();
		selectedPricetypeId = order?.pricetype?.id ?? pricetypes[0]?.id;
		productAutoCompleteList = products.map((product: any) => {
			return { label: product.item, value: product.id };
		});
		contactAutoCompleteList = contacts.map((contact: any) => {
			return { label: contact.name, value: contact.id };
		});
		inputContact = contacts.find((contact: any) => contact.id == order?.contact)?.name;
		loadItems(order);
	});
</script>

<title>Editar Pedidos</title>

<h1 class="h2 my-4">
	Editar Pedido #{data.id}
</h1>

<div class="flex flex-row justify-between">
	<h3 class="h3 my-[2rem]">Items: {items.length}</h3>
	<div class="space-x-2 flex flex-row">
		<div class="flex flex-col w-1/2 max-w-md">
			<label for="select-contact" class="h4">Cliente</label>
			<input
				class="input autocomplete"
				type="search"
				name="autocomplete-search"
				bind:value={inputContact}
				placeholder="Buscar..."
				use:popup={popupSettings}
			/>
			<div data-popup="popupAutocomplete" class="max-w-md w-full card">
				<Autocomplete
					bind:input={inputContact}
					options={contactAutoCompleteList}
					on:selection={(e) => {
						inputContact = e.detail.label;
						selectedContactId = e.detail.value;
					}}
				/>
			</div>
		</div>
		<div class="flex flex-col">
			<label for="" class="h4">Tipo de precio</label>
			<select
				class="select"
				name="pricetype"
				id="pricetype"
				bind:value={selectedPricetypeId}
				on:change={updateTablePrices}
			>
				{#each pricetypes as pricetype}
					<option value={pricetype.id}>{pricetype.name}</option>
				{/each}
			</select>
		</div>
	</div>
</div>
<!-- Responsive Container (recommended) -->
<div class="table-container">
	<!-- Native Table Element -->
	<table class="table table-hover overflow-x-scroll">
		<thead>
			<tr>
				<th>ID</th>
				<th>Item</th>
				<th>Referencia</th>
				<th>Cantidad</th>
				<th>Disponibilidad</th>
				<th>Precio</th>
				<th>Costo</th>
				<th class="w-[10rem]"></th>
			</tr>
		</thead>
		<tbody>
			{#each items as row, index}
				<tr
					on:mouseover={() => (row.hover = true)}
					on:mouseout={() => (row.hover = false)}
					on:focus={() => {}}
					on:blur={() => {}}
				>
					<td>{row.id || ''}</td>
					<td>
						<div
							class="input-group input-group-divider grid-cols-[1fr_auto] p-0"
							class:variant-ghost-error={row.search_error}
						>
							<input
								class="input autocomplete"
								class:variant-ghost-error={row.search_error}
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
					<td class="hidden lg:flex flex-row">
						<button
							class:hidden={!row.hover}
							class="btn variant-ghost-error"
							on:click={() => removeRow(row.index)}
						>
							<i class="fa-solid fa-trash"></i>
						</button>
						<button class:hidden={!row.hover} class="btn ml-2 variant-filled" on:click={addRow}>
							<i class="fa-solid fa-plus"></i>
						</button>
					</td>
					<td class="flex lg:hidden flex-row">
						<button class="btn variant-ghost-error" on:click={() => removeRow(row.index)}>
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
				<td class="font-bold">{totalQuantity}</td>
				<td></td>
				<td class="font-bold">{totalPrice}</td>
				<td class="font-bold">{totalCost}</td>
				<td></td>
			</tr>
		</tfoot>
	</table>
</div>
<div>
	<div class="flex flex-row justify-center mt-[2rem]">
		<button class="btn ml-2 text-sm variant-filled" on:click={addRow}>
			<i class="fa-solid fa-plus"></i><span class="hidden lg:block ml-2">Añadir item</span>
		</button>
		<button class="btn ml-2 text-sm variant-filled" on:click={confirmation}>
			<i class="fa-solid fa-floppy-disk mr-2"></i> Guardar
		</button>
		<button class="btn ml-2 text-sm variant-ghost-error" on:click={handleDelete}>
			<i class="fa-solid fa-trash mr-2"></i> Eliminar Pedido
		</button>
	</div>
	<div class="flex justify-end flex-row">
		<h1 class="h2 mt-[2rem]">Total: {totalCost}$</h1>
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
