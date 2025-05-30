<script>
	import { goto } from '$app/navigation';
	import { checkAdminGroup } from '$lib/auth';
	import { onMount } from 'svelte';

    export let data;
    let {user} = data;
    let {log} = data;
    onMount(() => {
        switch(log.action){
            case 0: 
            log.action = "Creación.";
            break;
            case 1: 
            log.action = "Actualización.";
            break;
            case 2: 
            log.action = "Eliminación.";
            break;
            case 3: 
            log.action = "Petición de acceso.";
            break;
        }
        if(!checkAdminGroup(user)){
            goto("/dashboard");
        }
    });
</script>


<p class="h2 text-center">Información del registro N°{log['id']}</p>

<div class="card my-3 p-10 text-start lg:w-[75%] space-y-6 mx-auto">
        <p>ID del registro: {log.id}</p>
        <p>ID del autor: {log?.actor_name}</p>
        <p>Email del autor: {log?.actor_email}</p>
        <p>Tipo de acción realizada: {log.action}</p>
        <p>Mensaje de cambios: {log.changes_text}</p>
        <p>JSON de cambios: {log.changes ?? "No Definido."}</p>
        <p>ID del objeto alterado: {log.object_id}</p>
        <p>JSON del objeto alterado: {log.object_repr}</p>
        <p>Dirección IP de la petición: {log.remote_addr}</p>
        <p>Tiempo de modificación: {log.timestamp}</p>
</div>