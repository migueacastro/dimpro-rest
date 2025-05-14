<script lang="ts">
	import { goto } from '$app/navigation';
export let data;
let {users} = data;
	let date = '';
	let action = '';
    let selectedUser:any;
    let systemLogs = false;
	const search = () => {
		goto(`/dashboard/logs?date=${date}&action=${action}&systemLogs=${systemLogs}&user=${selectedUser}`);
	};
</script>


<p class="h2 my-5">Indique la fecha que desea buscar</p>

	<input type="date" class="input ml-[5rem] w-[15em]" bind:value={date} />

<p class="h2 my-5">Indique la acción que desea buscar</p>

	<select class="input ml-[5rem] w-[15em]" bind:value={action}>
        <option value="creación">creación</option>
        <option value="actualización">actualización</option>
        <option value="eliminación">eliminación</option>
        <option value="pet">inicio/cierre de sesión</option>
        </select
	>
    <p class="h2 my-5">Indique el usuario que desea buscar</p>

	<select class="input ml-[5rem] w-[15em]" bind:value={selectedUser}>
        <option value="" selected>Ninguno</option>
        {#each users as user}
        <option value='{user?.id}'>{user?.email}</option>
        {/each}
        </select
	>
    <div class="flex my-5 ml-[5rem]">
    <input type="checkbox" class="w-[1em] mt-[2px] mr-[1rem] input" bind:checked={systemLogs}/>
    <p>Excluir los registros del sistema</p>
</div>
<button on:click={search} class="mt-[2rem] ml-[4rem] btn variant-filled"
><i class="fa-solid fa-magnifying-glass"></i></button
>
<footer class="p-4 text-center dark:text-gray-300 text-gray-900 text-sm">
    <p>Es posible dejar los campos vacios si no se desea incluir en la busqueda.</p>
  </footer>
