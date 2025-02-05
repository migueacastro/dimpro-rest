<script lang="ts">
	import type { DataHandler } from '@vincjo/datatables';
	export let handler: DataHandler;
	let value: string;
</script>

<input
	class="sm:w-64 w-36 bg-tertiary"
	type="search"
	placeholder="Buscar..."
	bind:value
	on:input={() => handler.search(value)}
/>
