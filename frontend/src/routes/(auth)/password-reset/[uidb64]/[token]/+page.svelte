<script lang="ts">
	import { enhance } from '$app/forms';
	import { goto } from '$app/navigation';
	import { FormErrors } from '$lib/FormErrors';
	import { getToastStore, type ToastSettings, ProgressRadial } from '@skeletonlabs/skeleton';

	const fields = new FormErrors();
	const toastStore = getToastStore();

	interface FormErrors {
		password: any;
		confirmPassword: any;
	}

	let errors: FormErrors = {
		password: [],
		confirmPassword: []
	};
	$: success = false;
	$: loaded = true;
	let password = '';
	let confirmPassword = '';

	let validatedFields: boolean = false;
	function validateFields() {
		validatedFields = fields.validatePasswords(password, confirmPassword);
	}

	function triggerSuccessToast() {
		let toast: ToastSettings = {
			message: 'Contraseña actualizada con exito.',
			background: 'variant-ghost-success',
			timeout: 3500
		};
		toastStore.trigger(toast);
	}
	function triggerErrorToast() {
		let toast: ToastSettings = {
			message: '¡ERROR! No se pudo enviar el correo.',
			background: 'variant-ghost-error',
			timeout: 3500
		};
		toastStore.trigger(toast);
	}

	async function handleEnhance() {
		loaded = false;
		return async ({ update, result }: any) => {
			if (result?.type === 'success') {
				triggerSuccessToast();
				success = true;
			} else {
				triggerErrorToast();
			}
			loaded = true;
			return update({ reset: false });
		};
	}

	function togglePasswordInput(event: Event) {
		let button = event.target as HTMLElement;
		if (button.tagName !== 'BUTTON') {
			// just in case the event.target is the icon and not the button
			button = button.closest('button') as HTMLElement;
		}
		const input = button.closest('.input-group')?.querySelector('input') as HTMLInputElement;
		input.type = input.type === 'password' ? 'text' : 'password';
		const icon = button.querySelector('i') as HTMLElement;
		icon.classList.toggle('fa-eye');
		icon.classList.toggle('fa-eye-slash');
	}
</script>

{#if !success}
	{#if loaded}
		<title>Reestablecer Contraseña</title>

		<div class=" mx-auto flex flex-col w-full">
			<form method="post" action="?/changepassword" use:enhance={handleEnhance}>
				<h3 class="text-4xl mb-[2rem]">Reestablecer Contraseña</h3>

				<div class="input-group mb-2 input-group-divider grid-cols-[1fr_auto] p-0">
					<input
						class="input"
						title="Contraseña"
						type="password"
						id="password"
						name="password"
						placeholder="Nueva Contraseña"
						bind:value={password}
						on:input={validateFields}
					/>
					<button type="button" on:click={togglePasswordInput}
						><i class="fa-regular fa-eye-slash"></i></button
					>
				</div>

				{#if password.length > 0}
					{#if password.length <= 5}
						<div class="card variant-ghost-error p-2 text-sm text-left">
							{fields.shortPass}
						</div>
					{:else if !fields.hasNumbers(password)}
						<div class="card variant-ghost-error p-2 text-sm text-left">
							{fields.NotNumbers}
						</div>
					{:else if !fields.hasUpperCase(password)}
						<div class="card variant-ghost-error p-2 text-sm text-left">
							{fields.NotUpperCase}
						</div>
					{/if}
				{/if}

				<div class="input-group input-group-divider grid-cols-[1fr_auto] my-2">
					<input
						class="input"
						title="Confirmar Contraseña"
						type="password"
						id="confirm_password"
						name="confirm_password"
						placeholder="Confirmar Contraseña"
						bind:value={confirmPassword}
						on:input={validateFields}
					/>
					<button type="button" on:click={togglePasswordInput}
						><i class="fa-regular fa-eye-slash"></i></button
					>
				</div>
				{#if confirmPassword.length > 0}
					{#if password !== confirmPassword}
						<div class="card variant-ghost-error p-2 text-sm text-left">
							{fields.NotMatchingPass}
						</div>
					{/if}
				{/if}
				{#if errors?.confirmPassword?.length > 0}
					<div class="card variant-ghost-error p-2 text-sm text-left">
						<ul>
							{#each errors?.confirmPassword as error}
								<li>{error}</li>
							{/each}
						</ul>
					</div>
				{/if}

				<button
					type="submit"
					class="btn btn-xl variant-filled-primary my-2 w-fit shadow-xl"
					disabled={!validatedFields}>Enviar</button
				>
			</form>
		</div>
	{:else}
		<div class="flex justify-center mt-[8rem]">
			<div class="my-auto">
				<div class="w-full justify-center flex"><ProgressRadial /></div>
			</div>
		</div>
	{/if}
{:else}
	<div class="flex justify-center mt-[8rem] flex-col">
		<div class="my-auto">
			<h2 class="h2 text-center mb-8">Contraseña actualizada</h2>
		</div>
		<button
			type="button"
			class="btn btn-xl variant-filled-primary my-2 w-fit shadow-xl mx-auto"
			on:click={() => goto('/start')}>Volver a inicio</button
		>
	</div>
{/if}
