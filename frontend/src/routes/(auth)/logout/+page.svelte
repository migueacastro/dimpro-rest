<script lang="ts">
	import { goto } from '$app/navigation';
	import { authenticate, fetchLogout } from '$lib/auth';
	import { user } from '../../../stores/stores';
	import Cookies from 'js-cookie';
	import { onMount } from 'svelte';

	onMount(async () => {
		await fetchLogout();
		await authenticate();
		goto('/');
	});
</script>

