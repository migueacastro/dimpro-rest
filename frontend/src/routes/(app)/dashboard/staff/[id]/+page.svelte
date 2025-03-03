<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
	import { onMount } from 'svelte';
	import { fetchData } from '$lib/utils';
	import { goto } from '$app/navigation';
	import { authenticate } from '$lib/auth';
	import { user } from '../../../../../stores/stores';
	export let data: any;
	let staff: any;
	onMount(async () => {
		await authenticate();
		let response = await fetchData('staff/' + data?.id, 'GET');
		staff = await response.json();
		if (staff['detail'] === 'No encontrado.') {
			goto('/dashboard');
		} else {
			let isAdmin = false;
			$user['groups'].forEach((group: any) => {
				if (group['name'] === 'admin') {
					isAdmin = true;
				}
			});
			if (!isAdmin) {
				goto('/dashboard');
			}
		}
	});
</script>

<div class="flex flex-col">
	<div class="flex flex-row">
		<div class="card p-[3rem] w-full mb-[2rem] mr-[2rem]">
			<div class="flex flex-col">
				<h4 class="h4 capitalize my-2">{staff?.name}</h4>
				<h4 class="h4 capitalize my-2">{staff?.email}</h4>
				<h4 class="h4 capitalize my-2">{staff?.phonenumber}</h4>
			</div>
		</div>
		<div class="card p-[3rem] w-full mb-[2rem]">
			<div class="flex flex-col">
				<h4 class="h4 my-2">Se unió en: {staff?.date_joined_format}</h4>
				<h4 class="h4 my-2">Último inicio de sesión: {staff?.last_login_format}</h4>
			</div>
		</div>
	</div>
	<div class="flex flex-row justify-between mb-[2rem]">
		<h2 class="h2">Pedidos: {staff?.orders?.length}</h2>
	</div>
	<Datatable
		use_array={true}
		source_data={staff?.orders}
		fields={['id', 'item', 'reference', 'quantity', 'price', 'cost']}
		headings={['Id', 'Item', 'Referencia', 'Cantidad', 'Precio', 'Costo']}
	/>
</div>
