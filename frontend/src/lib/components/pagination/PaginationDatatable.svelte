<script lang="ts">
	//@ts-nocheck
	//Import local datatable components
	import { goto } from '$app/navigation';
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	//Load local data

	import { onMount } from 'svelte';
	import { apiURL } from '$lib/api_url';
	import {
		getModalStore,
		getToastStore,
		type ModalSettings,
		type ToastSettings
	} from '@skeletonlabs/skeleton';
	import { Result } from 'postcss';
	import { enhance } from '$app/forms';
	import { checkPermission } from '$lib/auth';
	//import { loading } from '../../stores/stores';

	const modalStore = getModalStore();
	const toastStore = getToastStore();
	//Init data handler - CLIENT

	export let endpoint: any = { main: null, edit: null, add: null };
	export let fields: any = [];
	export let editable: any = false;
	export let headings: any = [];
	export let table_name = '';
	export let model_name = '';
	export let user: any = null;

	$: loaded = true;
	$: loading = false;
	export let filter_headings: any = [];
	export let order_headings: any = [];
	// List to use inside each heading so that it can access the Title and the field name to access the object attribute
	let combinedHeadingsList = headings.map((heading: any, index: any) => {
		let newObject: any = { heading: heading, field: fields[index] };
		if (headings.length > 0) {
			newObject.filter = filter_headings[index];
			newObject.order = order_headings[index];
		}
		return newObject;
	});

	export let handler: any;

	let searchTerm = handler.search || '';
	$: handler.search = searchTerm;
	loading = false;

	import { page } from '$app/stores';
	import { get } from 'svelte/store';

	function buildQuery(parameter: string, newPage: number | string) {
		const currentPage = get(page);
		const params = new URLSearchParams(currentPage.url.search);
		params.set(parameter, newPage.toString());
		// The pathname is important to preserve the current location (for example, '/dashboard/logs')
		return currentPage.url.pathname + '?' + params.toString();
	}
	function buildQueryWithKeys(paramsToSet: Record<string, string | number>) {
		const currentPage = get(page);
		const params = new URLSearchParams(currentPage.url.search);
		for (const [key, value] of Object.entries(paramsToSet)) {
			if (value.toString() === '') {
				params.delete(key);
				continue;
			}
			params.set(key, value.toString());
		}
		return currentPage.url.pathname + '?' + params.toString();
	}

	function deleteResult() {
		return async ({ update, result }: any) => {
			if (result.data.success) {
				// this is how you verify it was a successful submission
				const t: ToastSettings = {
					message: `El ${table_name} se eliminó con exito.`,
					background: 'variant-ghost-success',
					timeout: 3500
				};
				toastStore.trigger(t); // and then trigger whatever function you want
			} else {
				const toast: ToastSettings = {
					message: `¡ERROR! El ${table_name} no se pudo eliminar.
							\nmensaje:${result.data.error}`,
					background: 'variant-ghost-error',
					timeout: 3500
				};
				toastStore.trigger(toast); // just an else, in case there was an error
			}
			setTimeout(() => {
				window.location.reload();
			}, 1000);
		};
	}
	function deleteConfirmation(name: any, id: any, event: any) {
		// that button will trigger the confirmation popup, if it has response. Then it will trigger the formSubmission with this little one
		const modal: ModalSettings = {
			type: 'confirm',
			title: `Eliminar: ${name}`,
			body: `¿Está seguro de querer eliminar este ${table_name}?`,
			response: async (r: boolean) => {
				if (r) {
					const form = event.target.closest('form');
					if (form) {
						form.requestSubmit();
					}
				}
			}
		};
		modalStore.trigger(modal);
	}
</script>

