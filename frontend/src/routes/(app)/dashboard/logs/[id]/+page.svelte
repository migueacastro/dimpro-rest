<script>
	import { goto } from '$app/navigation';
	import { checkAdminGroup } from '$lib/auth';
	import { onMount } from 'svelte';

    export let data;
    let {user} = data;
    let {logStr} = data;
    onMount(() => {
        if(!checkAdminGroup(user)){
            goto("/dashboard");
        }
    });
</script>

<p>{logStr}</p>
<p>en desarrollo</p>