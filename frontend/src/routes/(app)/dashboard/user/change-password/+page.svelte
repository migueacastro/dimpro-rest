<script lang="ts">
	import { enhance } from '$app/forms';
	import { goto } from '$app/navigation';
	import { FormErrors } from '$lib/FormErrors';

	const fields = new FormErrors();

	interface FormErrors {
		password: any;
		oldPassword: any;
		confirmPassword: any;
	}

	let errors: FormErrors = {
		oldPassword: [],
		password: [],
		confirmPassword: []
	};

	let password = '';
	let confirmPassword = '';
	let oldPassword = '';


	let validatedFields: boolean = false;
	function validateFields() {
		validatedFields = fields.validatePasswords(password, confirmPassword);
	}

	function handleEnhance() {
		return ({ update, result }: any) => {
			if (result.type === 'success') {
				goto('/dashboard/user');
			} else {
				console.error('Error changing password:', result.data);
				errors.oldPassword = [
					'La contraseña actual es incorrecta. Por favor, inténtelo de nuevo.'
				];
			}
			return update({reset: false});
		};
	}

	function togglePasswordInput(event: Event) {
		const button = event.target as HTMLElement;
		const input = button.closest('.input-group')?.querySelector('input') as HTMLInputElement;
		input.type = input.type === 'password' ? 'text' : 'password';
		const icon = button.closest('i') as HTMLElement;
		icon.classList.toggle('fa-eye');
		icon.classList.toggle('fa-eye-slash');
	}
</script>

<title>Registrar Vendedor</title>

<div class=" mx-auto flex flex-col lg:w-1/2 w-full">
	<form method="post" action="?/changepassword" use:enhance={handleEnhance}>
		<h3 class="text-4xl mb-[2rem]">Cambiar contraseña</h3>

		<div class="input-group mb-2 input-group-divider grid-cols-[1fr_auto] p-0">
			<input
				class="input"
				title="Contraseña"
				type="password"
				id="oldPassword"
				name="oldPassword"
				placeholder="Contraseña"
				bind:value={oldPassword}
				on:input={validateFields}
			/>
			<button type="button" on:click={togglePasswordInput}
				><i class="fa-regular fa-eye-slash"></i></button
			>
		</div>
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
		{#if errors?.oldPassword?.length > 0}
			<div class="card variant-ghost-error p-2 text-sm text-left">
				<ul>
					{#each errors?.password as error}
						<li>{error}</li>
					{/each}
				</ul>
			</div>
		{/if}
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
				id="confirmPassword"
				name="confirmPassword"
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
			class="btn btn-xl variant-filled-primary my-2 w-fit shadow-xl"
			disabled={!validatedFields}>Guardar</button
		>
	</form>
</div>
