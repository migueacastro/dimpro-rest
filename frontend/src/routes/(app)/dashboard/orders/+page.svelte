<script>
	import { checkPermission, checkStaffGroup } from '$lib/auth';
	import Datatable from '$lib/components/Datatable.svelte';
	import { RadioGroup, RadioItem } from '@skeletonlabs/skeleton';
	export let data;
	let orderType = 'all';
</script>

{#if checkPermission(data.user, 'view_order') && checkPermission(data.user, 'view_own_order')}
	<RadioGroup name="order_type">
		<RadioItem bind:group={orderType} name="order_type" value={'all'}>Todos los pedidos</RadioItem>
		<RadioItem bind:group={orderType} name="order_type" value={'user'}>Mis pedidos</RadioItem>
	</RadioGroup>
{/if}
{#if (checkPermission(data.user, 'view_order') && !checkPermission(data.user, 'view_own_order')) || (checkPermission(data.user, 'view_order') && checkPermission(data.user, 'view_own_order') && orderType == 'all')}
	<h1 class="h2 my-4">Pedidos</h1>
	<Datatable
		editable={false}
		source_data={data.list_all}
		endpoint={{ main: 'orders' }}
		headings={['ID', 'Usuario', 'Contacto', 'Cantidad productos', 'Estado', 'Realización']}
		fields={['id', 'user_name', 'contact_name', 'product_count', 'status', 'date_format']}
	/>
{:else if (!checkPermission(data.user, 'view_order') && checkPermission(data.user, 'view_own_order')) || (checkPermission(data.user, 'view_order') && checkPermission(data.user, 'view_own_order') && orderType == 'user')}
	<h1 class="h2 my-4">Mis Pedidos</h1>
	<Datatable
		editable={false}
		source_data={data.list_user}
		endpoint={{ main: 'orders', secondary: 'orders' }}
		headings={['ID', 'Usuario', 'Contacto', 'Cantidad productos', 'Estado', 'Realización']}
		fields={['id', 'user_name', 'contact_name', 'product_count', 'status', 'date_format']}
	/>
{/if}
