<script lang="ts">
	import { enhance } from '$app/forms';
	import { goto } from '$app/navigation';
	import { checkPermission } from '$lib/auth';
	import RequestStatusButton from '$lib/components/RequestStatusButton.svelte';
	import { FormErrors } from '$lib/FormErrors';
	import {
		Autocomplete,
		getModalStore,
		getToastStore,
		popup,
		type AutocompleteOption,
		type ModalSettings,
		type PopupSettings,
		type ToastSettings
	} from '@skeletonlabs/skeleton';
	export let data: any;
	let { user } = data;
	let errors = new FormErrors();
	let identification = {
		value: data?.request?.identification,
		touched: false,
		valid: errors.validateCardID(data?.request?.identification)
	};
	let email = {
		value: data?.request?.email,
		touched: false,
		valid: errors.validateEmail(data?.request?.email)
	};
	let name = {
		value: data?.request?.name,
		touched: false,
		valid: errors.validateText(data?.request?.name)
	};
	let phonePrimary = {
		value: data?.request?.phonePrimary,
		touched: false,
		valid: errors.validatePhoneNumber(data?.request?.phonePrimary)
	};
	let address = {
		value: data?.request?.address,
		touched: false,
		valid: errors.validateText(data?.request?.address)
	};

	$: valid =
		identification.valid && email.valid && name.valid && phonePrimary.valid && address.valid;

	let toastStore = getToastStore();
	let modalStore = getModalStore();
	let saved: boolean = true;


	async function handleSave() {
		return async ({ update, result }: any) => {
			let toast: ToastSettings;
			if (result?.type == 'success') {
				saved = true;
				toast = {
					message: 'Se guardó la solicitud con éxito.',
					background: 'variant-ghost-success',
					timeout: 3500
				};
				console.log('Successfully saved');
				toastStore.trigger(toast);
			} else {
				toast = {
					message: `¡ERROR! No se pudo guardar la solicitud.
							\nmensaje:${result.data}`,
					background: 'variant-ghost-error',
					timeout: 3500
				};
				toastStore.trigger(toast);
			}
		};
	}

	let inputUser: string = data?.request?.user_name || '';
	let selectedUserId: number = data?.request?.user || 0;
	let userList: AutocompleteOption<number, string>[] = data?.users || [];
	let popupSettings: PopupSettings = {
		event: 'focus-click',
		target: 'popupAutocomplete',
		placement: 'bottom'
	};
	let deleteForm: HTMLFormElement;
	async function confirmDelete() {
		const modal: ModalSettings = {
			type: 'confirm',
			title: `Eliminar solicitud`,
			body: `¿Está seguro de eliminar esta solicitud?`,

			response: async (r: boolean) => {
				if (r) {
					
					deleteForm.requestSubmit();
				}
			}
		};
		modalStore.trigger(modal);
	}
	

	async function handleDelete() {
		return async ({ update, result }: any) => {
			let toast: ToastSettings;
			if (result?.type == 'success') {
				toast = {
					message: 'La solicitud se eliminó con éxito.',
					background: 'variant-ghost-success',
					timeout: 3500
				};
				console.log('Successfully deleted');
				goto(`/dashboard/contact-add-request/`);
				toastStore.trigger(toast);
			} else {
				toast = {
					message: `¡ERROR! La solicitud no se pudo eliminar.
							\nmensaje:${result.data}`,
					background: 'variant-ghost-error',
					timeout: 3500
				};
				toastStore.trigger(toast);
			}
		};
	}
</script>

