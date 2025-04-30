<script lang="ts">
	import { popup } from '@skeletonlabs/skeleton';
	import type { AutocompleteOption, PopupSettings } from '@skeletonlabs/skeleton';
	import { Autocomplete } from '@skeletonlabs/skeleton';
	import { getToastStore } from '@skeletonlabs/skeleton';
	import type { ToastSettings } from '@skeletonlabs/skeleton';
	import { goto } from '$app/navigation';
	import { enhance } from '$app/forms';

	export let data;
	const toastStore = getToastStore();
	const successSettings: ToastSettings = {
		message: 'Pedido creado exitosamente'
	};
	const errorSettings: ToastSettings = {
		message: 'Error al crear pedido'
	};
	let popupSettings: PopupSettings = {
		event: 'focus-click',
		target: 'popupAutocomplete',
		placement: 'bottom'
	};
	let inputContact: string = '';
	let selectedContactId: number;
	let contactList: AutocompleteOption<number, string>[] = data.contactList ?? [];
	async function handleSubmit() {
		return ({update, result}: any) => {
			console.log(result);
			if (result.type == 'success') {
				toastStore.trigger(successSettings);
				goto('/dashboard/orders/'+result.data.data.id);
			} else {
				toastStore.trigger(errorSettings);
			}
		}
	}
</script>

<h1 class="h2 my-4">Crear Pedido</h1>
<div class="flex flex-col w-1/2 max-w-md">
	<form action="?/create" method="post" use:enhance={handleSubmit}>
		<label for="select-contact" class="text-md my-2">Cliente</label>
		<input
			class="input autocomplete my-2"
			type="search"
			name="autocomplete-search"
			bind:value={inputContact}
			placeholder="Search..."
			use:popup={popupSettings}
		/>
		<div data-popup="popupAutocomplete" class="max-w-md w-full card">
			<Autocomplete
				bind:input={inputContact}
				options={contactList}
				on:selection={(e) => {
					inputContact = e.detail.label;
					selectedContactId = e.detail.value;
				}}
			/>
		</div>
		<p>
			No encuentras a un cliente? <a
				class="text-primary-500"
				href="mailto:dimproiluminacion@gmail.com ?subject=Solicitud de adición de cliente. &body=Nombre: %0D%0A Correo electrónico: %0D%0A RIF: %0D%0A Insertar imágen de documento RIF:"
				>solicita la adición de uno.</a
			>
		</p>

		<div class="flex flex-row justify-end">
			<input type="hidden" name="contact" value={selectedContactId}/>
			<button
				type="submit"
				class="btn variant-filled max-w-fit my-[2rem] px-[2rem]"
			>
				Crear
			</button>
		</div>
	</form>
	
</div>
