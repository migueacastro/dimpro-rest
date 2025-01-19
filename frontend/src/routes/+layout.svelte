<script lang="ts">
	import '../app.postcss';
	// Floating UI for Popups
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';
	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });
	import { authenticate } from '$lib/auth';
	import { user } from '../stores/stores';
	import { onMount } from 'svelte';
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import '@fortawesome/fontawesome-free/css/all.min.css';
	import { autoModeWatcher } from '@skeletonlabs/skeleton';
	import { initializeStores } from '@skeletonlabs/skeleton';

	initializeStores();

	$: loaded = false;

	onMount(async () => {
		
		autoModeWatcher();
		let userData = await authenticate();
		user.set(userData);
		setTimeout(()=> loaded = true, 1000);
	});
</script>
{#if loaded}
	<slot/>
{:else}
	<div class="flex justify-center align-middle h-full">
		<div class="my-auto">
			<ProgressRadial />
		</div>
	</div>
{/if}

<style lang="postcss" global></style>