<div class="w-3/4">
	<h1 class="h2 my-4">Solicitar Crear Cliente</h1>
	<form action="?/edit" method="post" use:enhance={handleSave} class="flex flex-col">
		<label for="user"> Usuario </label>
		<input
			class="input autocomplete my-2"
			type="search"
			name="autocomplete-search"
			autocomplete="off"
			bind:value={inputUser}
			placeholder="Search..."
			use:popup={popupSettings}
		/>
		<div data-popup="popupAutocomplete" class="max-w-md w-full card">
			<Autocomplete
				bind:input={inputUser}
				options={userList}
				on:selection={(e) => {
					inputUser = e.detail.label;
					selectedUserId = e.detail.value;
					saved = false;
				}}
			/>
		</div>
		<input type="hidden" name="user" value={selectedUserId} />
		<input type="hidden" name="status" value="pendiente" />
		<div class="flex flex-col space-y-2">
			<label for="identification">Cédula</label>
			<input
				type="text"
				bind:value={identification.value}
				class="input"
				name="identification"
				on:click={() => (identification.touched = true)}
				on:input={() => {
					identification.valid = errors.validateCardID(identification.value);
					identification.touched = true;
					saved = false;
				}}
				id="identification"
				required
			/>
			{#if identification.touched}
				{#if !errors.validateCardID(identification.value)}
						<div class="card variant-ghost-error p-2 text-sm text-left">
							{'La cédula o el rif no es válido'}
						</div>
				{/if}
			{/if}
			<label for="email">Email</label>
			<input
				type="email"
				bind:value={email.value}
				class="input"
				name="email"
				id="email"
				required
				on:click={() => (email.touched = true)}
				on:input={() => {
					email.valid = errors.validateEmail(email.value);
					email.touched = true;
					saved = false;
				}}
			/>
			{#if email.touched}
				{#if !email.value.match(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/)}
					<div class="card variant-ghost-error p-2 text-sm text-left">
						{'El email no es válido'}
					</div>
				{/if}
			{/if}

			<label for="name">Nombre</label>
			<input
				type="text"
				bind:value={name.value}
				class="input"
				name="name"
				id="name"
				on:click={() => (name.touched = true)}
				on:input={() => {
					name.valid = errors.validateText(name.value);
					name.touched = true;
					saved = false;
				}}
				required
			/>
			{#if name.touched}
				{#if !name.value.match(/^[a-zA-Z\s]+$/)}
					<div class="card variant-ghost-error p-2 text-sm text-left">
						{'El nombre no es válido'}
					</div>
				{/if}
			{/if}

			<label for="phonePrimary">Teléfono</label>
			<input
				type="text"
				bind:value={phonePrimary.value}
				class="input"
				name="phonePrimary"
				id="phonePrimary"
				on:click={() => (phonePrimary.touched = true)}
				on:input={() => {
					phonePrimary.valid = errors.validatePhoneNumber(phonePrimary.value);
					phonePrimary.touched = true;
					saved = false;
				}}
				required
			/>
			{#if phonePrimary.touched}
				{#if phonePrimary?.value?.length > 0}
					{#if !errors.validatePhoneNumber(phonePrimary.value)}
						<div class="card variant-ghost-error p-2 text-sm text-left">
							{errors.NotValidPhone}
						</div>
					{/if}
				{:else}
					<div class="card variant-ghost-error p-2 text-sm text-left">
						{errors.empyField}
					</div>
				{/if}
			{/if}

			<label for="address">Dirección</label>
			<textarea
				name="address"
				bind:value={address.value}
				class="input"
				id="address"
				required
				on:click={() => (address.touched = true)}
				on:input={() => {
					address.valid = errors.validateText(address.value);
					address.touched = true;
					saved = false;
				}}
			></textarea>
			{#if address.touched}
				{#if !errors.validateText(address.value)}
					<div class="card variant-ghost-error p-2 text-sm text-left">
						{'La dirección no es válida'}
					</div>
				{/if}
			{/if}
		</div>

		<div class="flex flex-row">
			<button
				type="submit"
				class="btn w-fit variant-filled-primary p-4 my-4"
				disabled={!identification.valid ||
					!email.valid ||
					!name.valid ||
					!phonePrimary.valid ||
					!address.valid}>Guardar Solicitud</button

			>
			{#if checkPermission(data.user, 'view_approve_contactaddrequest')}
				<RequestStatusButton request={data?.request} saved={saved} />
			{/if}
			{#if checkPermission(data.user, 'delete_contactaddrequest')}
			<form action="?/delete"
					method="post"
					bind:this={deleteForm}
					use:enhance={handleDelete}>
				<button
					type="button"
					class="btn variant-ghost-error max-w-fit px-[2rem]  ml-2 p-4 my-4"
					on:click={confirmDelete}
				>
					<i class="fa-solid fa-trash"></i>
				</button>
			</form>
				
			{/if}
			
		</div>
	</form>
</div>
