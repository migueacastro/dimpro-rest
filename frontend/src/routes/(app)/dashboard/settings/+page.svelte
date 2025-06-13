<script lang="ts">
	import { enhance } from '$app/forms';
	import { checkAdminGroup, checkPermission } from '$lib/auth';
	import { getToastStore, ProgressRadial } from '@skeletonlabs/skeleton';
	import type { ToastStore } from '@skeletonlabs/skeleton';
	const toastStore: ToastStore = getToastStore();
	let updateDBForm: HTMLFormElement;
	export let data: any;
	let { user } = data;
	$: loaded = true;
	function handleUpdateDBEnhance() {
		loaded = false;
		return async ({ result, update }: any) => {
			if (result.type === 'success') {
				toastStore.trigger({
					message: 'La base de datos ha sido actualizada exitosamente',
					background: 'variant-ghost-success',
					timeout: 3500
				});
			} else {
				toastStore.trigger({
					message: 'Error al actualizar la base de datos',
					background: 'variant-ghost-error',
					timeout: 3500
				});
			}
			loaded = true;
			return update({ reset: false });
		};
	}
	function handleUpdateDBButton(event: Event) {
		toastStore.trigger({
			message: 'Iniciando actualizacion de la base de datos.',
			background: 'variant-ghost-info',
			timeout: 3500
		});
		updateDBForm.requestSubmit();
	}
</script>

{#if loaded}
	<div class="flex flex-col">
		<h1 class="h2 my-4">Configuración</h1>
		<div class="lg:flex lg:flex-row mb-[1rem] flex-wrap lg:justify-start justify-center">
			{#if checkPermission(user, 'view_staff_user')}
			<a
				class="block card card-hover lg:p-[3.75rem] p-[1.5rem] lg:w-[30%] my-2 lg:mx-2 dark:variant-filled-surface variant-filled-tertiary"
				href="/dashboard/staff"
			>
				<div class="flex flex-row justify-center h-[2rem] lg:h-auto items-center">
					<p class="font-bold h4">Empleados</p>
					<i class="fa-solid fa-users-gear h3 ml-5" />
				</div>
			</a>
			{/if}
			{#if checkPermission(user, 'view_alegrauser')}
			<a
				class="block card card-hover lg:p-[3.75rem] p-[1.5rem] lg:w-[30%] my-2 lg:mx-2 dark:variant-filled-surface variant-filled-tertiary"
				href="/dashboard/settings/change-token"
			>
				<div class="flex flex-row justify-center h-[2rem] lg:h-auto items-center">
					<p class="font-bold h4">Cambiar Token de Alegra</p>
					<i class="fa-solid fa-flag h3 ml-5" />
				</div>
			</a>
			{/if}
			{#if checkPermission(user, 'view_logentry')}
			<a
				class="block card card-hover lg:p-[3.75rem] p-[1.5rem] lg:w-[30%] my-2 lg:mx-2 dark:variant-filled-surface variant-filled-tertiary"
				href="/dashboard/settings/filter"
			>
				<div class="flex flex-row justify-center h-[2rem] lg:h-auto items-center">
					<p class="font-bold h4">Registros</p>
					<i class="fa-solid fa-book h3 ml-5" />
				</div>
			</a>
			{/if}
			{#if checkAdminGroup(user)}
			<a
				class="block card card-hover lg:p-[3.75rem] p-[1.5rem] lg:w-[30%] my-2 lg:mx-2 dark:variant-filled-surface variant-filled-tertiary"
				href="/dashboard/settings/permissions"
			>
				<div class="flex flex-row justify-center h-[2rem] lg:h-auto items-center">
					<p class="font-bold h4">Permisos</p>
					<i class="fa-solid fa-book h3 ml-5" />
				</div>
			</a>
			{/if}
			
			{#if checkPermission(user, 'view_updatedb_product')}
			<form
				bind:this={updateDBForm}
				action="?/updatedb"
				use:enhance={handleUpdateDBEnhance}
				method="POST"
				class="block card card-hover lg:p-[3.75rem] p-[1.5rem] lg:w-[30%] my-2 lg:mx-2 dark:variant-filled-surface variant-filled-tertiary"
			>
				<button
					type="button"
					on:click={handleUpdateDBButton}
					class="flex flex-row justify-center w-full"
				>
					<div class="flex flex-row justify-center h-[2rem] lg:h-auto items-center">
						<p class="font-bold h4">Actualizar la base de datos</p>
						<i class="fa-solid fa-database h3 ml-5" />
					</div>
				</button>
			</form>
			{/if}
		</div>
	</div>
{:else}
	<div class="flex justify-center mt-[8rem]">
		<div class="my-auto">
			<h2 class="h2 text-center mb-8">Actualizando la base de datos</h2>
			<div class="w-full justify-center flex"><ProgressRadial /></div>
		</div>
	</div>
{/if}
