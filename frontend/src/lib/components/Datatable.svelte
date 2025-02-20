<script lang="ts">
	// @ts-nocheck

	//Import local datatable components
	import ThSort from '$lib/components/ThSort.svelte';
	import ThFilter from '$lib/components/ThFilter.svelte';
	import Search from '$lib/components/Search.svelte';
	import RowsPerPage from '$lib/components/RowsPerPage.svelte';
	import RowCount from '$lib/components/RowCount.svelte';
	import Pagination from '$lib/components/Pagination.svelte';
	import { goto } from '$app/navigation';
	//Load local data
	import { fetchData } from '$lib/utils.ts';

	//Import handler from SSD
	import { DataHandler } from '@vincjo/datatables';
	import { onMount } from 'svelte';
	import { apiURL } from '$lib/api_url';

	//Init data handler - CLIENT
	let data = [{}];
	export let endpoint: any = null;
	export let fields: any = [];
	export let editable: any = false;
	export let source_data: any = null;
	export let headings: any = [];

	// List to use inside each heading so that it can access the Title and the field name to access the object attribute
	let combinedHeadingsList = headings.map((heading: any, index: any) => {
		return { heading: heading, field: fields[index] };
	});

	let handler = new DataHandler(data, { rowsPerPage: 5 });
	let rows = handler.getRows();

	onMount(async () => {
		if (endpoint) {
			let response = await fetchData(endpoint, 'GET');
			data = await response.json();
			handler = new DataHandler(data, { rowsPerPage: 5 });
		} else {
			handler = new DataHandler(source_data, { rowsPerPage: 5 });
		}
		rows = handler.getRows();
	});
</script>

<div class=" overflow-x-auto space-y-4">
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
				<tr on:click={() => goto('/dashboard/' + endpoint + '/' + row['id'])}>
					{#each fields as field}
						<td class="capitalize">{row[field]}</td>
					{/each}
					{#if editable}
						<td class="flex flex-row">
							<button class="btn variant-filled">
								<i class="fa-solid fa-trash"></i>
							</button>
							<button class="btn ml-2 variant-filled">
								<i class="fa-solid fa-plus"></i>
							</button>
						</td>
					{/if}
				</tr>
			{/each}
		</tbody>
	</table>
	<!-- Footer -->
	<footer class="flex justify-between">
		<RowCount {handler} />
		<Pagination {handler} />
	</footer>
</div>
