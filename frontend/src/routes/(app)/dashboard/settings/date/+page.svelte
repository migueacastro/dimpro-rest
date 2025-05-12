<script>
	import { goto } from "$app/navigation";

let date = "";
const search = () => {
    goto(`/dashboard/logs?date=${date}`)
};
</script>

<p class="h2 mb-5">Indique la fecha que desea buscar</p>


<div class="flex gap-5">
    <input type="date" class="input" bind:value={date}>
    <button on:click={search} class="btn variant-filled"><i class="fa-solid fa-magnifying-glass"></i></button>
</div>