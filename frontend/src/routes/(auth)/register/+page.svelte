<script lang="ts">
	import { enhance } from '$app/forms';
	import { goto } from '$app/navigation';
	import { FormErrors } from '$lib/FormErrors';
	import { ProgressRadial } from '@skeletonlabs/skeleton';

	$: loaded = true;
	const fields = new FormErrors();

	interface FormErrors {
		email: any;
		password: any;
		name: any;
		confirmPassword: any;
		phoneNumber: any;
	}

	let errors: FormErrors = {
		email: [],
		password: [],
		confirmPassword: [],
		name: [],
		phoneNumber: []
	};
	let touched = {
		name: false,
		email: false,
		phoneNumber: false
	};

	let email = '';
	let name = '';
	let password = '';
	let confirmPassword = '';
	let phoneNumber = '';
	let validatedFields: any = false;
	function validateFields() {
		let valid: any = false;
		valid =
			error.validateEmail(email) &&
			error.validatePhoneNumber(phoneNumber) &&
			error.validateText(name);
		validatedFields = valid;
		return valid;
	}
	function togglePassword(event: Event) {
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
	function handleEnhance() {
		loaded = false;
		return ({ update, result }: any) => {
			if (result?.type == 'success') {
				goto('/dashboard/');
			} else {
				errors = result.data.error;
				loaded = true;
				return update({ reset: false });
			}
		};
	}
	let showPassword = false;

	let inputType = 'password';
	$: inputType = showPassword ? 'text' : 'password';
	let showRepPassword = false;

	let passwordError: any = true;
	const error = new FormErrors();
	let inputRepType = 'password';
	$: inputRepType = showRepPassword ? 'text' : 'password';
	function validatePassword() {
		if (password.length < 8) {
			passwordError = true;
		} else if (!error.hasNumbers(password)) {
			passwordError = true;
		} else if (!error.hasUpperCase(password)) {
			passwordError = true;
		} else if (password != confirmPassword) {
			passwordError = true;
		} else {
			passwordError = null;
		}
	}
</script>

<title>Registrar Vendedor</title>

{#if loaded}
	<div class="flex flex-col">
		<ol class="breadcrumb mb-[3rem]">
			<li class="crumb"><a class="anchor" href="/start">Inicio</a></li>
			<li class="crumb-separator" aria-hidden>/</li>
			<li class="crumb">Vendedor</li>
		</ol>

		<form
			class="flex flex-col space-y-2"
			method="post"
			action="?/register"
			use:enhance={handleEnhance}
		>
			<h3 class="text-4xl mb-[2rem]">Regístre su Vendedor</h3>

			<input
				class="input mb-2"
				title="Nombre"
				type="text"
				id="name"
				name="name"
				placeholder="Usuario"
				bind:value={name}
				on:input={validateFields}
				on:focus={() => (touched.name = true)}
			/>
			{#if touched.name}
				{#if name.length < 1}
					<div class="card variant-ghost-error mb-2 p-2 text-sm text-left">
						{fields.empyField}
					</div>
				{/if}
			{/if}

			<input
				class="input my-2"
				title="Email"
				type="text"
				id="email"
				name="email"
				placeholder="Email"
				bind:value={email}
				on:input={validateFields}
				on:focus={() => (touched.email = true)}
			/>
			{#if touched.email}
				{#if email.length > 0}
					{#if !fields.validateEmail(email) && touched.email}
						<div class="card variant-ghost-error mb-2 p-2 text-sm text-left">
							{fields.NotValidEmail}
						</div>
					{/if}
				{:else}
					<div class="card variant-ghost-error mb-2 p-2 text-sm text-left">
						{fields.empyField}
					</div>
				{/if}
			{/if}

			{#if errors?.email?.length > 0}
				<div class="card variant-ghost-error mb-2 p-2 text-sm text-left">
					<ul>
						{#each errors?.email as error}
							<li>{error}</li>
						{/each}
					</ul>
				</div>
			{/if}

			<div class="input-group input-group-divider grid-cols-[1fr_auto] p-0">
				<input
					class="input"
					title="Contraseña"
					type="text"
					id="password"
					name="password"
					placeholder="Contraseña"
					bind:value={password}
					on:input={validatePassword}
				/>
				<button type="button" on:click={togglePassword}
					><i class="fa-regular fa-eye-slash"></i></button
				>
			</div>
			<div
				class="mt-3 card p-4 text-left text-sm"
				class:variant-ghost-success={!passwordError}
				class:variant-ghost-error={passwordError}
			>
				<ul>
					<li>
						Tiene 8 caractéres o más {#if password.toString()?.length >= 8}
							<i class="fa-solid fa-check"></i>{:else}
							<i class="fa-solid fa-xmark"></i>{/if}
					</li>
					<li>
						Tiene números {#if error?.hasNumbers(password?.toString())}
							<i class="fa-solid fa-check"></i>{:else}
							<i class="fa-solid fa-xmark"></i>{/if}
					</li>
					<li>
						Tiene mayúsculas {#if error?.hasUpperCase(password?.toString())}
							<i class="fa-solid fa-check"></i>{:else}
							<i class="fa-solid fa-xmark"></i>{/if}
					</li>
					<li>
						Las contraseñas coinciden {#if password === confirmPassword && password?.toString().length > 0}
							<i class="fa-solid fa-check"></i>{:else}
							<i class="fa-solid fa-xmark"></i>{/if}
					</li>
				</ul>
			</div>

			<div class="input-group input-group-divider grid-cols-[1fr_auto] my-2">
				<input
					class="input"
					title="Confirmar Contraseña"
					type="text"
					id="confirmPassword"
					name="confirmPassword"
					placeholder="Confirmar Contraseña"
					bind:value={confirmPassword}
					on:input={validatePassword}
				/>
				<button type="button" on:click={togglePassword}
					><i class="fa-regular fa-eye-slash"></i></button
				>
			</div>

			<input
				class="input"
				title="telefono"
				type="text"
				id="phonenumber"
				name="phonenumber"
				placeholder="Número de telefono"
				bind:value={phoneNumber}
				on:input={validateFields}
				on:focus={() => (touched.phoneNumber = true)}
			/>
			{#if touched.phoneNumber}
				{#if phoneNumber.length > 0}
					{#if !fields.validatePhoneNumber(phoneNumber)}
						<div class="card variant-ghost-error p-2 text-sm text-left">
							{fields.NotValidPhone}
						</div>
					{/if}
				{:else}
					<div class="card variant-ghost-error mb-2 p-2 text-sm text-left">
						{fields.empyField}
					</div>
				{/if}
			{/if}
			{#if errors?.phoneNumber?.length > 0}
				<div class="card variant-ghost-error p-2 text-sm text-left">
					<ul>
						{#each errors?.phoneNumber as error}
							<li>{error}</li>
						{/each}
					</ul>
				</div>
			{/if}
			<button
				class="btn btn-xl variant-filled-primary my-2 w-full shadow-xl"
				disabled={!validatedFields || passwordError}>Registrarse</button
			>
			<p class="mt-4">
				¿Ya posees una cuenta? <a class="anchor no-underline" href="/login/user">Inicie sesión</a>
			</p>
		</form>
	</div>
{:else}
	<div class="flex justify-center mt-[8rem]">
		<div class="my-auto">
			<ProgressRadial />
		</div>
	</div>
{/if}
