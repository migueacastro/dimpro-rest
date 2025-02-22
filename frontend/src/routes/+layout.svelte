<script lang="ts">
	import '../app.postcss';
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import { setInitialClassState, storePopup } from '@skeletonlabs/skeleton';
	import { authenticate } from '$lib/auth';
	import { loading,  user } from '../stores/stores';
	import { onMount } from 'svelte';
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import '@fortawesome/fontawesome-free/css/all.min.css';
	import { initializeStores } from '@skeletonlabs/skeleton';
	import { beforeNavigate } from '$app/navigation';

	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });

	initializeStores();
	$: loaded = false;

	beforeNavigate(() => {
		setTimeout(() => {
            loaded = true;
			loading.set(false);
		}, 700);
	});

	onMount(async () => {
        loaded = false;
        loading.set(true);
		let userData = await authenticate();
		user.set(userData);
		setTimeout(() => {
			loaded = true;
			loading.set(false);
		}, 1000);
	});
</script>

{#if $loading}
	<div class="flex justify-center mt-[15rem]">
		<div class="my-auto">
			<ProgressRadial />
		</div>
	</div>
{/if}

<div class="flex h-full w-full" class:hidden={!loaded}>
	<slot />
</div>

<style lang="postcss" global></style>
