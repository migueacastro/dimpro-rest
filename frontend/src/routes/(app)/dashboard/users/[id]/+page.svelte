<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { fetchUsers } from '../../../../../lib/auth';
	const userId = parseInt($page.params.id);
	let data = [{}];
	let user = { id: '', name: '', email: '' };
	onMount(async () => {
		const data = await fetchUsers();
		user = data.find((value: any) => value['id'] === userId);
	});
</script>

{#if user}
	<h1>{user['email']}</h1>
{:else}
	<h1>usuario inexistente</h1>
{/if}
