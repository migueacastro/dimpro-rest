<script>
	import { user } from '../../../stores/stores';
</script>

{#if $user?.is_staff || $user?.is_superuser}
	<div class="lg:flex lg:flex-row ">
		<a class="block card card-hover lg:p-[3.75rem] p-[1.5rem] mx-auto lg:my-auto my-5 dark:variant-filled-surface variant-filled-tertiary" href="history">
			<div class="flex flex-row">
				<p class="font-bold h4">Historial de Pedidos</p>
				<i class="fa-solid fa-box h3 ml-5" />
			</div>
		</a>
		<a class="block card card-hover lg:p-[3.75rem] p-[1.5rem] mx-auto lg:my-auto my-5 dark:variant-filled-surface variant-filled-tertiary" href="sellers">
			<div class="flex flex-row">
				<p class="font-bold h4">Vendedores</p>
				<i class="fa-solid fa-users h3 ml-5" />
			</div>
		</a>
		<a class="block card card-hover lg:p-[3.75rem] p-[1.5rem] mx-auto lg:my-auto my-5 dark:variant-filled-surface variant-filled-tertiary" href="user">
			<div class="flex flex-row">
				<p class="font-bold h4">Empleado</p>
				<i class="fa-solid fa-user h3 ml-5" />
			</div>
		</a>
	</div>
{:else}  
	<div class="lg:flex lg:flex-row ml-[3.5rem] mt-5">
		<a class="block card card-hover lg:p-[3.75rem] p-[1.5rem] mx-auto lg:my-auto my-5 dark:variant-filled-surface variant-filled-tertiary" href="add">
			<div class="flex flex-row">
				<p class="font-bold h4">Crear Pedido</p>
				<i class="fa-solid fa-plus h3 ml-5" />
			</div>
		</a>
		<a class="block card card-hover lg:p-[3.75rem] p-[1.5rem] mx-auto lg:my-auto my-5 dark:variant-filled-surface variant-filled-tertiary" href="orders">
			<div class="flex flex-row">
				<p class="font-bold h4">Pedidos</p>
				<i class="fa-solid fa-box h3 ml-5" />
			</div>
		</a>
		<a class="block card card-hover lg:p-[3.75rem] p-[1.5rem] mx-auto lg:my-auto my-5 dark:variant-filled-surface variant-filled-tertiary" href="user">
			<div class="flex flex-row">
				<p class="font-bold h4">Vendedor</p>
				<i class="fa-solid fa-user h3 ml-5" />
			</div>
		</a>
	</div>
{/if}
