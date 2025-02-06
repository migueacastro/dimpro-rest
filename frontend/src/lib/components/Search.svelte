<script lang="ts">
	import type { DataHandler } from '@vincjo/datatables';
	export let handler: DataHandler;
	let value: string;
</script>

<input
	class="dark:variant-filled-surface variant-filled-tertiary rounded-xl border-0 mt-2 ml-2"
	type="search"
	placeholder="Buscar..."
	bind:value
	on:input={() => handler.search(value)}
/>
