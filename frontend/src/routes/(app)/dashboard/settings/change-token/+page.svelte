<script lang="ts">
	import { enhance } from '$app/forms';
	import { goto } from '$app/navigation';
	import { FormErrors } from '$lib/FormErrors';
	import { getModalStore, getToastStore, ProgressRadial, type ModalSettings, type ToastSettings } from '@skeletonlabs/skeleton';

  $: loaded = true;
	export let data;
	const fields = new FormErrors();
  const modalStore = getModalStore();

	const toastStore = getToastStore();
  let form: HTMLFormElement;

	interface FormErrors {
    email: any
		token: any
	}

	let errors: FormErrors = {
		email: [],
    token: [],
	};

	let email= data.alegratoken.email;
	let token = data.alegratoken.token;
	
	let validatedFields: boolean = false;
	function validateFields() {
		validatedFields = token.length > 0 && email.length > 0;
	}

  async function confirmSave() {
		const modal: ModalSettings = {
			type: 'confirm',
			title: `Modificar Token de Alegra`,
			body: `¿Está seguro de cambiar el Token de Alegra?`,

			response: async (r: boolean) => {
				if (r) {
					
					warningConfirm();
				}
			}
		};
		modalStore.trigger(modal);
	}
  async function warningConfirm() {
		const modal: ModalSettings = {
			type: 'confirm',
			title: `Modificar Token de Alegra`,
			body: `Si coloca el token equivocado, no podrá acceder a la información en Alegra, ni actualizar la base de datos.`,

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
			let toast: ToastSettings  = {
					message: 'Token actualizado con exito.',
					background: 'variant-ghost-success',
					timeout: 3500
				};
			if (result?.type === 'success') {
				toastStore.trigger(toast);
				return goto('/dashboard/settings');
				
			} else {
				
				toast = {
					message: `¡ERROR! No se pudo actualizar el Token.`,
					background: 'variant-ghost-error',
					timeout: 3500
				};
				toastStore.trigger(toast);
			}
      loaded = true;
			return update({ reset: false });
		};
	}

	function togglePasswordInput(event: Event) {
		let button = event.target as HTMLElement;
		if (button.tagName !== 'BUTTON') { // just in case the event.target is the icon and not the button
			button = button.closest('button') as HTMLElement;
		}
		const input = button.closest('.input-group')?.querySelector('input') as HTMLInputElement;
		input.type = input.type === 'password' ? 'text' : 'password';
		const icon = button.querySelector('i') as HTMLElement;
		icon.classList.toggle('fa-eye');
		icon.classList.toggle('fa-eye-slash');
	}
</script>

<title>Cambiar Token de Alegra</title>

{#if loaded}
<div class=" mx-auto flex flex-col lg:w-1/2 w-full">
	<form method="post" action="?/changetoken" use:enhance={handleEnhance} bind:this={form}>
		<h3 class="text-4xl mb-[2rem]">Cambiar Token de Alegra</h3>
		<div class="input-group input-group-divider grid-cols-[1fr_auto] my-2">
			<input
				class="input"
				title="Email"
				type="email"
				id="email"
				name="email"
				placeholder="Email"
				bind:value={email}
				on:input={validateFields}
			/>
		</div>
		{#if errors?.email?.length > 0}
			<div class="card variant-ghost-error p-2 text-sm text-left">
				<ul>
					{#each errors?.email as error}
						<li>{error}</li>
					{/each}
				</ul>
			</div>
		{/if}
		{#if errors?.token?.length > 0}
			<div class="card mb-2 variant-ghost-error p-2 text-sm text-left">
				<ul>
					{#each errors?.token as error}
						<li>{error}</li>
					{/each}
				</ul>
			</div>
		{/if}
		<div class="input-group mb-2 input-group-divider grid-cols-[1fr_auto] p-0">
			<input
				class="input"
				title="Token"
				type="password"
				id="token"
				name="token"
				placeholder="Token"
				bind:value={token}
				on:input={validateFields}
			/>
			<button type="button" on:click={togglePasswordInput}
				><i class="fa-regular fa-eye-slash"></i></button
			>
		</div>

		<button
      on:click={confirmSave}
			type="button"
			class="btn btn-xl variant-filled-primary my-2 w-fit shadow-xl"
			disabled={!validatedFields}>Guardar</button
		>
	</form>
</div>
{:else}
	<div class="flex justify-center mt-[8rem]">
		<div class="my-auto">
			<ProgressRadial/>
		</div>
	</div>
{/if}
