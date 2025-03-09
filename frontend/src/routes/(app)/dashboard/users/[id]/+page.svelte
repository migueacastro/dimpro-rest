<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
	import { onMount } from 'svelte';
	import { fetchData } from '$lib/utils';
	import { goto } from '$app/navigation';
	import { authenticate } from '$lib/auth';
	export let data: any;
	let user: any;
	onMount(async () => {
		await authenticate();
		let response = await fetchData('users/' + data?.id, 'GET');
		user = await response.json();
		if(user['detail']==='No posee los permisos necesarios'){
			goto('/dashboard');
		}
	});
</script>

<div class="flex flex-col">
	<div class="flex flex-row">
		<div class="card p-[3rem] w-full mb-[2rem] mr-[2rem]">
			<div class="flex flex-col">
				<h4 class="h4 capitalize my-2">{user?.name}</h4>
				<h4 class="h4 capitalize my-2">{user?.email}</h4>
				<h4 class="h4 capitalize my-2">{user?.phonenumber}</h4>
			</div>
		</div>
		<div class="card p-[3rem] w-full mb-[2rem]">
			<div class="flex flex-col">
				<h4 class="h4 my-2">Se unió en: {user?.date_joined_format}</h4>
				<h4 class="h4 my-2">Último inicio de sesión: {user?.last_login_format}</h4>
			</div>
		</div>
	</div>
	<div class="flex flex-row justify-between mb-[2rem]">
		<h2 class="h2">Pedidos: {user?.orders?.length}</h2>
	</div>
	<Datatable
		use_array={true}
		source_data={user?.orders}
		fields={['id', 'item', 'reference', 'quantity', 'price', 'cost']}
		headings={['Id','Item','Referencia','Cantidad','Precio','Costo']}
	/>
</div>
