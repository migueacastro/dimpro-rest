<script lang="ts">
	import '../app.postcss';
	// Floating UI for Popups
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';
	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });
	import { authenticate } from '$lib/auth';
	import { user } from '../stores/stores';
	import { onMount } from 'svelte';

	onMount(async () => {
		let userData = await authenticate();
		user.set(userData);
	});
</script>
<slot></slot>