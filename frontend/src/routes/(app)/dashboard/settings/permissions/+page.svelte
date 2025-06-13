<script lang="ts">
	import { enhance } from '$app/forms';
	import { goto, invalidateAll } from '$app/navigation';
	import { SlideToggle } from '@skeletonlabs/skeleton';
	import {
		getModalStore,
		getToastStore,
		ProgressRadial,
		type ModalSettings,
		type ToastSettings
	} from '@skeletonlabs/skeleton';

	export let data;
	let groupsObject: any = data.groupsObject;
	let selectedGroupId = groupsObject[0]?.id || 0;
	$: selectedGroup = groupsObject.find((group: any) => group.id === selectedGroupId);
	
	$: loaded = true;

	$: JSONStringifiedGroupsObject = JSON.stringify(groupsObject);

	$: permissionsObject = data.permissionsObject ?? {};
	const listPermissionNames = data.listPermissionNames;

	let permissionChecked: { [id: number]: boolean } = {};



	function togglePermission(event: any, permission: any) {
		if (selectedGroup?.permissions.includes(permission.id)) {
			selectedGroup.permissions = selectedGroup.permissions.filter(
				(id: number) => id !== permission.id
			);
		} else {
			selectedGroup.permissions.push(permission.id);
			
		}
		groupsObject = groupsObject.map((group: any) => {
				if (group.id === selectedGroupId) {
					return { ...group, permissions: selectedGroup.permissions };
				}
				return group;
			});
		updatePermissionChecked();
	}

	function updatePermissionChecked() {
		let updated: {[id: number]: boolean} = {};
		for (const name of listPermissionNames) {
			(permissionsObject[name] || []).forEach((permission: any) => {
				// Mark as checked if the selectedGroup's permissions include this permission id
				updated[permission.id] = selectedGroup.permissions.includes(permission.id);
			});
		}
		permissionChecked = updated;
	}

	$: if (selectedGroup) {
		updatePermissionChecked();
	}

	const modalStore = getModalStore();

	const toastStore = getToastStore();
	let form: HTMLFormElement;

	function confirmation() {
		const modal: ModalSettings = {
			type: 'confirm',
			title: `¿Está seguro de querer modificar estos permisos?`,
			body: `Puede alterar el funcionamiento de la aplicación.`,
			response: async (r: boolean) => {
				if (r) {
					form.requestSubmit();
				}
			}
		};
		modalStore.trigger(modal);
	}

	async function handleEnhance() {
		loaded = false;
		return ({ update, result }: any) => {
			let toast: ToastSettings = {
				message: 'Permisos actualizados con exito.',
				background: 'variant-ghost-success',
				timeout: 3500
			};
			if (result?.type === 'success') {
				window.location.reload();
				return
			} else {
				toast = {
					message: `¡ERROR! No se pudo actualizar los permisos.`,
					background: 'variant-ghost-error',
					timeout: 3500
				};
				toastStore.trigger(toast);
			}
			loaded = true;
			return update({ reset: false });
		};
	}
</script>

<title>Cambiar permisos</title>

{#if loaded}
	<div class=" mx-auto flex flex-col lg:w-1/2 w-full justify-start">
		<div class="flex flex-col lg:flex-row justify-between mb-[2rem]">
			<h3 class="text-4xl">Cambiar Permisos</h3>
			<button on:click={confirmation} class="btn w-fit my-2 h-fit variant-filled-primary"
				><i class="fa-solid fa-floppy-disk mr-5"></i>Guardar</button
			>
		</div>

		<form action="?/save" method="post" use:enhance={handleEnhance} bind:this={form}>
			<input type="hidden" name="groups" bind:value={JSONStringifiedGroupsObject} />
			<select
				class="select capitalize mb-4"
				name="group-select"
				id=""
				bind:value={selectedGroupId}
				
			>
				{#each groupsObject as group}
					<option class="capitalize" value={group.id}>{group.name}</option>
				{/each}
			</select>
			<div class="mx-auto flex justify-center flex-col space-y-3">
				{#each listPermissionNames as name}
					<div class="card p-3 flex flex-col w-full">
						<h3 class="text-xl mb-4 capitalize">{name}</h3>
						<div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
							{#each permissionsObject[name] as permission}
								<div class="flex items-center capitalize flex-row space-x-4">
									<SlideToggle
										active="bg-primary-500"
										on:click={(e) => togglePermission(e, permission)}
										name={permission.name}
										bind:checked={permissionChecked[permission.id]}
									/>
									<p class="text-sm capitalize">
										{permission.name}
									</p>
								</div>
							{/each}
						</div>
					</div>
				{/each}
			</div>
		</form>
	</div>
{:else}
	<div class="flex justify-center mt-[8rem]">
		<div class="my-auto">
			<ProgressRadial />
		</div>
	</div>
{/if}
