<script lang="ts">
	import { enhance } from '$app/forms';
	import { goto } from '$app/navigation';
  import {RadioGroup, RadioItem} from '@skeletonlabs/skeleton';
	import { getModalStore, getToastStore, ProgressRadial, type ModalSettings, type ToastSettings } from '@skeletonlabs/skeleton';

  $: loaded = true;
  $: action = "Crear";
	export let data;
  const modalStore = getModalStore();

	const toastStore = getToastStore();
  let form: HTMLFormElement;



	async function handleEnhance() {
    loaded = false;
		return ({ update, result }: any) => {
			let toast: ToastSettings  = {
					message: 'Token actualizado con exito.',
					background: 'variant-ghost-success',
					timeout: 7000
				};
			if (result?.type === 'success') {
				toastStore.trigger(toast);
				return goto('/dashboard/settings');
				
			} else {
				
				toast = {
					message: `¡ERROR! No se pudo actualizar el Token.`,
					background: 'variant-ghost-error',
					timeout: 7000
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
	<h3 class="text-4xl mb-[2rem]">Cambiar Permisos</h3>

  <form action="?/save" method="post" use:enhance={handleEnhance} bind:this={form}>
    <select class="select capitalize mb-4" name="group-select" id="">
      {#each data.groups as group}
        <option value={group.id}>{group.name}</option>
      {/each}
    </select>
    <div class="mx-auto flex justify-center">
      <RadioGroup>
        <RadioItem bind:group={action} name="Crear" value={"Crear"}>Crear</RadioItem>
        <RadioItem bind:group={action} name="Leer" value={"Leer"}>Ver</RadioItem>
        <RadioItem bind:group={action} name="Editar" value={"Editar"}>Editar</RadioItem>
        <RadioItem bind:group={action} name="Eliminar" value={"Eliminar"}>Eliminar</RadioItem>
      </RadioGroup>
    </div>
    
  </form>
</div>
{:else}
	<div class="flex justify-center mt-[8rem]">
		<div class="my-auto">
			<ProgressRadial/>
		</div>
	</div>
{/if}
