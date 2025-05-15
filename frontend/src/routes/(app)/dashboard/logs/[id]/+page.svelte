<script>
	import { goto } from '$app/navigation';
	import { checkAdminGroup } from '$lib/auth';
	import { onMount } from 'svelte';

    export let data;
    let {user} = data;
    let {log} = data;
    let {keys} = data;
    onMount(() => {
        if(!checkAdminGroup(user)){
            goto("/dashboard");
        }
    });
</script>


<p class="h2 text-center">Información del registro N°{log['id']}</p>

<div class="card my-3 p-10 text-start lg:w-[75%] space-y-6 mx-auto">
    {#each keys as key}
        <p>{key}: {log[key]}</p>
    {/each}
</div>