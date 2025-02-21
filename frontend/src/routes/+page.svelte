<script lang="ts">
	import { onMount } from "svelte";
	import { user } from "../stores/stores";
	import Cookies from "js-cookie";
	import { goto } from "$app/navigation";
	onMount(async () => {
		let token = Cookies.get('token');
		if (token) {
			goto("/dashboard");
		} else {
			goto("/start");
		}
	});
</script>

<title>Cargando...</title>

<div class="m-[10rem]">
	<h1 style="font-size: x-large;">Bienvenido, 
		{$user?.name}
	</h1>
</div>