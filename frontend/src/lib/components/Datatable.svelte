<script>
	// @ts-nocheck

	//Import local datatable components
	import ThSort from '$lib/components/ThSort.svelte';
	import ThFilter from '$lib/components/ThFilter.svelte';
	import Search from '$lib/components/Search.svelte';
	import RowsPerPage from '$lib/components/RowsPerPage.svelte';
	import RowCount from '$lib/components/RowCount.svelte';
	import Pagination from '$lib/components/Pagination.svelte';

	//Load local data
	import { getData } from '$lib/components/data.ts';

	//Import handler from SSD
	import { DataHandler } from '@vincjo/datatables';
	import { onMount } from 'svelte';

	//Init data handler - CLIENT
	let data = [{}];
	export let endpoint;
	export let fields;
	let handler = new DataHandler(data, { rowsPerPage: 5 });
	let rows = handler.getRows();

	onMount(async () => {
		data = await getData(endpoint);
		handler = new DataHandler(data, { rowsPerPage: 5 });
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
				{#each fields as field}
					<ThSort {handler} orderBy={field}>{field}</ThSort>
				{/each}
			</tr>
			<tr>
				{#each fields as field}
					<ThFilter {handler} filterBy={field} />
				{/each}
			</tr>
		</thead>
		<tbody>
			{#each $rows as row}
				<tr>
					{#each fields as field}
						<td>{row[field]}</td>
					{/each}
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
