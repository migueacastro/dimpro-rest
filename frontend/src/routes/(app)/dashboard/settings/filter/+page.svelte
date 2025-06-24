<script lang="ts">
	import { goto } from '$app/navigation';
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	export let data;
	let { users } = data;
	let date = '';
	let action = '';
	let selectedUser: any;
	let systemLogs = false;
    $: loaded = true;
	const search = () => {
        loaded = false;
		goto(
			`/dashboard/logs?timestamp__date=${date}&changes_text=${action}&not_system=${systemLogs}&actor_id=${selectedUser}`
		);
	};
</script>

{#if loaded}
<div class="lg:ml-[7rem]">
	<p class="h2 my-5">Indique la fecha que desea buscar</p>

	<input type="date" class="input  w-[15em]" bind:value={date} />

	<p class="h2 my-5">Indique la acción que desea buscar</p>

	<select class="input  w-[15em] capitalize" bind:value={action}>
		<option value="creación">creación</option>
		<option value="actualización">actualización</option>
		<option value="eliminación">eliminación</option>
		<option value="inicio / cierre de sesión">inicio de sesión</option>
	</select>
	<p class="h2 my-5">Indique el usuario que desea buscar</p>

	<select class="input  w-[15em] " bind:value={selectedUser}>
		<option value="" selected>Ninguno</option>
		{#each users as user}
			<option value={user?.id}>{user?.email}</option>
		{/each}
	</select>
	<div class="flex my-5 ">
		<input type="checkbox" class="w-[1em] mt-[2px] mr-[1rem] input" bind:checked={systemLogs} />
		<p>Excluir los registros del sistema</p>
	</div>
	<button on:click={search} class="mt-[2rem] btn variant-filled"
		><i class="fa-solid fa-magnifying-glass"></i></button
	>
	<footer class="p-4 text-center dark:text-gray-300 text-gray-900 text-sm">
		<p>Es posible dejar los campos vacios si no se desea incluir en la busqueda.</p>
	</footer>
</div>
{:else}
	<div class="flex justify-center mt-[8rem]">
		<div class="my-auto">
			<ProgressRadial />
		</div>
	</div>
{/if}
