<script>
	import { checkStaffGroup } from '$lib/auth.ts';
	import { user } from '../../../stores/stores';
	import Datatable from '$lib/components/Datatable.svelte';
	import { apiURL } from '$lib/api_url';
</script>

<title>Dimpro Iluminación</title>

{#if checkStaffGroup($user)}
	<div class="lg:flex lg:flex-row mb-[1rem]">
		<a
			class="block card card-hover lg:p-[3.75rem] p-[1.5rem] lg:w-[50%] lg:mr-[1rem] my-5 dark:variant-filled-surface variant-filled-tertiary"
			href="/dashboard/orders"
		>
			<div class="flex flex-row justify-center h-[2rem] lg:h-auto items-center">
				<p class="font-bold h4">Historial de Pedidos</p>
				<i class="fa-solid fa-box h3 ml-5" />
			</div>
		</a>
		<a
			class=" block card card-hover lg:p-[3.75rem] p-[1.5rem] my-5 lg:w-[30%] lg:mr-[1rem] dark:variant-filled-surface variant-filled-tertiary"
			href="/dashboard/users"
		>
			<div class="flex flex-row justify-center items-center lg:h-auto h-[2rem]">
				<p class="font-bold h4">Vendedores</p>
				<i class="fa-solid fa-users h3 ml-5" />
			</div>
		</a>
		<a
			class="block card card-hover lg:p-[3.75rem] p-[1.5rem] lg:w-[20%] my-5 dark:variant-filled-surface variant-filled-tertiary"
			href="/"
		>
			<div class="flex flex-row justify-center lg:h-auto h-[2rem]">
				<p class="font-bold h4">Empleado</p>
				<i class="fa-solid fa-user h3 ml-5" />
			</div>
		</a>
	</div>
	<div>
		<Datatable
			editable={false}
			endpoint={'orders'}
			fields={['ID', 'Usuario', 'Contacto', 'Cantidad productos', 'Estado', 'Realización']}
		/>
	</div>
{:else}
	<div class="lg:flex lg:flex-row ml-[3.5rem] mt-5">
		<a
			class="block card card-hover lg:p-[3.75rem] p-[1.5rem] mx-auto lg:my-auto my-5 dark:variant-filled-surface variant-filled-tertiary"
			href="/dashboard/add-order"
		>
			<div class="flex flex-row">
				<p class="font-bold h4">Crear Pedido</p>
				<i class="fa-solid fa-plus h3 ml-5" />
			</div>
		</a>
		<a
			class="block card card-hover lg:p-[3.75rem] p-[1.5rem] mx-auto lg:my-auto my-5 dark:variant-filled-surface variant-filled-tertiary"
			href="/dashboard/edit-order"
		>
			<div class="flex flex-row">
				<p class="font-bold h4">Pedidos</p>
				<i class="fa-solid fa-box h3 ml-5" />
			</div>
		</a>
		<a
			class="block card card-hover lg:p-[3.75rem] p-[1.5rem] mx-auto lg:my-auto my-5 dark:variant-filled-surface variant-filled-tertiary"
			href="user"
		>
			<div class="flex flex-row">
				<p class="font-bold h4">Vendedor</p>
				<i class="fa-solid fa-user h3 ml-5" />
			</div>
		</a>
	</div>
{/if}
