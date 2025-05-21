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
	import { checkPermission } from '$lib/auth';
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
	export let model_name = '';
	export let user: any = null;

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
		// so, after the form.requestSubmit() which is different than form.submit() because form.submit() submits the form as the server, and form.requestSubmit() submits the form as an user. form.submit()

		// so, this is an enhance function, triggered by the form submission as an user so in every form enhance function
		// you want to return this. result is the object returned by the action, like this
		return async ({ update, result }: any) => {
			if (result.data.success) {
				// this is how you verify it was a successful submission
				const t: ToastSettings = {
					message: `El ${table_name} se eliminó con exito.`,
					background: 'variant-ghost-success',
					timeout: 7000
				};
				toastStore.trigger(t); // and then trigger whatever function you want
			} else {
				const toast: ToastSettings = {
					message: `¡ERROR! El ${table_name} no se pudo eliminar.
							\nmensaje:${result.data.error}`,
					background: 'variant-ghost-error',
					timeout: 7000
				};
				toastStore.trigger(toast); // just an else, in case there was an error
			}
			setTimeout(() => {
				window.location.reload();
			},1000);
		};

		// kinda get it so far? if any you can base your own on this (copy and adapt xd) you don't have to understand it fully, but atleast now that

		/*     */
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

	onMount(async () => {
		loaded = false;
		loading = true;

		handler = new DataHandler(source_data, { rowsPerPage: 5 }); // Now it always use source_data

		rows = handler.getRows();
		setTimeout(() => {
			loaded = true;
			loading = false;
		}, 200);
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
				<tr on:click={() => {if(!editable){goto('/dashboard/' + endpoint['main']+`/${row['id']}`)}}}>
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
							{#if user && model_name && checkPermission(user, 'delete_'+model_name)}
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
							{#if user && model_name && checkPermission(user, 'change_'+model_name)}
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
