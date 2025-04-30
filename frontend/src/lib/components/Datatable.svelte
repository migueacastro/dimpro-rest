<script lang="ts">
	//@ts-nocheck
	//Import local datatable components
	import { beforeNavigate } from '$app/navigation';
	import ThSort from '$lib/components/ThSort.svelte';
	import ThFilter from '$lib/components/ThFilter.svelte';
	import Search from '$lib/components/Search.svelte';
	import RowsPerPage from '$lib/components/RowsPerPage.svelte';
	import RowCount from '$lib/components/RowCount.svelte';
	import Pagination from '$lib/components/Pagination.svelte';
	import { goto } from '$app/navigation';
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	//Load local data

	//Import handler from SSD
	import { DataHandler } from '@vincjo/datatables';
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
	//import { loading } from '../../stores/stores';

	const modalStore = getModalStore();
	const toastStore = getToastStore();
	//Init data handler - CLIENT
	let data = [{}];
	export let endpoint: any = { main: null, edit: null, add: null };
	export let fields: any = [];
	export let editable: any = false;
	export let source_data: any = null;
	export let headings: any = [];
	export let table_name = '';

	$: loaded = false;
	$: loading = true;

	beforeNavigate(() => {
		setTimeout(() => {
			loaded = true;
			loading = false;
		}, 700);
	});

	// List to use inside each heading so that it can access the Title and the field name to access the object attribute
	let combinedHeadingsList = headings.map((heading: any, index: any) => {
		return { heading: heading, field: fields[index] };
	});

	let handler = new DataHandler(data, { rowsPerPage: 5 });
	let rows = handler.getRows();

	function deleteResult() {
		return async ({ update, result }: any) => {
			if (result.type == 'success') {
				const t: ToastSettings = {
					message: `El ${table_name} se eliminó con exito.`,
					background: 'variant-ghost-success',
					timeout: 7000
				};
				toastStore.trigger(t);
			} else {
				const toast: ToastSettings = {
					message: `¡ERROR! El ${table_name} no se pudo eliminar.
							\nmensaje:${response.statusText}`,
					background: 'variant-ghost-error',
					timeout: 7000
				};
				toastStore.trigger(toast);
			}
		};
	}
	function deleteConfirmation(name: any, id: any) {
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
				goto('/dashboard/' + endpoint['main']);
			}
		};
		modalStore.trigger(modal);
	}

	onMount(async () => {
		loaded = false;
		loading = true;
		
		handler = new DataHandler(source_data, { rowsPerPage: 5 });
		
		rows = handler.getRows();
		setTimeout(() => {
			loaded = true;
			loading = false;
		}, 1000);
	});
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
	<header class="flex justify-between gap-4">
		<Search {handler} />
		<RowsPerPage {handler} />
	</header>
	<!-- Table -->
	<table class="table table-hover table-compact w-full table-auto">
		<thead>
			<tr>
				{#each combinedHeadingsList as item}
					<ThSort {handler} orderBy={item?.field}>{item?.heading}</ThSort>
				{/each}
				{#if editable}
					<ThSort {handler} orderBy={fields[0]}>Acciones</ThSort>
				{/if}
			</tr>
			<tr>
				{#each fields as field}
					<ThFilter {handler} filterBy={field} />
				{/each}
				{#if editable}
					<ThFilter {handler} filterBy={fields[0]} />
				{/if}
			</tr>
		</thead>
		<tbody>
			{#each $rows as row}
				<tr
					on:click={() => {
						if (endpoint['secondary']) {
							goto('/dashboard/' + endpoint['secondary'] + '/' + row['id']);
						} else if (endpoint['main']) {
							goto('/dashboard/' + endpoint['main'] + '/' + row['id']);
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
							<form action="?/handleDelete" method="POST" use:enhance={deleteResult}>
								<input type="hidden" name="id" value={row['id']} />
								<button
									type="button"
									class="btn variant-filled"
									on:click={() => deleteConfirmation(row['name'], row['id'])}
								>
									<i class="fa-solid fa-trash"></i>
								</button>
							</form>
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
						</td>
					{/if}
				</tr>
			{/each}
			<tr>
				{#each fields as field}
					<td class="capitalize">----</td>
				{/each}
				{#if editable}
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
		<RowCount {handler} />
		<Pagination {handler} />
	</footer>
</div>
