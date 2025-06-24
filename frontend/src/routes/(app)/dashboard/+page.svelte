<script>
	import { checkPermission } from '$lib/auth.ts';
	import Datatable from '$lib/components/Datatable.svelte';
	export let data;
	let {user} = data;
</script>

<title>Dimpro Iluminación</title>

{#if checkPermission(user, "view_advanced_homepage_user")}
	<div class="lg:flex lg:flex-row mb-[1rem] justify-center">
		{#if checkPermission(user, "view_order") || checkPermission(user, "view_own_order")}
		<a
			class="block card card-hover lg:p-[3.75rem] p-[1.5rem] lg:w-[50%] lg:mr-[1rem] my-5 dark:variant-filled-surface variant-filled-tertiary"
			href="/dashboard/orders"
		>
			<div class="flex flex-row justify-center h-[2rem] lg:h-auto items-center">
				<p class="font-bold h4">Historial de Pedidos</p>
				<i class="fa-solid fa-box h3 ml-5" />
			</div>
		</a>
		{/if}
		{#if checkPermission(user, "view_user")}
		<a
			class=" block card card-hover lg:p-[3.75rem] p-[1.5rem] my-5 lg:w-[30%] lg:mr-[1rem] dark:variant-filled-surface variant-filled-tertiary"
			href="/dashboard/users"
		>
			<div class="flex flex-row justify-center items-center lg:h-auto h-[2rem]">
				<p class="font-bold h4">Vendedores</p>
				<i class="fa-solid fa-users h3 ml-5" />
			</div>
		</a>
		{/if}
		<a
			class="block card card-hover lg:p-[3.75rem] p-[1.5rem] lg:w-[20%] my-5 dark:variant-filled-surface variant-filled-tertiary"
			href="/dashboard/user"
		>
			<div class="flex flex-row justify-center lg:h-auto h-[2rem]">
				<p class="font-bold h4">Perfil</p>
				<i class="fa-solid fa-user h3 ml-5" />
			</div>
		</a>
	</div>
	{#if checkPermission(user, 'view_order')}
	<div>
		<Datatable
			editable={false}
			source_data={data.list}
			endpoint={{ main: 'orders' }}
			headings={['ID', 'Usuario', 'Contacto', 'Cantidad productos', 'Estado', 'Realización']}
			fields={['id', 'user_name', 'contact_name', 'product_count', 'status', 'date_format']}
		/>
	</div>
	{/if}
{:else}
	
	<div class="lg:flex lg:flex-row mb-[1rem] justify-center">
		{#if checkPermission(user, 'add_order')}
		<a
			class=" block card card-hover lg:p-[3.75rem] p-[1.5rem] my-5 lg:w-[30%] lg:mr-[1rem] dark:variant-filled-surface variant-filled-tertiary"
			href="/dashboard/add-order"
		>
			<div class="flex flex-row justify-center h-[2rem] lg:h-auto items-center">
				<p class="font-bold h4">Crear Pedido</p>
				<i class="fa-solid fa-plus h3 ml-5" />
			</div>
		</a>
		{/if}
		{#if checkPermission(user, 'view_order')}
		<a
			class="block card card-hover lg:p-[3.75rem] p-[1.5rem] my-5 lg:w-[30%] lg:mr-[1rem] dark:variant-filled-surface variant-filled-tertiary"
			href="/dashboard/orders"
		>
			<div class="flex flex-row justify-center h-[2rem] lg:h-auto items-center">
				<p class="font-bold h4">Pedidos</p>
				<i class="fa-solid fa-box h3 ml-5" />
			</div>
		</a>
		{/if}
		<a
			class="block card card-hover lg:p-[3.75rem] p-[1.5rem] my-5 lg:w-[30%] lg:mr-[1rem] dark:variant-filled-surface variant-filled-tertiary"
			href="/dashboard/user"
		>
			<div class="flex flex-row justify-center h-[2rem] lg:h-auto items-center">
				<p class="font-bold h4">Vendedor</p>
				<i class="fa-solid fa-user h3 ml-5" />
			</div>
		</a>
	</div>
{/if}
