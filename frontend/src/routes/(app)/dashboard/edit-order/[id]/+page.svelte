<script lang="ts">
	//@ts-nocheck
	import { checkAdminGroup, checkPermission, checkStaffGroup } from '$lib/auth';
	import { onMount } from 'svelte';
	import { enhance } from '$app/forms';
	import Reminder from '$lib/components/Reminder.svelte';
	import {
		Autocomplete,
		getModalStore,
		getToastStore,
		ProgressRadial
	} from '@skeletonlabs/skeleton';
	import { popup } from '@skeletonlabs/skeleton';
	import { goto } from '$app/navigation';
	import type { AutocompleteOption, PopupSettings } from '@skeletonlabs/skeleton';
	import StatusButton from '$lib/components/StatusButton.svelte';

	export let data;
	let orderForm, orderDeleteForm: HTMLFormElement;
	let user = data.user;
	let products: any = data.products ?? [];
	let contacts: any = data.contacts ?? [];
	let pricetypes: Array<any> = data.pricetypes ?? [];
	let productBlacklist: any = [];
	let productAutoCompleteList: AutocompleteOption[] = data.productAutoCompleteList ?? [];
	let selectedPricetypeId: any = data.selectedPricetypeId ?? pricetypes[0].id;
	let order: any = data.order ?? {};
	let toastStore = getToastStore();
	let modalStore = getModalStore();
	let inputContact: string = data.inputContact ?? '';
	let selectedContactId: number = data.selectedContactId ?? '';
	let contactAutoCompleteList: AutocompleteOption<number, string>[] =
		data.contactAutoCompleteList ?? [];
	let popupSettings: PopupSettings = {
		event: 'focus-click',
		target: 'popupAutocomplete',
		placement: 'bottom'
	};

	let items: Array<any> = data.items;

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
			)?.name ?? pricetypes[0]?.name;
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
		for (let item: any of items) {
			loadRowItemValues(item, item.id);
		}
	}

	async function handleSave() {
		loaded = false;
		return async ({ update, result }: any) => {
			let toast: ToastSettings;
			if (result?.type == 'success') {
				goto(`/dashboard/orders/${order.id}`);
				toast = {
					message: 'El pedido se guardó con exito.',
					background: 'variant-ghost-success',
					timeout: 3500
				};
				loaded = true;
				console.log('Successfully saved');
				toastStore.trigger(toast);
			} else {
				toast = {
					message: `¡ERROR! El pedido no se pudo guardar.
							\nmensaje:${result.data}`,
					background: 'variant-ghost-error',
					timeout: 3500
				};
				toastStore.trigger(toast);
			}
		};
	}

	async function confirmDelete() {
		const modal: ModalSettings = {
			type: 'confirm',
			title: `Eliminar pedido`,
			body: `¿Está seguro de querer eliminar este pedido?`,
			response: async (r: boolean) => {
				if (r) {
					orderDeleteForm.requestSubmit();
				}
			}
		};
		modalStore.trigger(modal);
	}

	async function handleDelete() {
		return async ({ update, result }: any) => {
			let toast: ToastSettings;
			if (result?.type == 'success') {
				toast = {
					message: 'El pedido se eliminó con exito.',
					background: 'variant-ghost-success',
					timeout: 3500
				};
				console.log('Successfully deleted');
				goto(`/dashboard/orders`);
				toastStore.trigger(toast);
			} else {
				toast = {
					message: `¡ERROR! El pedido no se pudo eliminar.
							\nmensaje:${result.data}`,
					background: 'variant-ghost-error',
					timeout: 3500
				};
				toastStore.trigger(toast);
			}
		};
	}

	async function confirmSave() {
		const modal: ModalSettings = {
			type: 'confirm',
			title: `Modificar Pedido`,
			body: `¿Está seguro de querer modificar este Pedido?`,
			response: async (r: boolean) => {
				if (r) {
					order = {
						...order,
						total: totalCost,
						pricetype: selectedPricetypeId ?? pricetypes[0]?.id,
						user: order.user.id,
						contact: selectedContactId ?? order.contact.id
					};
					orderForm.requestSubmit();
				}
			}
		};
		modalStore.trigger(modal);
	}
	$: loaded = false;
	onMount(async () => {
		loadItems(order);
		loaded = true;
	});

$: console.log(selectedContactId)
</script>

<title>Editar Pedidos</title>