{#if loading}
	<div class="flex justify-center mt-[8rem]">
		<div class="my-auto">
			<ProgressRadial />
		</div>
	</div>
{/if}

<div class=" overflow-x-auto space-y-4" class:hidden={!loaded}>
	<!-- Header -->
	<header class="flex flex-row justify-between gap-4">
		<input
			class="input sm:w-64 w-36"
			type="search"
			placeholder="Buscar..."
			bind:value={searchTerm}
			on:input={() => {
				goto('?search=' + searchTerm + '&page_size=' + handler.pages.size + '&page=1', {
					keepFocus: true
				});
			}}
		/>
		<aside class="flex place-items-center">
			Mostrar
			<select
				class="select ml-2"
				bind:value={handler.pages.size}
				on:change={(e) => {
					goto(buildQueryWithKeys({ page_size: handler.pages.size, page: '' }));
				}}
			>
				{#each handler.pages.sizes as option}
					<option value={option}>
						{option}
					</option>
				{/each}
			</select>
		</aside>
	</header>
	<!-- Table -->
	<table class="table table-hover table-compact w-full table-auto">
		<thead>
			<tr>
				{#each combinedHeadingsList as item}
					<th
						on:click={() => {
							console.log('Current ordering:', handler?.ordering); // Debug current state
							let filter = '';
							if (handler?.ordering === '-' + item.order) {
								filter = item.order;
							} else {
								filter = '-' + item.order;
							}
							console.log('New ordering:', filter); // Debug new value
							goto(buildQuery('ordering', filter));
						}}
						class="cursor-pointer select-none"
					>
						<div class="flex h-full items-center justify-start gap-x-2">
							{item?.heading}
							{#if handler.ordering}
								{#if handler.ordering.includes('-') === 'asc'}
									&darr;
								{:else}
									&uarr;
								{/if}
							{:else}
								&updownarrow;
							{/if}
						</div>
					</th>
				{/each}
				{#if editable}
					<th class="flex h-full items-center justify-start gap-x-2"> Acciones </th>
				{/if}
			</tr>

			<tr>
				{#each combinedHeadingsList as item}
					{#if item !== ''}
						<th>
							<input
								class="input text-sm w-full capitalize"
								type={item.field === 'timestamp' ? 'date' : 'text'}
								placeholder={'Filtrar ' + item?.heading}
								on:input={() => {
									goto(buildQuery(item.filter, event.target.value), { keepFocus: true });
								}}
							/>
						</th>
					{/if}
				{/each}
				{#if editable}
					<th>
						<p class="text-sm w-full capitalize">Acciones</p>
					</th>
				{/if}
			</tr>
		</thead>
		<tbody>
			{#each handler.results as row}
				<tr
					on:click={() => {
						if (!editable) {
							goto('/dashboard/' + endpoint['main'] + `/${row['id']}`);
						}
					}}
				>
					{#each fields as field}
						{#if row[field]}
							<td class="capitalize">{row[field]}</td>
						{:else}
							<td class="capitalize">No Definido</td>
						{/if}
					{/each}

					{#if editable}
						<td class="flex flex-row">
							<button
								class="btn mr-2 variant-filled"
								on:click={() => {
									setTimeout(() => {
										goto('/dashboard/' + endpoint['main'] + '/' + row['id']);
									}, 90);
								}}
							>
								<i class="fa-solid fa-info"></i>
							</button>
							{#if user && model_name && checkPermission(user, 'delete_' + model_name)}
								<form action="?/handleDelete" method="POST" use:enhance={deleteResult}>
									<input type="hidden" name="id" value={row['id']} />
									<button
										type="button"
										class="btn variant-filled"
										on:click={(e) => deleteConfirmation(row['name'], row['id'], e)}
									>
										<i class="fa-solid fa-trash"></i>
									</button>
								</form>
							{/if}
							{#if user && model_name && checkPermission(user, 'change_' + model_name)}
								<button
									class="btn ml-2 variant-filled"
									on:click={() => {
										setTimeout(() => {
											goto(
												'/dashboard/' + endpoint['main'] + '/' + `${endpoint['edit']}/` + row['id']
											);
										}, 90);
									}}
								>
									<i class="fa-solid fa-pencil"></i>
								</button>
							{/if}
						</td>
					{/if}
				</tr>
			{/each}
			<tr>
				{#each fields as field}
					<td class="capitalize">----</td>
				{/each}
				{#if editable && model_name && checkPermission(user, 'add_' + model_name)}
					<button
						class="btn variant-filled ml-[0.75rem]"
						on:click={() => goto('/dashboard/' + endpoint['main'] + '/' + `${endpoint['add']}`)}
					>
						<i class="fa-solid fa-plus"></i>
					</button>
				{/if}
			</tr>
		</tbody>
	</table>
	<!-- Footer -->
	<footer class="flex justify-between">
		<aside class="text-sm leading-8 mr-6">
			{#if handler.rowCount.total > 0}
				<b>{handler.rowCount.start}</b>
				- <b>{handler.rowCount.end}</b>
				/ <b>{handler.rowCount.total}</b>
			{:else}
				Sin registros
			{/if}
		</aside>

		<section
			class="btn-group variant-ghost-surface [&>*+*]:border-surface-500 h-10 hidden lg:flex flex-row"
		>
			<button
				on:click={() => goto(buildQuery('page', parseInt(handler.pages.current) - 1))}
				type="button"
				class="hover:variant-soft-primary"
				disabled={handler.pages.current == 1}
			>
				←
			</button>

			{#each handler.pages.list as page}
				<button
					on:click={() => goto(buildQuery('page', page))}
					class="hover:variant-soft-primary"
					class:variant-soft-secondary={handler.pages.current == page}
					class:ellipse={page == null}
				>
					{page ?? '...'}
				</button>
			{/each}
			<button
				on:click={() => goto(buildQuery('page', parseInt(handler.pages.current) + 1))}
				type="button"
				class="hover:variant-soft-primary"
				disabled={handler.pages.current == handler.pages.count}
			>
				→
			</button>
		</section>

		<!-- Mobile buttons -->
		<section class="lg:hidden overflow-x-scroll w-full">
			<button
				on:click={() => goto(buildQuery('page', parseInt(handler.pages.current) - 1))}
				type="button"
				class="btn variant-ghost-surface mr-2 mb-2 hover:variant-soft-primary"
				disabled={handler.pages.current == 1}
			>
				←
				{#each handler.pages.list as page}
					<button
						on:click={() => goto(buildQuery('page', page))}
						class="hover:variant-soft-primary px-2"
						class:variant-soft-secondary={handler.pages.current == page}
						class:ellipse={page == null}
					>
						{page ?? '...'}
					</button>
				{/each}
				<button
					on:click={() => goto(buildQuery('page', parseInt(handler.pages.current) + 1))}
					type="button"
					class="hover:variant-soft-primary"
					disabled={handler.pages.current == handler.pages.count}
				>
					→
				</button>
			</button>
		</section>
	</footer>
</div>
