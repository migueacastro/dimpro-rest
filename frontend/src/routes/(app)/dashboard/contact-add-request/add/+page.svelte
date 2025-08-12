<script lang="ts">
	import { enhance } from '$app/forms';
	import { goto } from '$app/navigation';
	import { FormErrors } from '$lib/FormErrors';
	import { getToastStore, type ToastSettings } from '@skeletonlabs/skeleton';
	export let data: any;
	let { user } = data;

	let identification = { value: '', touched: false, valid: false };
	let email = { value: '', touched: false, valid: false };
	let name = { value: '', touched: false, valid: false };
	let phonePrimary = { value: '', touched: false, valid: false };
	let address = { value: '', touched: false, valid: false };
	

  let toastStore = getToastStore();

	let errors = new FormErrors();
  async function handleSave() {
		return async ({ update, result }: any) => {
			let toast: ToastSettings;
			if (result?.type == 'success') {
				goto(`/dashboard/`);
				toast = {
					message: 'Se solicitó la creación del cliente con éxito.',
					background: 'variant-ghost-success',
					timeout: 3500
				};
				console.log('Successfully saved');
				toastStore.trigger(toast);
			} else {
				toast = {
					message: `¡ERROR! No se pudo solicitar la creación del cliente.
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
	<form action="?/add" method="post" use:enhance={handleSave}  class="flex flex-col">
		<input type="hidden" name="user" value={user.id} />
		<input type="hidden" name="status" value="pendiente" />
		<div class="flex flex-col space-y-2">
			<label for="identification">Cédula o Rif</label>
			<input
				type="text"
				bind:value={identification.value}
				class="input"
				name="identification"
				on:click={() => (identification.touched = true)}
				on:input={() => {
          identification.valid = errors.validateCardID(identification.value)
          identification.touched = true
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
          email.valid = errors.validateEmail(email.value)
          email.touched = true
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
          name.valid = errors.validateText(name.value)
          name.touched = true
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
          phonePrimary.valid = errors.validatePhoneNumber(phonePrimary.value)
          phonePrimary.touched = true
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
          address.valid = errors.validateText(address.value)
          address.touched = true
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

		<button
			type="submit"
			class="btn w-fit variant-filled-primary p-4 my-4"
			disabled={!identification.valid ||
				!email.valid ||
				!name.valid ||
				!phonePrimary.valid ||
				!address.valid}>Enviar Solicitud</button
		>
	</form>
</div>