{#if loaded}
	<h1 class="h2 my-4">
		Editar Pedido #{data.id}
	</h1>

	<div class="flex flex-col lg:flex-row justify-between mb-3">
		<h3 class="h3 mb-3 lg:mb-0 lg:my-[2rem] lg:w-full">Items: {items.length}</h3>
		<div class="lg:space-x-2 flex flex-col lg:flex-row lg:w-3/4">
			<div class="flex flex-col lg:w-1/2 w-full lg:max-w-md lg:my-0 my-2">
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
			<div class="flex flex-row space-x-2 w-full">
				<div class="flex flex-col w-full lg:my-0 mb-3">
					<label for="" class="h4">Tipo de precio</label>
					<select
						class="select w-full lg:max-w-md"
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
				{#if checkPermission(user, 'change_status_order')}
					<div class="flex flex-col w-fit lg:my-0 mb-2">
						<label for="select-contact" class="h4">Estatus</label>
						<StatusButton {order} />
					</div>
				{/if}
			</div>
		</div>
	</div>
	<!-- Responsive Container (recommended) -->
	<div class="table-container">
		<!-- Native Table Element -->
		<form action="?/save" bind:this={orderForm} method="post" use:enhance={handleSave}>
			<input type="hidden" name="order" value={JSON.stringify(order)} />
			<input type="hidden" name="items" value={JSON.stringify(items)} />
			<input type="hidden" name="pricetype" bind:value={selectedPricetypeId} />
			<input type="hidden" name="contact" bind:value={selectedContactId} />
			<input type="hidden" name="total" bind:value={totalCost} />
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
					{#if checkPermission(user, 'view_order_product')}
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
											disabled={!checkPermission(user, 'change_order_product')}
											class="input autocomplete"
											class:variant-ghost-error={row.search_error}
											type="search"
											autocomplete="off"
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
										<button
											type="button"
											class="input-group-shim"
											on:click={() => clearItemInput(row)}
										>
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
										disabled={row.input_disabled || !checkPermission(user, 'change_order_product')}
										bind:value={row.quantity}
										on:input={() => calculateCost(row)}
									/></td
								>
								<td>{row.availability || ''}</td>
								<td>{row.price || ''}</td>
								<td>{row.cost || ''}</td>
								<td class="hidden lg:flex flex-row">
									{#if checkPermission(user, 'delete_order_product')}
										<button
											type="button"
											class:hidden={!row.hover}
											class="btn variant-ghost-error"
											on:click={() => removeRow(row.index)}
										>
											<i class="fa-solid fa-trash"></i>
										</button>
									{/if}
									{#if checkPermission(user, 'add_order_product')}
										<button
											type="button"
											class:hidden={!row.hover}
											class="btn ml-2 variant-filled"
											on:click={addRow}
										>
											<i class="fa-solid fa-plus"></i>
										</button>
									{/if}
								</td>
								<td class="flex lg:hidden flex-row">
									{#if checkPermission(user, 'delete_order_product')}
										<button
											type="button"
											class="btn variant-ghost-error"
											on:click={() => removeRow(row.index)}
										>
											<i class="fa-solid fa-trash"></i>
										</button>
									{/if}
									{#if checkPermission(user, 'add_order_product')}
										<button type="button" class="btn ml-2 variant-filled" on:click={addRow}>
											<i class="fa-solid fa-plus"></i>
										</button>
									{/if}
								</td>
							</tr>
						{/each}
					{/if}
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
		</form>
	</div>
	<div>
		<div class="flex flex-row justify-center mt-[2rem]">
			<button class="btn ml-2 text-sm variant-filled" on:click={addRow}>
				<i class="fa-solid fa-plus"></i><span class="hidden lg:block ml-2">Añadir item</span>
			</button>
			<button class="btn ml-2 text-sm variant-filled" on:click={confirmSave}>
				<i class="fa-solid fa-floppy-disk mr-2"></i> Guardar
			</button>
			{#if checkPermission(user, 'delete_order')}
				<form
					action="?/delete"
					method="post"
					bind:this={orderDeleteForm}
					use:enhance={handleDelete}
				>
					<input type="hidden" name="id" value={data.id} />
					<button
						type="button"
						class="btn ml-2 text-sm variant-ghost-error"
						on:click={confirmDelete}
					>
						<i class="fa-solid fa-trash mr-2"></i> Eliminar Pedido
					</button>
				</form>
			{/if}
		</div>
		<div class="flex justify-end flex-row mb-[5rem]">
			<h1 class="h2 mt-[2rem]">Total: {totalCost}$</h1>
		</div>
		{#if checkPermission(user, 'view_note')}
		<Reminder {user} reminders={data.reminders} />
		{/if}
	</div>
{:else}
	<div class="flex justify-center mt-[8rem]">
		<div class="my-auto">
			<ProgressRadial />
		</div>
	</div>
{/if}
